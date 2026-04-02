import pandas as pd
import random
from datetime import datetime, timedelta

products = ["Laptop", "Phone", "Tablet", "Headphones"]
regions = ["North", "South", "East", "West"]

data = []

start_date = datetime(2025, 1, 1)

for i in range(200):  # 200 rows = more realistic
    date = start_date + timedelta(days=random.randint(0, 90))
    product = random.choice(products)
    region = random.choice(regions)
    sales = random.randint(50, 500)
    quantity = random.randint(1, 5)

    data.append([date.strftime("%Y-%m-%d"), product, region, sales, quantity])

df = pd.DataFrame(data, columns=["Date", "Product", "Region", "Sales", "Quantity"])
df.to_csv("sales.csv", index=False)

print("Dataset generated: sales.csv")