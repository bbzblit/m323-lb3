from datetime import date
from .helper import time_to_string, remove_negative_delay
from fpandas import FunctionalDF


def get_statistics_of_train(date: date, train: str):
    """
    Returns a dictionary containing statistics of a train's delay for a given date.

    Args:
    - date (date): The date for which the statistics are to be calculated.
    - train (str): The name of the train for which the statistics are to be calculated.

    Returns:
    - A dictionary containing the following keys:
        - "Meta Informations": A dictionary containing meta information about the train and date.
        - "Delay Statistics": A dictionary containing delay statistics of the train for the given date.
    """

    df = FunctionalDF.from_csv(date)
    df = df.filter_content("LINIEN_TEXT", lambda x: x == train)
    df = df.filter_content("DELAY_ABFAHRT", lambda x: x == "")
    df = remove_negative_delay(df)

    stops = df["HALTESTELLEN_NAME"].toset()

    return {
        "Meta Informations": {
            "Rides": len(df),
            "Train": train,
            "Date": date,
            "Endstations": ", ".join(stops),
        },
        "Delay Statistics": {
            "Minimum Delay": time_to_string(df["DELAY_ANKUFT"].min()),
            "Maximum Delay": time_to_string(df["DELAY_ANKUFT"].max()),
            "Average Delay": time_to_string(df["DELAY_ANKUFT"].mean()),
            "Median Delay": time_to_string(df["DELAY_ANKUFT"].median()),
        },
    }
    

def get_delay_of_exact_connection(date: date, train_line: str, time: str):
    """
    Returns delay statistics and delay per stop for a specific train connection at a specific time.

    Args:
        date (date): The date of the train connection.
        train_line (str): The name of the train line.
        time (str): The departure time of the train.

    Returns:
        dict: A dictionary containing the delay statistics and delay per stop for the specified train connection.
    """

    df = FunctionalDF.from_csv(date)
    
    df = df.filter_content("LINIEN_TEXT", lambda x: x == train_line)
    fahrt_id = df.filter_content("ABFAHRTSZEIT", lambda x: x == time)[0]["FAHRT_ID"]
    df = df.filter_content("FAHRT_ID", lambda x: x == fahrt_id)
    stops = df["HALTESTELLEN_NAME"]
    df = remove_negative_delay(df)

    delay_per_stop = {
            stop: time_to_string(delay)
            for stop, delay in zip(stops, [float(df["DELAY_ABFAHRT"][0])] + df["DELAY_ANKUFT"].tolist()[1:])
    }

    return {
        "Meta Informations": {
            "Train": train_line,
            "Start Time": time,
            "End Time": df["ANKUNFTSZEIT"][-1],
            "Stops": " -> ".join(stops),
        },
        "Delay Statistics": {
            "Minimum Delay": time_to_string(df["DELAY_ANKUFT"].min()),
            "Maximum Delay": time_to_string(df["DELAY_ANKUFT"].max()),
            "Average Delay": time_to_string(df["DELAY_ANKUFT"].mean()),
            "Median Delay": time_to_string(df["DELAY_ANKUFT"].median()),
        },
        "Delay per Stop": delay_per_stop,
    }

def get_statistics_of_day(date: date):
    """
    Returns a dictionary containing delay statistics for a given date.

    Args:
        date (date): The date for which to retrieve delay statistics.

    Returns:
        dict: A dictionary containing delay statistics for the given date.
            The dictionary has two keys:
                - "Meta Informations": A dictionary containing meta information about the statistics.
                - "Delay Statistics": A dictionary containing the delay statistics.
            The "Meta Informations" dictionary has one key:
                - "Date": The date for which the statistics were retrieved.
            The "Delay Statistics" dictionary has four keys:
                - "Minimum Delay": The minimum delay for the given date.
                - "Maximum Delay": The maximum delay for the given date, along with the train(s) that experienced the delay.
                - "Average Delay": The average delay for the given date.
                - "Median Delay": The median delay for the given date.
    """

    df = FunctionalDF.from_csv(date)
    df = df.filter_content("DELAY_ANKUFT", lambda x: x != "")
    df = remove_negative_delay(df)
    delays = df["DELAY_ANKUFT"]
    maximum = delays.max()

    maximum = f"{time_to_string(maximum)} (Train: {', '.join(df.filter_content('DELAY_ANKUFT', lambda x: x == maximum)['LINIEN_TEXT'].tolist())})"
    return {
        "Meta Informations": {
            "Date": date,
        },
        "Delay Statistics": {
            "Minimum Delay": time_to_string(delays.min()),
            "Maximum Delay": maximum,
            "Average Delay": time_to_string(delays.mean()),
            "Median Delay": time_to_string(delays.median()),
        },
    }
