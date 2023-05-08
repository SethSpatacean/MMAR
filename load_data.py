# -*- coding: utf-8 -*-
"""
Created on Thu May 20 13:28:48 2021

@author: seths
"""
import pandas as pd
import numpy as np

# Import - Project specific
import toolbox
import toolbox.process as process


# ------------------------------ Define paths ------------------------------ #
path_db = '//neptune.radsci.uci.edu/NeptuneData/Datasets/CONFIRM/database/db_CONFIRM.accdb'

# ------------------------------ Import data ------------------------------- #

## Import CONFIRM clinical data (cast type of confirm_idc for merging with MMAR data)
qsel_confirm = 'SELECT * FROM tblConfirmCONFIRM;'
df_confirm = toolbox.process.db_query(path_db, qsel_confirm)
df_confirm['confirm_idc'] = df_confirm['confirm_idc'].astype('int64')

## Import CONFIRM per patient data
qsel_per_patient = 'SELECT * FROM tblConfirmPerPatient;'
df_per_patient = toolbox.process.db_query(path_db, qsel_per_patient)
df_per_patient['confirm_idc'] = df_per_patient['confirm_idc'].astype('int64')

## Import CONFIRM per lesion data
qsel_lesion = 'SELECT * FROM tblConfirmPerLesion;'
df_lesion = toolbox.process.db_query(path_db, qsel_lesion)
df_lesion['confirm_idc'] = df_lesion['confirm_idc'].astype('int64')
df_lesion['lesion_culprit_ica_ct'] = pd.to_numeric(df_lesion['lesion_culprit_ica_ct'], errors='coerce').fillna(0)

## Import myocardial mass at-risk data (must rename id_patient to confirm_idc for merging with CONFIRM dataset)
qsel_mmar = 'SELECT * FROM tblMCP;'
df_mmar = toolbox.process.db_query(path_db, qsel_mmar)
df_mmar = df_mmar.rename(columns={'id_patient' : 'confirm_idc', 'id_vessel_study' : 'lesion_id'})
df_mmar['confirm_idc'] = df_mmar['confirm_idc'].astype('int64')

## Import quality assurrance of MMAR (must rename id_patient to confirm_idc for merging with CONFIRM dataset)
qsel_mmar_qa = 'SELECT * FROM tblMCP_QA;'
df_mmar_qa = toolbox.process.db_query(path_db, qsel_mmar_qa)
df_mmar_qa = df_mmar_qa.rename(columns={'id_patient' : 'confirm_idc'})
df_mmar_qa['confirm_idc'] = df_mmar_qa['confirm_idc'].astype('int64')

# ------------------------------- Clean data ------------------------------- #

## DUMMY VARS - df_confirm - determine severity
df_confirm['cad_normal_obstruction'] = (df_confirm['obstructive_cad_confirm'] == 0).astype('int')
df_confirm['cad_no_obstruction'] = (df_confirm['obstructive_cad_confirm'] == 1).astype('int')
df_confirm['cad_obstruction'] = (df_confirm['obstructive_cad_confirm'] == 2).astype('int')
df_confirm['cad_severity'] = (df_confirm['cad_severity'] > 1).astype('int')

df_confirm['cad_vessel0'] = (df_confirm['num_vessel_disease_confirm'] == 0).astype('int')
df_confirm['cad_vessel1'] = (df_confirm['num_vessel_disease_confirm'] == 1).astype('int')
df_confirm['cad_vessel2'] = (df_confirm['num_vessel_disease_confirm'] == 2).astype('int')
df_confirm['cad_vessel3'] = (df_confirm['num_vessel_disease_confirm'] == 3).astype('int')
df_confirm['cad_vesseln'] = (df_confirm['num_vessel_disease_confirm'] > 1).astype('int')

df_confirm['plaque_anyn'] = (df_confirm['num_vessel_plaque_confirm'] > 1).astype('int')
df_confirm['plaque_any1'] = (df_confirm['num_vessel_plaque_confirm'] == 1).astype('int')
df_confirm['plaque_any2'] = (df_confirm['num_vessel_plaque_confirm'] == 2).astype('int')
df_confirm['plaque_any3'] = (df_confirm['num_vessel_plaque_confirm'] == 3).astype('int')

df_confirm['plaque_modn'] = (df_confirm['num_vessel_mod_confirm'] > 1).astype('int')
df_confirm['plaque_mod1'] = (df_confirm['num_vessel_mod_confirm'] == 1).astype('int')
df_confirm['plaque_mod2'] = (df_confirm['num_vessel_mod_confirm'] == 2).astype('int')
df_confirm['plaque_mod3'] = (df_confirm['num_vessel_mod_confirm'] == 3).astype('int')

df_confirm['plaque_severen'] = (df_confirm['num_vessel_severe_confirm'] > 1).astype('int')
df_confirm['plaque_severe1'] = (df_confirm['num_vessel_severe_confirm'] == 1).astype('int')
df_confirm['plaque_severe2'] = (df_confirm['num_vessel_severe_confirm'] == 2).astype('int')
df_confirm['plaque_severe3'] = (df_confirm['num_vessel_severe_confirm'] == 3).astype('int')

## FILTER - df_mmar_qa - select patients with permissible image data
df_mmar_qa = df_mmar_qa.loc[(df_mmar_qa['qa_mcp'] == 3) & (df_mmar_qa['qa_centerlines'] == 3) & (df_mmar_qa['qa_lv_segmentation'] == 3)]

## DUMMY VAR - df_mmar - find lesion for each patient with most MMAR
lesion_id_max_mmar = df_mmar[df_mmar.groupby('confirm_idc')['mass_mcp_perc'].transform('max') == df_mmar['mass_mcp_perc']]['lesion_id']
df_mmar['lesion_max_mmar'] = 0
df_mmar.loc[df_mmar['lesion_id'].isin(lesion_id_max_mmar), 'lesion_max_mmar'] = 1

## FILTER - df_mmar - select patients with permissible QA
df_mmar = df_mmar.loc[df_mmar['confirm_idc'].isin(df_mmar_qa['confirm_idc'])]

## FILTER - df_mmar - select mmar in the LAD only
# df_mmar = df_mmar.loc[df_mmar['id_main_vessel'] == 'lad']

## FILTER - df_mmar - select only DISTAL mass at-risk
df_mmar = df_mmar.loc[df_mmar['id_vessel'].str.contains('_dist')]

## DUMMY VAR - df_lesion - select lesion with largest plaque volume
lesion_id_max_pv = df_lesion[df_lesion.groupby('confirm_idc')['plaquevolume_lesion'].transform('max') == df_lesion['plaquevolume_lesion']]['lesion_id']
df_lesion['lesion_max_pv'] = 0
df_lesion.loc[df_lesion['lesion_id'].isin(lesion_id_max_pv), 'lesion_max_pv'] = 1

## FILTER - df_lesion - select patients present in df_mmar
df_lesion = df_lesion.loc[df_lesion['lesion_id'].isin(df_mmar['lesion_id'])]

## FILTER - df_lesion - select culprit lesions only (should be one entry per patient)
# df_lesion = df_lesion.loc[(df_lesion['lesion_culprit_ica_ct'] == 1)]

## FILTER - df_lesion - select confirm_idc remaining after filtering based on lesion vessel location
# We need this block because we filtered based on lesion location - i.e. we only want to include patients wherein a culprit lesion was included
# Without this block, we might end up patients WITHOUT a culprit lesion as the culprit lesion was filtered when we filtered by lesion location
confirm_idc_w_mi = df_lesion.loc[(df_lesion['lesion_culprit_ica_ct'] == 1)]['confirm_idc']
df_lesion = df_lesion.loc[df_lesion['confirm_idc'].isin(confirm_idc_w_mi)]

## FILTER - df_mmar - select lesions with matching lesion_id from df_lesion
df_mmar = df_mmar.loc[df_mmar['lesion_id'].isin(df_lesion['lesion_id'])]

## FILTER - df_confirm - select clinical variables only for patients in df_mmar
df_confirm = df_confirm.loc[df_confirm['confirm_idc'].isin(df_mmar['confirm_idc'])]

## AGGREGATE
# NOTHING TO AGGREGATE HERE...

## MERGE
df_mmar_lesion = df_mmar.merge(df_lesion.drop(columns='confirm_idc'), on='lesion_id', how='left')
df_mmar_lesion = df_mmar_lesion.merge(df_confirm[['confirm_idc', 'mi_time']], on='confirm_idc', how='left')
df_confirm_per_patient = df_confirm.merge(df_per_patient, on='confirm_idc', how='left')
# ------------------------ Create final dataframes ------------------------- #
PER_PATIENT = df_confirm_per_patient
PER_LESION = df_mmar_lesion