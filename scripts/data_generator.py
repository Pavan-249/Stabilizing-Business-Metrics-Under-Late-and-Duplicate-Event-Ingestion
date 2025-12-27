import datetime
from datetime import timedelta
from random import sample
import random
import uuid
from faker import Faker
random.seed(42)

start_date = datetime.date(2026,6,11)
end_date = start_date+timedelta(days=90)
start = start_date
random_90_dates = [start_date]

while start_date != end_date:
    start_date += timedelta(days=1)
    random_90_dates.append(start_date)

random_50_dates = sample(random_90_dates, k=50)
random_50_dates.sort()
match_dates = random_50_dates

import pandas as pd
import random
import datetime
from datetime import datetime


team_rows = []
stadium_rows = []
match_rows = []
team_ids = ["T01","T02","T03","T04","T05","T06","T07","T08","T09","T10"]
team_name = ["France","Senegal","South Africa","Spain","Switzerland","Argentina","Uruguay","England",
"Croatia", "Belgium"]

for i in range(len(team_ids)):
    team_row = {
        "team_id": team_ids[i],
        "team_name": team_name[i]
        }
    team_rows.append(team_row)
    
team_table = pd.DataFrame.from_records(team_rows)


stadium_ids = ["S01","S02","S03","S04","S05","S06","S07","S08","S09","S10"]
stadium_names = ["Lumen Field","BC Place","MetLife Stadium",
"Mercedes-Benz Stadium","BMO Field","AT&T Stadium","NRG Stadium","GEHA Field at Arrowhead Stadium",
"SoFi Stadium","Hard Rock Stadium","Levi’s Stadium","Lincoln Financial Field"]
stadium_capacity = [random.randint(50,70)*1000 for i in range(10)]
avg_ticket_price = [random.randint(500,1000) for i in range(10)]

for i in range(len(stadium_ids)):
    stadium_row = {
        "stadium_id": stadium_ids[i],
        "stadium_name": stadium_names[i],
        "stadium_capacity": stadium_capacity[i],
        "avg_ticket_price": avg_ticket_price[i]
    }
    stadium_rows.append(stadium_row)

stadium_table = pd.DataFrame.from_records(stadium_rows)

match_ids = [str(i) for i in range(1,51)]
match_ids = list(map(lambda x: "M"+ x, match_ids))

for i in range(len(match_ids)):
    home = random.choice(team_ids)
    away = random.choice([t for t in team_ids if t != home])

    match_row = {
        "match_id": match_ids[i],
        "home_team_id": home,
        "away_team_id": away,
        "stadium_id": random.choice(stadium_ids),
        "match_date": match_dates[i]
    }
    match_rows.append(match_row)
match_table = pd.DataFrame.from_records(match_rows)
from datetime import datetime, timedelta
import random

def get_purchase_time():
    now = datetime.utcnow()
    delta = timedelta(
        days=random.randint(0, 6),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )
    return now - delta

quantity_choices = [x for x in range(1,10)]
transactions = []

Faker.seed(42)
fake = Faker()
total_transactions_num = 50000
ticket_categories_map = {'GA':1,'Student':0.7,'VIP':1.3}


for i in range(total_transactions_num):
    match_id = random.choice(match_ids)
    stadium_id = match_table[match_table["match_id"]==match_id]['stadium_id'].iloc[0]
    stadium_name = stadium_table[stadium_table["stadium_id"]==stadium_id]['stadium_name'].iloc[0]
    quantity = random.choice(quantity_choices)
    ticket_category = random.choice(list(ticket_categories_map.keys()))
    ticket_multiplier = ticket_categories_map[ticket_category]
    amount = stadium_table[stadium_table["stadium_id"]==stadium_id]['avg_ticket_price'].iloc[0]*quantity*ticket_multiplier
    match_date = match_table[match_table["match_id"]==match_id]['match_date'].iloc[0]
    purchase_time = get_purchase_time()
    ticketId = str(uuid.uuid4())
    
    user_id  = "FIFAW26"+str(i).zfill(6)
    user_name = fake.first_name() + " " + fake.last_name()
    user_email = fake.unique.ascii_free_email()
    
    transactions.append({
        "ticket_id": ticketId,
        "match_id": match_id,
        "user_id": user_id,
        "user_name": user_name,
        "user_email": user_email,
        "ticket_type": ticket_category,
        "quantity": quantity,
        "stadium": stadium_name,
        "price": round(amount, 2),
        "purchase_timestamp": purchase_time
    })

base_df = pd.DataFrame(transactions)

base_df.to_csv('../data/transaction_data.csv')
match_table.to_csv(
    "../data/matches_data.csv",
    index=False
)
stadium_table.to_csv(
    "../data/stadium_data.csv",
    index=False
)
team_table.to_csv(
    "../data/team_data.csv",
    index=False
)
