import pandas as pd

df = pd.read_csv("output/2016Census_G03_VIC_SED_2022.csv")

df = df.melt(id_vars="district", var_name="census_variable", value_name="value")

df.to_csv("output/2016Census_G03_VIC_SED_2022_unpivot_sorted.csv", index=False)

out = df.sort_values(by=["census_variable", "value"])

out.to_csv("output/2016Census_G03_VIC_SED_2022_unpivot_sorted.csv", index=False)

tmp = out.groupby("census_variable").size()
rank = tmp.map(range)
rank = [item for sublist in rank for item in sublist]
out["rank"] = rank
out["rank"] = out["rank"] + 1

out.to_csv("output/2016Census_G03_VIC_SED_2022_unpivot_sorted_ranked.csv", index=False)
