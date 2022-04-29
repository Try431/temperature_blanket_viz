# Temperature Blanket Visualizer

Just something I threw together on a whim. Grabs temperature data for a specified zip code over a date range, and will construct a basic HTML 
"blanket" of layered colors based on a list of desired colors.

The code will by default use the daily high temperature for the color generation.

## Requirements/Setup

### For ALL users
Get a Weather API key by signing up at https://www.visualcrossing.com/sign-up (it's free). Once you've signed up, you can view it on your Account Details page.

*Inside the `temp_blanket_viz.py` code itself, there are variables for setting your weather API key (see above), your zip code, the desired colors (in hex format), and your start/end dates for the historical data you want to grab. You must edit these variables for the code to run.*


### For Linux systems

To install local dependencies:
```
$ python -m venv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```


### For Windows

I'm going to assume that if you're reading this section, you have nothing set up.

1. Download this repo code as a .zip file and extract it to a folder
2. Go to the Microsoft Store, search for "Python", and install Python 3.10 or higher
3. Open up the Command Prompt (you can do this by entering `cmd` in the Windows search bar)
4. Navigate to the folder you extracted the code to 
    -  (e.g., if I extracted the code within my Documents folder, I would enter `cd C:Documents\temperature_blanket_viz-master\`
5. Set up a virtual environment by entering `python -m venv env` inside the Command Prompt
6. Enter into the virtual environment by entering `.\env\Scripts\activate`
7. Install the required dependencies by entering `pip install -r requirements.txt`

You are now fully set up to run the code! Don't forget to edit the necessary variables if you haven't already - see above!

## Running

### For Linux systems
```
$ python temp_blanket_viz.py           # defaults to high
$ python temp_blanket_viz.py high      # use daily highs
$ python temp_blanket_viz.py low       # use daily lows
$ python temp_blanket_viz.py both      # layer in both
```

### For Windows

If you haven't already, follow steps #3 through #7 above - then, all you need to do is enter one of the following:
```
$ python temp_blanket_viz.py           # defaults to high
$ python temp_blanket_viz.py high      # use daily highs
$ python temp_blanket_viz.py low       # use daily lows
$ python temp_blanket_viz.py both      # layer in both
```

You will see that a file called `color.html` will pop up in your directory. This file will change depending on whether you input `high`, `low`, or `both`. You can run the code as many times as you want, changing the colors and inputs as you desire, but do note the API limits described below if you decide to change locations and want to get new temperature JSON data.

## Viewing

Just load the generated `color.html` in any browser of your choice.


# Notes

## Weather API

Weather History API docs: https://www.visualcrossing.com/resources/documentation/weather-api/weather-api-documentation/#history

*Do note that there's a limit of 1000 records being requested per day - meaning that you can only make two queries for a full-year's worth of data per day, at least with the free tier*

*This is why the data is written to a local JSON file and the API is called only if that JSON file doesn't exist.*
