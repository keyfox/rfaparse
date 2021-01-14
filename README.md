# rfaparse

## Installation

```bash
pip3 install git+https://github.com/keyfox/rfaparse
```

## Requirements

  - Python 3.8+
  - Google Cloud Platform account with Cloud Vision API enabled
    - Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

## Python script usage

Call `parse_summary_screen` function with path of an image file, file-like object, or whatever Pillow's `Image.open` accepts.
The function returns `RFARecord` instance.

```python
from rfaparse import parse_summary_screen

summary = parse_summary_screen("./screenshot.jpg")

# integer, "total time exercising" value in seconds.
print(summary.time_exercising_seconds)
# float, "total calories burnt" value in kilocalories.
print(summary.calories_burnt_kcal)
# float, "total distance run" value in kilometers.
print(summary.distance_run_km)

in_case_you_need_dict = summary.asdict()
```

## Commandline usage

```bash
rfaparse ./screenshot.jpg
```

The command above is equivalent to the following Python script:

```python
print(json.dumps(parse_summary_screen("./screenshot.jpg").asdict()))
```

