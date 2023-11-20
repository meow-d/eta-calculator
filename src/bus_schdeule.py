from io import open
from datetime import datetime, date


def get_next_bus(to_school):
    if to_school:
        schedule_path = "./bus_schedule/to.txt"
    else:
        schedule_path = "./bus_schedule/from.txt"
    schedule = parse_schedule(schedule_path)

    current_time = datetime.now().time()
    next_bus_time = time_nearest(schedule, current_time)
    next_bus_datetime = datetime.combine(date.today(), next_bus_time)

    bus_time_difference = round(
        time_difference(current_time, next_bus_time).total_seconds() / 60
    )

    return next_bus_datetime, bus_time_difference


def parse_schedule(file_path):
    with open(file_path, "r") as f:
        f_text = f.read()
        schedule = f_text.strip().split("\n")
        schedule = convert_string_to_time_bulk(schedule)
    return schedule


def convert_string_to_time_bulk(time_list):
    out = []
    for time_string in time_list:
        time_converted = datetime.strptime(time_string, "%H:%M").time()
        out.append(time_converted)
    return out


def time_nearest(items, pivot):
    nearest = min(
        [i for i in items if i >= pivot], key=lambda x: abs(time_difference(x, pivot))
    )
    return nearest


def time_difference(time_a, time_b):
    datetime_a = datetime.combine(date.today(), time_a)
    datetime_b = datetime.combine(date.today(), time_b)
    return datetime_b - datetime_a
