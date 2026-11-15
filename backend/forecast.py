# backend/forecast


from pathlib import Path
import pandas as pd



DATA = Path(__file__).parent / "data"
Q = ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9"]

forecast_df = None
routes_df = None



def load():
    global forecast_df, routes_df
    forecast_df = pd.read_csv(DATA / "seasonal_forecast.csv")
    routes_df = pd.read_csv(DATA / "routes.csv")
    forecast_df["date"] = forecast_df["date"].astype(str)


def all_routes():
    return routes_df[["route", "name"]].to_dict("records")


def route_dates(route):
    rows = forecast_df[forecast_df["route"] == route]
    return sorted(rows["date"].unique().tolist())


def calc(route, date, price):
    frow = forecast_df[(forecast_df["route"] == route) & (forecast_df["date"] == date)]
    if frow.empty:
        return None
    
    # rows
    frow = frow.iloc[0]
    rrow = routes_df[routes_df["route"] == route].iloc[0]

    seats = int(frow["seats"])
    base_price = float(rrow["base_price"])
    sens = float(rrow["price_sensitivity"])
    rec_price = float(frow["0.5_price"])

    want = float(frow["0.5_base_demand"]) - sens * (price - base_price)
    buy = min(seats, max(0.0, want))

    chart = []
    for q in Q:
        q_want = float(frow[f"{q}_base_demand"]) - sens * (price - base_price)
        q_buy = min(seats, max(0.0, q_want))
        chart.append({"q": q, "want": round(q_want, 1), "buy": round(q_buy, 1)})


    return {"seats": seats, "want": round(want, 1), "buy": round(buy, 1), "rec_price": rec_price, "chart": chart}