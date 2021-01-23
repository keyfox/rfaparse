import dataclasses
import functools
from datetime import timedelta
import re
from typing import Tuple, Callable, Any


@dataclasses.dataclass
class Region:
    # TODO: use tuple[float, float] instead in Python 3.9
    position: Tuple[float, float]
    size: Tuple[float, float]

    @staticmethod
    def product(a, b):
        return tuple((ea * eb for ea, eb in zip(a, b)))

    def cropargs(self, imgsize):
        imgsize = tuple(imgsize)
        position = self.product(self.position, imgsize)
        size = self.product(self.size, imgsize)
        return (*position, *(c + d for c, d in zip(position, size)))


def coords_to_ratios_720p(coords):
    return tuple(a / b for a, b in zip(coords, (1280, 720)))


def region_from_720p(position, size):
    return Region(coords_to_ratios_720p(position), coords_to_ratios_720p(size))


def row_region(y):
    return region_from_720p((584, y), (368, 64))


@dataclasses.dataclass
class OCRSubject:
    name: str
    region: Region
    parser: Callable[[Any], Any]


def extract_primary_text(func):
    @functools.wraps(func)
    def wrapper(vision_response):
        result = vision_response.text_annotations[0]
        primary_text = result.description.split("\n")[0].strip()
        return func(primary_text)

    return wrapper


@extract_primary_text
def duration_parser(text):
    # Parse text for "total time exercising" and return it as int in seconds.
    m = re.match(r"(?:(\d+)時間)?(\d{1,2})分(\d{1,2})秒", text)
    h, m, s = map(int, m.groups(default="0"))
    delta = timedelta(hours=h, minutes=m, seconds=s)
    return delta.seconds


@extract_primary_text
def calories_parser(text):
    # Parse text for "total calories burned" and return kilocalories as float.
    return float(text.rstrip("kcal"))


@extract_primary_text
def distance_parser(text):
    # Parse text for "total distance run" and return kilocalories as float.
    if text == "-":
        return 0
    return float(text.rstrip("km"))


# List of subjects.
SUBJECTS = [
    OCRSubject("time_exercising_seconds", row_region(274), duration_parser),
    OCRSubject("calories_burned_kcal", row_region(394), calories_parser),
    OCRSubject("distance_run_km", row_region(500), distance_parser),
]


RFARecord = dataclasses.make_dataclass(
    "RFARecord",
    (s.name for s in SUBJECTS),
    namespace={"asdict": lambda self: dataclasses.asdict(self)},
)
