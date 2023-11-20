import requests


def calculate_distance(
    api_key, origin, destination, start_time, travel_mode="Driving"
) -> int:
    api_url = "https://dev.virtualearth.net/REST/v1/Routes/Transit"
    params = {
        "key": api_key,
        "waypoint.1": origin,
        "waypoint.2": destination,
        "travelMode": travel_mode,
        "dateTime": start_time,
        "timeType": "Departure",
        "routeAttributes": "transitStops",
        # "routeAttributes": "routeSummariesOnly",
    }

    http_result = requests.get(api_url, params=params)

    seconds = int(http_result["resourceSets"][0]["resources"][0]["travelDuration"])  # type: ignore
    return seconds
