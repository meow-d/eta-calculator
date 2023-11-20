import argparse
from dotenv import load_dotenv
import configparser
from os import getenv

from datetime import datetime, timedelta

from bus_schdeule import get_next_bus
from maps import calculate_distance


def main():
    args = arguments()

    load_dotenv()
    api_key = getenv("BING_MAPS_API_KEY")

    config = configparser.ConfigParser()
    config.read("config.ini")

    # bus schedule
    eta, estimated_travel_time = get_next_bus(args.to_school)
    eta = update_and_print_eta(eta, estimated_travel_time, "Bus", update=False)

    # get ETA estimation from bing maps
    eta_seconds = calculate_distance(
        api_key,
        config["addresses"]["school"],
        config["addresses"]["school_station"],
        eta,
        "Driving",
    )
    eta = update_and_print_eta(eta, eta_seconds, "School bus to station")

    eta_seconds = calculate_distance(
        api_key,
        config["addresses"]["school_station"],
        config["addresses"]["home_station"],
        eta,
        "Transit",
    )
    eta = update_and_print_eta(eta, eta_seconds, "School station to home station")


def arguments():
    parser = argparse.ArgumentParser(
        prog="etacalculator",
        description="automatically calculates ETA based on APU bus schedule and Bing maps",
    )
    parser.add_argument(
        "-t",
        "--to-school",
        action="store_true",
        help="calculate ETA to school instead of from school",
    )
    return parser.parse_args()


def update_and_print_eta(eta, seconds: int, text: str, update=True):
    eta_timedelta = timedelta(seconds=seconds)
    if update:
        eta = eta + eta_timedelta
    print(
        f"{text}: {eta.strftime('%I:%M')}, {seconds//3600} hours {(seconds//60)%60} minutes and {seconds%60} seconds"
    )
    return eta


if __name__ == "__main__":
    main()
