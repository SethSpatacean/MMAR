# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 17:36:24 2021

@author: smalk

"""

# Import - Included

# Import - Third-party
import numpy as np
from tableone import TableOne
import seaborn as sns
import matplotlib.pyplot as plt
# Import - Project specific
import toolbox

sns.set_theme()
# plt.style.use("dark_background")

# -------------------------------- Load data ------------------------------- #
import load_data
df_per_lesion = load_data.PER_LESION
df_per_patient = load_data.PER_PATIENT

# -------------------------- Statistical analysis -------------------------- #

df_per_lesion = df_per_lesion.loc[df_per_lesion['lesion_culprit_ica_ct'] == 1]
df_per_lesion = df_per_lesion.loc[(df_per_lesion['mi_type'] == '1') | (df_per_lesion['mi_type'] == '4')]
df_per_lesion = df_per_lesion.loc[df_per_lesion['id_main_vessel'] == 'lad']

# FIX VESSEL IDs FOR BETTER DISPLAY:
df_per_lesion['mi_type'] = df_per_lesion['mi_type'].astype('str')
    
df_per_lesion['mi_type'] = df_per_lesion['mi_type'].replace('1', 'STEMI')
df_per_lesion['mi_type'] = df_per_lesion['mi_type'].replace('2', 'NSTEMI')
df_per_lesion['mi_type'] = df_per_lesion['mi_type'].replace('3', 'UA/UNKNOWN')
df_per_lesion['mi_type'] = df_per_lesion['mi_type'].replace('4', 'UA/UNKNOWN')



# df_per_lesion['mi_type'] = df_per_lesion['mi_type'].replace('1', 'STEMI/NSTEMI')
# df_per_lesion['mi_type'] = df_per_lesion['mi_type'].replace('2', 'OTHER')
# df_per_lesion['mi_type'] = df_per_lesion['mi_type'].replace('3', 'OTHER')
# df_per_lesion['mi_type'] = df_per_lesion['mi_type'].replace('4', 'OTHER')



## Generate tables

### Table 1 - Atherosclerotic features

### Table 1 - General demographic data
demographic_cols = ['age_confirm',
                    'sex_confirm',
                    'bmi_confirm',
                    ]

demographic_categorical_cols = ['sex_confirm', 
                                # 'htn_confirm', 
                                # 'dm_confirm', 
                                # 'chol_confirm'
                                ]
tbl_demographics = TableOne(df_per_patient, columns=demographic_cols, categorical=demographic_categorical_cols)

risk_factors_cols = ['htn_confirm',
                    'chol_confirm',
                    'dm_confirm',
                    'smokecurrent_confirm',
                    'smokepast_confirm',
                    'famhx_confirm',
                    ]

risk_factors_cat_cols = ['htn_confirm', 
                        'chol_confirm',
                        'dm_confirm',
                        'smokecurrent_confirm',
                        'smokepast_confirm',
                        'famhx_confirm',
                        ]
tbl_risk_factors = TableOne(df_per_patient, columns=risk_factors_cols, categorical=risk_factors_cat_cols)

### Table - CAD Severity - Note:  cad_vesselN is number of lesions >50%, not number of diseased lesions in general!
cad_severity_cols = [
                     'cad_severity',
                     'pat_numlesions',
                     'cad_normal_obstruction',
                     'cad_obstruction',
                     'cad_vesseln',
                     'cad_vessel0',
                     'cad_vessel1',
                     'cad_vessel2',
                     'cad_vessel3',
                     'plaque_anyn',
                     'plaque_any1',
                     'plaque_any2',
                     'plaque_any3',
                     'plaque_modn',
                     'plaque_mod1',
                     'plaque_mod2',
                     'plaque_mod3',
                     'plaque_severen',
                     'plaque_severe1',
                     'plaque_severe2',
                     'plaque_severe3',
                     'lm_50_confirm',
                    ]

cad_severity_cat_cols = [
                         'cad_severity',
                         'cad_normal_obstruction',
                         'cad_obstruction',
                         'cad_vesseln',
                         'cad_vessel0',
                         'cad_vessel1',
                         'cad_vessel2',
                         'cad_vessel3',
                         'plaque_anyn',
                         'plaque_any1',
                         'plaque_any2',
                         'plaque_any3',
                         'plaque_modn',
                         'plaque_mod1',
                         'plaque_mod2',
                         'plaque_mod3',
                         'plaque_severen',
                         'plaque_severe1',
                         'plaque_severe2',
                         'plaque_severe3',
                         'lm_50_confirm',
                        ]
tbl_cad_severity = TableOne(df_per_patient, columns=cad_severity_cols, categorical=cad_severity_cat_cols)

### Table - CAD Severity - Per-Patient level
cols = [
        'pat_regionlength',
        'pat_vesselvolume',
        'pat_lumenvolume',
        'pat_plaquevolume',
        'pat_fibrousvolume',
        'pat_fibrousfattyvolume',
        'pat_necroticcorevolume',
        'pat_densecalciumvolume',
        'pat_noncalcifiedvolume',
        'pat_percent_apv',
        ]
tbl_patient_plaque_burden = TableOne(df_per_patient, columns=cols)


### Table per-lesion plaque characteristics
cols = [
        'mass_mcp_perc',
        'omlddistance',
        'lesion_length',
        'vesselvolume_lesion',
        'plaquevolume_lesion',
        'necroticcorevolume_lesion',
        'fibrousfattyvolume_lesion',
        'fibrousvolume_lesion',
        'densecalcium_area',
        'id_main_vessel',
        ]
cat = ['id_main_vessel']
tbl_per_lesion = TableOne(df_per_lesion, columns=cols, categorical=cat, groupby=['mi_type'], pval=True)

cols = [
        'mass_mcp_perc',
        'omlddistance',
        'lesion_length',
        'vesselvolume_lesion',
        'lumenvolume_lesion',
        'plaquevolume_lesion',
        'fibrousvolume_lesion',
        'fibrousfattyvolume_lesion',
        'necroticcorevolume_lesion',
        'densecalciumvolume_lesion',
        'noncalcifiedvolume_lesion',
        'plaqueburdenmean_lesion',
        'lesionmaximalplaquethickness',
        'lumenarea',
        'lumenareastenosis',
        'lumenmeandiameter',
        'lumendiameterstenosis',
        'lumenminimaldiameter',
        'vesselwallarea',
        'vesselwallmeandiameter',
        'plaqueeccentricity',
        'plaqueburden',
        'vesselwallremodelingindex',
        'plaquethicknessmaximal',
        'fibrous_area',
        'fibrousfatty_area',
        'necroticcore_area',
        'densecalcium_area',
        ]

# toolbox.visualize.composite_histplot(df_per_lesion, cols, 'lesion_culprit_ica_ct', nbins=15)
# toolbox.visualize.composite_violinplot(df_per_lesion, cols, 'lesion_culprit_ica_ct')


## Figure 1 - Boxplot of MMAR - grouped by SCCT
BOXPROPS = {
            'whis' : np.inf,
            'linewidth' : 1.5,
            'showfliers' : False,
            'showmeans' : False,
            'meanprops' : {"marker": "+",
                           "markeredgecolor": "black",
                           "markersize": 12},
            } 
    
STRIPPLOTPROPS = {
        'dodge' : True,
        'edgecolor' : 'white',
        'linewidth' : .5,
        'alpha' : .70,
        's' : 6, # CHANGE TO 10
        }

fig1 = plt.figure()
# MAKE CUSTOM PALETTE
colors = ['#93B7BE', '#E63946']
# custom_palette = sns.set_palette(sns.color_palette(colors))

ax = sns.boxplot(y="mass_mcp_perc", x="mi_type",
                   data=df_per_lesion, color=colors[0], **BOXPROPS)

ax = sns.stripplot(y="mass_mcp_perc", x="mi_type",
                   data=df_per_lesion, color=colors[0], ax=ax, **STRIPPLOTPROPS)
ax.legend([],[], frameon=False)
plt.ylabel('Myocardial Mass (%)', fontsize=16, fontweight='bold')
plt.xticks(fontsize=12)
plt.xlabel('ACS Type', fontsize=16, fontweight='bold')
plt.yticks(fontsize=12)
plt.tight_layout()
plt.ylim(-1, 100)


## View Tables:
print(tbl_per_lesion.tabulate(tablefmt='fancy_grip'))

# ------------------- Generate Markdown file for results ------------------- #

