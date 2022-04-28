# Temperature Blanket Visualizer

Just something I threw together on a whim. Grabs temperature data for a specified zip code over a date range, and will construct a basic HTML 
"blanket" of layered colors based on a list of desired colors.

The code will by default use the daily high temperature for the color generation.

## Requirements/Setup

To install local dependencies:
```
$ python -m venv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

Inside the `temp_blanket_viz.py` code itself, there are variables for setting your weather API key (see Notes), your zip code, the desired colors (in hex format), and your start/end dates for the historical data you want to grab.

## Running

```
$ python temp_blanket_viz.py           # defaults to high
$ python temp_blanket_viz.py high      # use daily highs
$ python temp_blanket_viz.py low       # use daily lows
$ python temp_blanket_viz.py both      # layer in both
```

## Viewing

Just load the generated `color.html` in any browser of your choice.


# Notes

## Weather API

Get a Weather API key by signing up at https://www.visualcrossing.com/sign-up (it's free)

Weather History API docs: https://www.visualcrossing.com/resources/documentation/weather-api/weather-api-documentation/#history

*Do note that there's a limit of 1000 records being requested per day, which is why the data is written to a local JSON file and the API is called only if that JSON file doesn't exist*