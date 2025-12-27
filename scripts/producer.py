import json
import time
import pandas as pd
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

df = pd.read_csv("../data/transaction_data.csv")

for i, row in df.iterrows():
    event = row.to_dict()
    producer.send("ticket_purchases_raw", event)

    if i % 500 == 0:
        print(f"Sent {i} events")
        time.sleep(1)  # Simulate a small delay between events
producer.flush()
print("Finished sending ticket purchase events")
