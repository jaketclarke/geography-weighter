# An example file to rank variables in output file.

import pandas as pd

df = pd.read_excel('output/2021Census_G01_VIC_SED_2022.xlsx', na_values=['Null','NaN','nan','Nan'])

df = df.melt(id_vars = 'District', var_name = 'census_variable', value_name = 'value')

out = df.sort_values(by=['census_variable', 'value'])

out.to_csv('output/2016Census_G01_VIC_SED_2022_unpivot_sorted.csv', index="False", na_rep='Null')

tmp = out.groupby('census_variable').size()
rank = tmp.map(range)
rank =[item for sublist in rank for item in sublist]
out['rank'] = rank
out["rank"] = out["rank"] + 1

# if all the input data is NaN, don't rank
input_data.loc[input_data['value'].isnull(), 'rank'] = np.nan

output_file = input_file.replace('unpivoted','ranked_unpivoted')
input_data.to_csv(f'output{os.sep}{output_file}', index=False, na_rep='Null')

out.to_csv('output/2016Census_G01_VIC_SED_2022_unpivot_sorted_processed.csv', index="False", na_rep='Null')


transform = pd.pivot_table(data=out, index=['District','census_variable'])
transform = transform.reset_index()
transform = transform.drop('value',1)


print(transform)

pivot = transform.pivot(index='District', columns='census_variable',values='rank')

print(pivot)

pivot.to_csv('output/2016Census_G01_VIC_SED_2022_Ranks.csv')
