def time_to_string(value: int) -> str:
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
    