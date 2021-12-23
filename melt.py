import pandas as pd

df = pd.read_csv('output/2016Census_G01_VIC_SED_2022.csv')

df = df.melt(id_vars = 'district', var_name = 'census_variable', value_name = 'value')

df.to_csv('output/2016Census_G01_VIC_SED_2022_unpivot_sorted.csv')

out = df.sort_values(by=['census_variable', 'value'])

out.to_csv('output/2016Census_G01_VIC_SED_2022_unpivot_sorted.csv')