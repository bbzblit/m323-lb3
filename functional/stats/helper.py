from fpandas import FunctionalDF


def time_to_string(value: int) -> str:
    """
    Converts a time value in seconds to a string representation.

    Args:
        value (int): The time value in seconds.

    Returns:
        str: The string representation of the time value.
    """
    if value % 60 == 0:
        if value == 0:  
            return "No Delay"
        if value < 120:
            return f"[bright_yellow]{round(value // 60)} min[/bright_yellow]"
        elif value < 300:
            return f"[orange_red1]{round(value // 60)} min[/orange_red1]"
        return f"[bright_red]{round(value // 60)} min[/bright_red]"
    
    elif value < 60:
        return f"{round(value)} sec"
    
    if value < 120:
        return f"[bright_yellow]{round(value // 60)} min {round(value % 60)} sec[/bright_yellow]"
    elif value < 300:
        return f"[orange_red1]{round(value // 60)} min {round(value % 60)} sec[/orange_red1]"    
    return f"[bright_red]{round(value // 60)} min {round(value % 60)} sec[/bright_red]"
    

def remove_negative_delay(df: FunctionalDF) -> FunctionalDF:
    """
    Removes negative values from the 'DELAY_ANKUFT' column of the given FunctionalDF object.

    Args:
        df (FunctionalDF): The FunctionalDF object to remove negative values from.

    Returns:
        FunctionalDF: The updated FunctionalDF object with negative values removed from the 'DELAY_ANKUFT' column.
    """
    df = df.cast("DELAY_ANKUFT", float, 0)
    return df.query_update("DELAY_ANKUFT", lambda x: x < 0 , 0)
