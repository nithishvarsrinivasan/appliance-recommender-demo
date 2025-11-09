
import pandas as pd

EFFICIENT_MODELS = {
    "Fridge":"Fridge Pro Efficient A++",
    "Washing Machine":"Washer EcoMax Inverter",
    "Air Conditioner":"Air Conditioner A+++ Inverter",
    "Water Heater":"Water Heater Heat-Pump A+",
    "Microwave":"Microwave Inverter Efficient",
    "TV":"LED TV A+",
    "Dishwasher":"Dishwasher EcoSense A++",
    "Ceiling Fan":"BLDC Ceiling Fan Super Saver",
    "Laptop":"Laptop Low-Power Model",
    "Lighting":"LED Lighting A+"
}

class Recommender:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df["usage_norm"] = self.df.groupby("user_id")["usage_count"].transform(lambda s:(s-s.min())/(s.max()-s.min()+1e-9))
        self.df["power_norm"] = self.df.groupby("user_id")["power_kwh"].transform(lambda s:(s-s.min())/(s.max()-s.min()+1e-9))
        self.df["score"] = 0.6*self.df["usage_norm"] + 0.4*self.df["power_norm"]

    def recommend_for_user(self, user_id: str):
        sub = self.df[self.df["user_id"]==user_id]
        if sub.empty: return None
        top = sub.sort_values("score", ascending=False).iloc[0]
        app = top["appliance"]
        model = EFFICIENT_MODELS.get(app, f"{app} Efficient Model")
        est_kwh_saved = round(float(top["power_kwh"])*0.20,3)
        return {
            "user_id": user_id,
            "appliance": app,
            "current_power_kwh": float(top["power_kwh"]),
            "usage_count": int(top["usage_count"]),
            "score": float(top["score"]),
            "recommended_model": model,
            "estimated_kwh_saved_per_use": est_kwh_saved,
            "rationale": "Combines your usage frequency and appliance power draw to prioritize the highest-impact upgrade."
        }
