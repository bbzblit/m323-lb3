import datetime
import pandas as pd


def get_all_trains(date: datetime.date) -> list[str]:
    df = pd.read_csv(f"./data/{date.isoformat()}.csv")
    return df["LINIEN_TEXT"].unique().tolist()


def get_start_times(date: datetime.date, train_line: str) -> list[str]:
    df = pd.read_csv(f"./data/{date.isoformat()}.csv")
    df = df[df["LINIEN_TEXT"] == train_line]
    end_df = df[df["ABFAHRTSZEIT"].isna()]
    df = df[df["ANKUNFTSZEIT"].isna()]
    times = []
    for index, row in df.iterrows():
        start_time = datetime.datetime.strptime(
            row["ABFAHRTSZEIT"], "%Y-%m-%d %H:%M:%S"
        )

        endstation = row["HALTESTELLEN_NAME"]
        end_serie = end_df[end_df["FAHRT_ID"] == row["FAHRT_ID"]].iloc[0]
        beginstation = end_serie["HALTESTELLEN_NAME"]

        end_time = datetime.datetime.strptime(
            end_serie["ANKUNFTSZEIT"], "%Y-%m-%d %H:%M:%S"
        )

        times.append(
            (
                row["ABFAHRTSZEIT"],
                f"{start_time.strftime('%H:%M')} ({beginstation}) -> {end_time.strftime('%H:%M')} ({endstation})",
            )
        )
    return sorted(times)
