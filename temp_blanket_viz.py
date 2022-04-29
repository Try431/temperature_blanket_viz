import requests
import json
import pandas as pd
import sys

from os.path import exists

from pprint import pprint

WEATHER_API_KEY = "INSERT_YOUR_API_KEY_HERE"
START_DATE = "2021-01-01"
END_DATE = "2021-12-31"

ZIP_CODE = "INSERT_YOUR_ZIP_CODE_HERE"

WEATHER_ENDPOINT = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{ZIP_CODE}/{START_DATE}/{END_DATE}?unitGroup=us&elements=datetime%2Ctempmax%2Ctempmin%2Ctemp&include=days&key={WEATHER_API_KEY}&contentType=json"

# note - lower indices will correspond to lower temperatures
DESIRED_COLORS = ["#F700FF",
                  "#C383FF",
                  "#7C74FF",
                  "#0059FF",
                  "#00E4FF",
                  "#85FDBD",
                  "#19FF06",
                  "#FFE506",
                  "#FFAC06",
                  "#DE0000",
                  "#5C0000"]

NUM_COLORS_WANTED = len(DESIRED_COLORS)


def write_weather_data_to_file():
    resp = requests.get(WEATHER_ENDPOINT)
    print(resp.status_code)
    data = json.loads(resp.text)
    with open("./temp_data.json", "w") as f:
        json.dump(data, f)


def generate_temp_bins(temp_data):
    min_temp, max_temp = min(temp_data), max(temp_data)
    diff = max_temp - min_temp
    even_split = diff / NUM_COLORS_WANTED
    bins = []
    # slightly decreasing the first lower bin value so that our min_temp will fall within the bucket,
    # because the df buckets are (low, high]
    bins.append(round(min_temp - 0.1, 1))
    for i in range(1, NUM_COLORS_WANTED + 1):
        bin_val = round(min_temp + i * even_split, 1)
        bins.append(bin_val)
    return bins


def create_color_mapping():
    high_temp_days, low_temp_days = [], []
    file_data = None
    with open("./temp_data.json") as f:
        file_data = json.load(f)

    list_of_days = file_data.get("days")
    for day in list_of_days:
        high_temp_days.append(day.get("tempmax"))
        low_temp_days.append(day.get("tempmin"))

    color_mapping = {}
    for day_data in list_of_days:
        color_mapping[day_data.get("datetime")] = {"high_color": None, "low_color": None}

    # mapping high temperature data
    high_temp_bins = generate_temp_bins(high_temp_days)

    high_temp_df = pd.DataFrame(data=high_temp_days, columns=["data"])
    high_temp_df["bucket"] = pd.cut(high_temp_df.data, high_temp_bins)

    for i, val in enumerate(high_temp_df.get("bucket")):
        color_num = high_temp_bins.index(val.left)
        day = list_of_days[i].get("datetime")
        color_mapping[day]["high_color"] = color_num

    # mapping low temperature data
    low_temp_bins = generate_temp_bins(low_temp_days)

    low_temp_df = pd.DataFrame(data=low_temp_days, columns=["data"])
    low_temp_df["bucket"] = pd.cut(low_temp_df.data, low_temp_bins)

    for i, val in enumerate(low_temp_df.get("bucket")):
        color_num = low_temp_bins.index(val.left)
        day = list_of_days[i].get("datetime")
        color_mapping[day]["low_color"] = color_num

    return color_mapping


def visualize_color_pattern(color_mapping, viz_param):
    # pprint(color_mapping)

    with open("color.html", "w") as f:
        f.write("<html>\n")
        for day in sorted(color_mapping.keys()):
            high_color_ind = color_mapping.get(day).get("high_color")
            high_color = DESIRED_COLORS[high_color_ind]
            low_color_ind = color_mapping.get(day).get("low_color")
            low_color = DESIRED_COLORS[low_color_ind]
            high_color_rect = f'<rect width="1600" height="20" style="fill:{high_color}" />\n'
            low_color_rect = f'<rect width="1600" height="20" style="fill:{low_color}" />\n'
            if viz_param in ["high", "both"]:
                f.write('<svg width="1600" height="20">\n')
                f.write(f"{day} HIGH -- {high_color_rect}")
                f.write("</svg>\n")
            if viz_param in ["low", "both"]:
                f.write('<svg width="1600" height="20">\n')
                f.write(f"{day} LOW -- {low_color_rect}")
                f.write("</svg>\n")

        f.write("</html>")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        viz_param = sys.argv[1]
    if not exists("./temp_data.json"):
        write_weather_data_to_file()
    color_mapping = create_color_mapping()
    visualize_color_pattern(color_mapping, viz_param)
