import pandas as pd
import csv

df = pd.read_csv("US_births_2000-2014_SSA.csv")

# favourable cases
grouped = df.groupby(["month", "date_of_month"])
totals = grouped.sum()

# possible events
tot_totals = totals["births"].sum()

# frequentist probability
probabilities = totals["births"].apply(lambda x: x/tot_totals)
#print(probabilities)


with open("probabilities.csv", "w") as csf:
    header = "mm/dd,probabilities\n"
    csf.write(header)


with open("probabilities.csv", "a") as csf:
    for k,v in zip(probabilities.index, probabilities):
        csf.write(f"{k[0]}/{k[1]},{v}\n")
