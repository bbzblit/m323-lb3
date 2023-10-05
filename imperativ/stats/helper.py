def time_to_string(value: int) -> str:
    if value % 60 == 0:
        if value == 0:  
            return "No Delay"
        return f"{round(value // 60)} min"
    
    elif value < 60:
        return f"{round(value)} sec"
    
    return f"{round(value // 60)} min {round(value % 60)} sec"
