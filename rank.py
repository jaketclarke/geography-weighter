# An example file to rank variables in output file.

import pandas as pd

df = pd.read_excel('output/2021Census_G01_VIC_SED_2022.xlsx')
# df = pd.read_csv('output/2021Census_G01_VIC_SED_2022.csv')

df = df.melt(id_vars = 'District', var_name = 'census_variable', value_name = 'value')

out = df.sort_values(by=['census_variable', 'value'])

out.to_csv('output/2016Census_G01_VIC_SED_2022_unpivot_sorted.csv', index="False")

tmp = out.groupby('census_variable').size()
rank = tmp.map(range)
rank =[item for sublist in rank for item in sublist]
out['rank'] = rank
out["rank"] = out["rank"] + 1

out.to_csv('output/2016Census_G01_VIC_SED_2022_unpivot_sorted_processed.csv', index="False")


transform = pd.pivot_table(data=out, index=['District','census_variable'])
transform = transform.reset_index()
transform = transform.drop('value',1)


print(transform)

pivot = transform.pivot(index='District', columns='census_variable',values='rank')

print(pivot)

pivot.to_csv('output/2016Census_G01_VIC_SED_2022_Ranks.csv')