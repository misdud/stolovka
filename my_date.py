from datetime import datetime

def my_current_datetame():

    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    now_data_time = now.strftime("%d-%m-%Y %H:%M:%S")
    return now_data_time
