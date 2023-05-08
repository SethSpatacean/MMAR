# # Setup

# In[ ]:


import pandas as pd
import pyodbc
import numpy as np
import matplotlib.pyplot as plt
import getpass
from tableone import TableOne
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('load_ext', 'sql')

server = "host.docker.internal" # IP ADDRESS OF SERVER
db = "confirm_db" # NAME OF DATABASE
username = "sa"
password = 


# In[6]:


conn = pyodbc.connect(
                     driver='{sqlsrv}',
                     server=server,
                     port=1433,
                     database=db,
                     uid=username,
                     pwd=password)


# # Query database

# In[11]:


tbl_mcp = pd.read_sql("Select * from tblMCP WHERE id_vessel Like '%dist%'", conn)
tbl_perlesion = pd.read_sql("Select * from tblConfirmPerLesion", conn)
tbl_confirm = pd.read_sql("Select * from tblConfirmCONFIRM", conn)


# # Check queries

# ### View Table - MCP

# In[14]:


tbl_mcp


# ### View Table - PerLesion

# In[15]:


tbl_perlesion


# ### View Table - Confirm

# In[16]:


tbl_confirm


# # Merge Per Lesion Data

# In[27]:


# Rename ID columns to allow merging
tbl_mcp = tbl_mcp.rename(columns = {'id_vessel_study' : 'lesion_id'})

# Merge tbl_mcp with tbl_perlesion
tbl_merge_perlesion = tbl_perlesion.merge(tbl_mcp[['lesion_id', 'mass_mcp_perc', 'mass_mcp_g']], on='lesion_id', how='right')

# Check tbl_merge_perlesion
tbl_merge_perlesion


# In[30]:


# View columns in tbl_merge_perlesion
print(tbl_merge_perlesion.columns)


# # Select lesion with largest diameter stenosis for each patient

# In[35]:


maxds_idx = tbl_merge_perlesion.groupby(['confirm_idc'])['lumendiameterstenosis'].transform(max) == tbl_merge_perlesion['lumendiameterstenosis']
tbl_merge_perlesion_maxds = tbl_merge_perlesion[maxds_idx]
tbl_merge_perlesion_maxds
