import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "../data/exports/etric_instability.csv"
)

plt.figure(figsize=(8, 5))
plt.plot(df["checkpoint"], df["tickets_sold"], marker="o")

for i, row in df.iterrows():
    plt.text(
        row["checkpoint"],
        row["tickets_sold"],
        row["observed_at"].split(".")[0],  
        ha="right",
        va="bottom",
        fontsize=8
    )

plt.title("Metric Instability Observed for December 20,2025 due to Late-Arrival of Data")
plt.xlabel("When metrics were queried")
plt.ylabel("Tickets sold")
plt.grid(True)

plt.tight_layout()
plt.savefig("metric_instability.png", dpi=150)
plt.show()
