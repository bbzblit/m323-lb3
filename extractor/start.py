from pandas import DataFrame
import pandas as pd
import numpy as np
import os


def modify_df(df: DataFrame) -> DataFrame:
    df["FAHRT_ID"] = df["FAHRT_BEZEICHNER"]
    df = df.drop(
        [
            "BETRIEBSTAG",
            "BETREIBER_ID",
            "BETREIBER_ABK",
            "FAHRT_BEZEICHNER",
            "BETREIBER_NAME",
            "LINIEN_ID",
            "VERKEHRSMITTEL_TEXT",
            "AB_PROGNOSE_STATUS",
            "AN_PROGNOSE_STATUS",
            "ZUSATZFAHRT_TF",
            "BPUIC",
            "UMLAUF_ID",
            "DURCHFAHRT_TF",
        ],
        axis=1,
    )

    df = df[df["PRODUKT_ID"] == "Zug"]
    
    fail_ids = df[df["FAELLT_AUS_TF"]]["FAHRT_ID"].unique().tolist()
    
    df = df[~df["FAHRT_ID"].isin(fail_ids)]
    
    ids = df["FAHRT_ID"].unique().tolist()

    for id in ids:
        line = df[df["FAHRT_ID"] == id]
        
        start = line[line["ANKUNFTSZEIT"].isna()]
        end = line[line["ABFAHRTSZEIT"].isna()]

        if len(start) == 0 or len(end) == 0:
            df = df[df["FAHRT_ID"] != id]

    df = df.drop(["FAELLT_AUS_TF", "PRODUKT_ID"], axis=1)
    df.replace("", np.nan, inplace=True)

    for time_col in ["ANKUNFTSZEIT", "ABFAHRTSZEIT"]:
        df[time_col] = pd.to_datetime(df[time_col], format="%d.%m.%Y %H:%M")

    for time_col in ["AN_PROGNOSE", "AB_PROGNOSE"]:
        df[time_col] = pd.to_datetime(df[time_col], format="%d.%m.%Y %H:%M:%S")

    df["AN_PROGNOSE"] = df["AN_PROGNOSE"].fillna(df["ANKUNFTSZEIT"])
    df["AB_PROGNOSE"] = df["AB_PROGNOSE"].fillna(df["ABFAHRTSZEIT"])

    df["DELAY_ANKUFT"] = (df["AN_PROGNOSE"] - df["ANKUNFTSZEIT"]).astype(
        "timedelta64[s]"
    )
    df["DELAY_ABFAHRT"] = (df["AB_PROGNOSE"] - df["ABFAHRTSZEIT"]).astype(
        "timedelta64[s]"
    )

    df["DELAY_ANKUFT"] = df["DELAY_ANKUFT"] / pd.Timedelta(seconds=1)
    df["DELAY_ABFAHRT"] = df["DELAY_ABFAHRT"] / pd.Timedelta(seconds=1)

    df = df[
        df["DELAY_ABFAHRT"].between(-10, 300)
        | df["DELAY_ANKUFT"].between(-10, 300)
        | df["DELAY_ABFAHRT"].isna()
        | df["DELAY_ANKUFT"].isna()
    ]

    df = df.dropna(subset=["HALTESTELLEN_NAME"])


    return df


def list_files(dir: str = "./data"):
    for path, subdirs, files in os.walk(dir):
        for name in files:
            yield os.path.join(path, name)


def main():
    for file in list_files():
        df = pd.read_csv(file, engine="pyarrow", encoding="utf-8", delimiter=";")
        df = modify_df(df)
        df.to_csv(
            f"out/{file.rsplit('/', maxsplit=1)[-1].rsplit('_', maxsplit=1)[0]}.csv"
        )


if __name__ == "__main__":
    main()
