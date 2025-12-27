import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/exports/mart_stability.csv")

plt.figure(figsize=(8,5))
plt.plot(df["checkpoint"], df["raw_tickets"], marker="o", label="Raw metric")
plt.plot(df["checkpoint"], df["mart_tickets"], linestyle="--", label="Mart metric")

plt.title("Raw vs Stable Metric for the Same Sale Date")
plt.xlabel("Observation time")
plt.ylabel("Tickets sold")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("../diagrams/mart_stability.png")
plt.show()
