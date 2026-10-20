---
title: Python Dates and Times
slug: dates
summary: Create, format, parse and do arithmetic with dates using the datetime module.
minutes: 9
---
## Today and now

```python tryit
from datetime import date, datetime

print(date.today())        # e.g. 2026-10-20
print(datetime.now())      # date and time
```

The output changes every day. The rest of this lesson uses fixed dates so the results are the same for everyone.

## Making a date

```python tryit
from datetime import date, datetime

launch = date(2026, 3, 14)
print(launch)
print(launch.year, launch.month, launch.day)
print(launch.weekday())     # Monday is 0 ... Sunday is 6

meeting = datetime(2026, 3, 14, 9, 30)
print(meeting)
```

## Formatting with strftime()

`strftime()` turns a date into text using codes such as `%d` (day), `%m` (month), `%Y` (year), `%A` (weekday name) and `%B` (month name).

```python tryit
from datetime import datetime

moment = datetime(2026, 3, 14, 9, 30)
print(moment.strftime("%d/%m/%Y"))          # 14/03/2026
print(moment.strftime("%A %d %B %Y"))       # Saturday 14 March 2026
print(moment.strftime("%H:%M"))             # 09:30
print(f"{moment:%Y-%m-%d}")                 # works in f-strings too
```

## Reading text with strptime()

`strptime()` does the opposite: it reads text into a datetime, using the same codes.

```python tryit
from datetime import datetime

text = "25-12-2026 18:00"
party = datetime.strptime(text, "%d-%m-%Y %H:%M")
print(party.year, party.hour)
```

## Date arithmetic with timedelta

A `timedelta` is a length of time. Add it to a date, or subtract two dates to get one.

```python tryit
from datetime import date, timedelta

start = date(2026, 1, 15)
print(start + timedelta(days=30))           # 2026-02-14
print(start - timedelta(weeks=2))           # 2026-01-01

exam = date(2026, 6, 1)
left = exam - start
print(left.days, "days to study")
```

## Comparing dates

```python tryit
from datetime import date

deadline = date(2026, 5, 31)
submitted = date(2026, 6, 2)
if submitted > deadline:
    print(f"Late by {(submitted - deadline).days} days")
```

## Summary

- `date(y, m, d)` and `datetime(y, m, d, h, min)` create values.
- `strftime()` formats, `strptime()` parses, with codes like `%d %m %Y %H %M`.
- `timedelta(days=...)` adds or subtracts time; subtracting dates gives a `timedelta`.

```exercise
{
  "title": "Days until the trip",
  "prompt_md": "Read the two dates from text with `strptime()` and print how many days are between them. The output must be `48`.",
  "starter_code": "from datetime import datetime\n\ntoday = \"2026-10-20\"\ntrip = \"2026-12-07\"\n",
  "solution_code": "from datetime import datetime\n\ntoday = \"2026-10-20\"\ntrip = \"2026-12-07\"\na = datetime.strptime(today, \"%Y-%m-%d\")\nb = datetime.strptime(trip, \"%Y-%m-%d\")\nprint((b - a).days)",
  "check_type": "output",
  "expected_value": "48",
  "hint": "The format is \"%Y-%m-%d\". Subtract the two datetimes and use .days."
}
```

```quiz
[
  {"question": "Which method turns a date into text?", "options": ["strptime()", "strftime()", "str_date()"], "answer": 1, "explanation": "strftime = string format time."},
  {"question": "What is date(2026, 1, 31) + timedelta(days=1)?", "options": ["2026-01-32", "2026-02-01", "an error"], "answer": 1, "explanation": "timedelta handles month ends for you."},
  {"question": "Which code means the 4-digit year?", "options": ["%y", "%Y", "%D"], "answer": 1, "explanation": "%Y is 2026; %y would be 26."}
]
```
