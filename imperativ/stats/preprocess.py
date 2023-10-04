import datetime
import pandas as pd


def get_all_trains(date: datetime.date) -> list[str]:
    df = pd.read_csv(f"./data/{date.isoformat()}.csv")
    return df["LINIEN_TEXT"].unique().tolist()


def get_start_times(date: datetime.date, train_line: str) -> list[str]:
    df = pd.read_csv(f"./data/{date.isoformat()}.csv")
    df = df[df["LINIEN_TEXT"] == train_line]
    df = df[df["ANKUNFTSZEIT"].isna()]
    times = []
    for index, row in df.iterrows():
        start_time = datetime.datetime.strptime(
            row["ABFAHRTSZEIT"], "%Y-%m-%d %H:%M:%S"
        )
        times.append(
            (row["ABFAHRTSZEIT"], f"{start_time.strftime('%H:%M')} - {row['HALTESTELLEN_NAME']}")
        )
    return sorted(times)
