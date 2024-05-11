import re
from csv import DictReader as CSVDictReader
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import Dict, Generator, List, Set

from gpx import GPX, Latitude, Longitude, Track, TrackSegment, Waypoint

RE_POINT = re.compile(
    r"\((?P<latitude>[-+]?[0-9]*\.?[0-9]*)"
    r", (?P<longitude>[-+]?[0-9]*\.?[0-9]*)\)"
)


def transform_latitude(value: str) -> Latitude:
    """
    Transform the geo value to a Decimal.
    """
    return Latitude(value).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)  # type: ignore


def transform_longitude(value: str) -> Longitude:
    """
    Transform the geo value to a Decimal.
    """
    return Longitude(value).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)  # type: ignore


def remove_duplicate_visits(
    list_of_dicts: List[Dict[str, str]],
) -> Generator[Dict[str, str], None, None]:
    """
    Remove duplicate visits from the list of visits.
    """
    seen: Set[str] = set()
    for visit in list_of_dicts:
        unique_str = "::".join(
            [
                visit["Name"],
                str(transform_latitude(visit["Latitude"])),
                str(transform_longitude(visit["Longitude"])),
            ]
        )
        if unique_str not in seen:
            seen.add(unique_str)
            yield visit


def process_visit_to_waypoint(visit: Dict[str, str]) -> Waypoint:
    """
    Process the visits data and return a Waypoint object.
    """
    waypoint = Waypoint()
    waypoint.name = visit["Name"]
    waypoint.lat = transform_latitude(visit["Latitude"])
    waypoint.lon = transform_longitude(visit["Longitude"])
    waypoint.time = datetime.fromisoformat(visit["Start Time"]).replace(
        tzinfo=timezone.utc
    )
    waypoint.src = visit["Service"]
    return waypoint


def process_travel_point_to_track_segment(points: str) -> TrackSegment:
    """
    Process the travel points data and return a TrackSegment object.
    """
    track_segment = TrackSegment()
    for latitude, longitude in RE_POINT.findall(points):
        waypoint = Waypoint()
        waypoint.lat = transform_latitude(latitude)
        waypoint.lon = transform_longitude(longitude)
        track_segment.trkpts.append(waypoint)

    return track_segment


def process_travel_to_track(travel: Dict[str, str]) -> Track:
    """
    Process the travels data and add it to the GPX object.
    """
    track = Track()
    track.type = travel["Type"]
    track.src = travel["Service"]
    track.trksegs = [
        process_travel_point_to_track_segment(travel["Points"]),
    ]
    return track


def gyroscope_to_gpx(
    visits_csv_path: Path,
    travels_csv_path: Path,
    output_gpx_path: Path,
):
    # Read the visits CSV file
    with visits_csv_path.open("r") as visits_csv_file_obj:
        visits_csv_obj = CSVDictReader(visits_csv_file_obj)
        visits = list(visits_csv_obj)

    # Read the travels CSV file
    with travels_csv_path.open("r") as travels_csv_file_obj:
        travels_csv_obj = CSVDictReader(travels_csv_file_obj)
        travels = list(travels_csv_obj)

    gpx = GPX()
    gpx.creator = "gyroscope-to-gpx"

    # Process the visits data and add it to the GPX object as waypoints.
    for visit in remove_duplicate_visits(visits):
        gpx.waypoints.append(process_visit_to_waypoint(visit))

    # Process the travels data and add it to the GPX object as tracks.
    for travel in travels:
        gpx.tracks.append(process_travel_to_track(travel))

    gpx.to_file(output_gpx_path)
