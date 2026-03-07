from datetime import datetime, timedelta

def next4weekends():
    '''
    returns the 4 next weekends as d.m.y strings
    '''
    d = datetime.today()
    d_of_month = d.day
    d_of_week = d.weekday()

    t = timedelta((11 - d_of_week) % 7) # days to friday

    next_weekend_begin = d + t
    next_weekend_end = next_weekend_begin + timedelta(days=2)

    next_weekend={
        "begin": next_weekend_begin.strftime("%d.%m.%Y"),
        "end": next_weekend_end.strftime("%d.%m.%Y")
    }


    weekends = [next_weekend]
    for i in range(0, 3):
        next_weekend_begin = next_weekend_begin + timedelta(days=7)
        next_weekend_end = next_weekend_end + timedelta(days=7)

        next_weekend={
            "begin": next_weekend_begin.strftime("%d.%m.%Y"),
            "end": next_weekend_end.strftime("%d.%m.%Y")
        }
        weekends.append(next_weekend)

    return weekends
    
def str2hour(string):
    str_format="%H:%M"
    return datetime.strptime(string, str_format)

def weekend_str2date(string):
    str_format="%d.%m.%Y"
    return datetime.strptime(string, str_format)

def plus1day():
    return timedelta(days=1)

def timedif(date1, date2):
    return int((date2 - date1).total_seconds() // 60)

def final_dates(weekend, departure_list, comeback_list, i, j):
    date1 = datetime.combine(
        weekend_str2date(weekend["begin"]), 
        departure_list[i]["arrival"].time()
    )
    if departure_list[i]["next_day_arr"]:
        date1 = date1 + plus1day()

    date2 = datetime.combine(
        weekend_str2date(weekend["end"]), 
        comeback_list[j]["departure"].time()
    )

    return date1, date2