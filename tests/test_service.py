from decimal import Decimal

import pytest

from gyroscope_to_gpx import service


@pytest.mark.parametrize(
    "string, expected_result",
    (
        pytest.param(
            "(40.748440, -73.984559)",
            [("40.748440", "-73.984559")],
            id="one_point",
        ),
        pytest.param(
            "(40.748440, -73.984559),(40.748440, -73.984559)",
            [("40.748440", "-73.984559"), ("40.748440", "-73.984559")],
            id="two_points",
        ),
        pytest.param(
            "(40.748440, -73.984559),(40.748440, -73.984559),(40.748440, -73.984559)",
            [
                ("40.748440", "-73.984559"),
                ("40.748440", "-73.984559"),
                ("40.748440", "-73.984559"),
            ],
            id="three_points",
        ),
    ),
)
def test_re_point(string, expected_result):
    result = service.RE_POINT.findall(string)
    assert result == expected_result


def test_process_travel_point_to_track_segment():
    points = "(40.748440, -73.984559)"
    segment = service.process_travel_point_to_track_segment(points)

    assert len(segment.trkpts) == 1
    assert segment.trkpts[0].lat == Decimal("40.748440")
    assert segment.trkpts[0].lon == Decimal("-73.984559")
