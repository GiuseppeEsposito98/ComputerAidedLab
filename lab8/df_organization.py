import pandas as pd
import csv

df = pd.read_csv("US_births_2000-2014_SSA.csv")
#print(df.head())

grouped = df.groupby(["month", "date_of_month"])
totals = grouped.sum()
tot_totals = totals["births"].sum()

probabilities = totals["births"].apply(lambda x: x/tot_totals)



#probabilities = list()

# with open("probabilities.csv", "w") as csf:
#     header = "mm/dd,probabilities\n"
#     csf.write(header)
print(probabilities.index)

#with open("probabilities.csv", "a") as csf:
for k,v in enumerate(probabilities):
    print("v: ",v)
    print("k: ",k)
        #for val in v["births"]:
        #    csf.write(f"{k[0]}/{k[1]},{val/(totals.loc[k]['births'])}\n")
