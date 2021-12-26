import pandas as pd

run = False

if run:

    df = pd.read_csv("test-data/2016Census_G03_VIC_SED_2022.csv")

    # unpivot
    df = df.melt(id_vars="district", var_name="census_variable", value_name="value")
    df.to_csv("output/2016Census_G03_VIC_SED_2022_unpivot.csv", index=False)

    # sort
    out = df.sort_values(by=["census_variable", "value"])
    out.to_csv("output/2016Census_G03_VIC_SED_2022_unpivot_sorted.csv", index=False)

    # remove n
    remove_rows = out[out["census_variable"].str.endswith("_n")].index
    out.drop(remove_rows, inplace=True)

    # rank
    tmp = out.groupby("census_variable").size()
    rank = tmp.map(range)
    rank = [item for sublist in rank for item in sublist]
    out["rank"] = rank
    out["rank"] = out["rank"] + 1

    out.to_csv("output/2016Census_G03_VIC_SED_2022_unpivot_sorted_ranked.csv", index=False)

    # pivot
    test = out.pivot(index="census_variable", columns="district", values="value")
    test.to_csv("output/2016Census_G03_VIC_SED_2022_pivot.csv")
