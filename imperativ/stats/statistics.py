from datetime import date, datetime
import pandas as pd


def get_statistics_of_train(date: date, train: str):
    df = pd.read_csv(f"./data/{date.isoformat()}.csv")
    df = df[(df == 0).all(1)]
    df = df[df["LINIEN_TEXT"] == train]
    df = df[df["DELAY_ABFAHRT"].isna()]
    
    df[df["DELAY_ANKUFT"] < 0].loc[:, "DELAY_ANKUFT"] = 0
    df[df["DELAY_ABFAHRT"] < 0].loc[:, "DELAY_ABFAHRT"] = 0
    
    stops = df["HALTESTELLEN_NAME"].unique().tolist()

    return {
        "Minimum": df["DELAY_ANKUFT"].min(),
        "Maximum": df["DELAY_ANKUFT"].max(),
        "Average": df["DELAY_ANKUFT"].mean(),
        "Median": df["DELAY_ANKUFT"].median(),
        "meta": {
            "Rides": len(df),
            "Train": train,
            "Date": date,
            "Endstations": stops,
        }
    }

def get_delay_of_exact_connection(date: date, train_line: str, time: str):
    df = pd.read_csv(f"./data/{date.isoformat()}.csv")
    df = df[df["LINIEN_TEXT"] == train_line]
    fahrt_id = df[df["ABFAHRTSZEIT"] == time].iloc[0]["FAHRT_ID"]
    df = df[df["FAHRT_ID"] == fahrt_id]

    df[df["DELAY_ANKUFT"] < 0].loc[:, "DELAY_ANKUFT"] = 0
    df[df["DELAY_ABFAHRT"] < 0].loc[:, "DELAY_ABFAHRT"] = 0

    return {
        "meta":  {
            "Train": train_line,
            "Date": date,
            "Time": time,
            "Stops": df["HALTESTELLEN_NAME"].unique().tolist()
        },
        "Median Delay": df["DELAY_ANKUFT"].mean(),
        "Maximum Delay": df["DELAY_ANKUFT"].max(),
        "Minimum Delay": df["DELAY_ANKUFT"].min(),
        "Average Delay": df["DELAY_ANKUFT"].mean(),
        "Delay at Beginning": df[df["ANKUNFTSZEIT"].isna()].iloc[0]["DELAY_ABFAHRT"],
    }