import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("/Users/pavankumar_s/Desktop/Data Engineering/real_time_tickets_observability/dbt_project/dbs_obs/metric_instability.csv")

plt.figure(figsize=(8,5))
plt.plot(df["checkpoint"], df["tickets_sold"], marker="o")
plt.title("Metric Instability Due to Late Arriving Data")
plt.xlabel("Observation Time")
plt.ylabel("Tickets Sold")
plt.grid(True)

plt.tight_layout()
plt.show()
