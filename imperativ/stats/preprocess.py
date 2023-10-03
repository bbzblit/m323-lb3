import datetime
import pandas as pd

def get_all_trains(date: datetime.date) -> list[str]:
    df = pd.read_csv(f"./data/{date.isoformat()}.csv")
    return df["LINIEN_TEXT"].unique().tolist() 