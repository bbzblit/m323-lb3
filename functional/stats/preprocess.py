import datetime
from fpandas import FunctionalDF, FunctionalSeries


def get_all_trains(date: datetime.date) -> list[str]:
    df = FunctionalDF.from_csv(date)
    return df["LINIEN_TEXT"].toset()


def _line_to_string(start_serie: FunctionalSeries, end_serie: FunctionalSeries) -> str:
    start_time = datetime.datetime.strptime(
        start_serie["ABFAHRTSZEIT"], "%Y-%m-%d %H:%M:%S"
    )
    end_time = datetime.datetime.strptime(
        end_serie["ANKUNFTSZEIT"], "%Y-%m-%d %H:%M:%S"
    )
    start_station = start_serie["HALTESTELLEN_NAME"]
    end_station = end_serie["HALTESTELLEN_NAME"]
    return f"{start_time.strftime('%H:%M')} ({start_station}) -> {end_time.strftime('%H:%M')} ({end_station})"


def get_start_times(date: datetime.date, train_line: str) -> list[str]:
    df = FunctionalDF.from_csv(date)
    df = df.filter_content("LINIEN_TEXT", lambda x: x == train_line)
    end_df = df.filter_content("ABFAHRTSZEIT", lambda x: x == "")
    df = df.filter_content("ANKUNFTSZEIT", lambda x: x == "")
    times = [
        (
            row["ABFAHRTSZEIT"],
            _line_to_string(
                row, end_df.filter_content("FAHRT_ID", lambda x: x == row["FAHRT_ID"])[0]
            ),
        )
        for row in df.iterrows()
    ]
    return sorted(times)
