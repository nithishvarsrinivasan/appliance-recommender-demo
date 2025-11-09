
import os, random, pandas as pd

APPLIANCES = ["Fridge","Washing Machine","Air Conditioner","Water Heater","Microwave","TV","Dishwasher","Ceiling Fan","Laptop","Lighting"]

def simulate_csv(csv_path: str, n_users: int = 10, seed: int = 42):
    random.seed(seed)
    rows = []
    for i in range(1, n_users+1):
        uid = f"U{i}"
        k = random.randint(5,8)
        apps = random.sample(APPLIANCES, k)
        base_power = {
            "Fridge": 1.2, "Washing Machine": 0.9, "Air Conditioner": 3.5, "Water Heater": 4.5,
            "Microwave": 1.1, "TV": 0.2, "Dishwasher": 1.5, "Ceiling Fan": 0.07, "Laptop": 0.06, "Lighting": 0.05
        }
        for app in apps:
            power_kwh = round(base_power[app]*random.uniform(0.8,1.3),3)
            usage = random.randint(10,200)
            rows.append((uid, app, power_kwh, usage))
    df = pd.DataFrame(rows, columns=["user_id","appliance","power_kwh","usage_count"])
    df.to_csv(csv_path, index=False)
    return df

def ensure_data(data_dir: str) -> str:
    os.makedirs(data_dir, exist_ok=True)
    path = os.path.join(data_dir,"simulated_usage.csv")
    if not os.path.exists(path): simulate_csv(path)
    return path

def load_data(csv_path: str):
    import pandas as pd
    return pd.read_csv(csv_path)
