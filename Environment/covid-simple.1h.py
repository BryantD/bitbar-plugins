#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3

# The MIT License (MIT)
#
# Copyright (c) 2020 Bryant Durrell
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# <bitbar.title>COVID-19 Tracker</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Bryant Durrell</bitbar.author>
# <bitbar.author.github>bdurrell</bitbar.author.github>
# <bitbar.desc>Shows corona virus data from https://covidtracking.com/</bitbar.desc>
# <bitbar.dependencies>python3, requests, pygal</bitbar.dependencies>
# <bitbar.image>XXX</bitbar.image>
# <bitbar.abouturl>XXX</bitbar.abouturl>

#### RATIONALE
# The other BitBar COVID-19 tracking plugins use up more menu bar real estate
# than I wanted. But they're perfectly decent plugins.

#### DEPENDENCIES
# This script requires python modules requests and pygal
# Install via pip:  `pip install requests pygal`

#### DATA
# This script retrieves data from the COVID Tracking Project API, available at:
# https://covidtracking.com/api
#
# GitHub: https://github.com/COVID19Tracking

#### CONFIGURATION
# Look for the configure() function. I'd do a config file but this is
# how BitBar rolls.

import requests
import csv
import pygal


def show_menubar():
    print(
        "| templateImage=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"
    )
    print("---")


def show_error(status_code):
    print(f"API error: {status_code}")


def show_data(stats):
    print(f"{stats}")


def get_state_data(api, state):

    r = requests.get(f"{api}/states/{state}/daily.csv")

    if r.status_code == 200:
        content = r.content.decode("utf-8")
        csv_reader = csv.DictReader(content.splitlines(), delimiter=",")
        csv_data = list(csv_reader)[:14]

        return r.status_code, csv_data

    else:
        return r.status_code, "[Failed]"


def format_data(daily_data, state, tracker_data):
    deaths_by_day = []
    for row in daily_data:
        deaths_by_day.append(int(row["deathIncrease"]))

    last_death_increase = daily_data[0]["deathIncrease"]
    last_date = daily_data[0]["date"]

    three_day_average = sum(deaths_by_day[0:3]) / 3

    if three_day_average > int(last_death_increase):
        color = "green"
    else:
        color = "red"

    death_chart = pygal.Line()
    death_chart.add("", deaths_by_day)
    death_sparkline = death_chart.render_sparktext()

    mb_text = f"{state} New Deaths on {last_date[0:4]}-{last_date[4:6]}-{last_date[6:8]}: {last_death_increase} | color={color}\n"
    mb_text += f"{state} 3 Day Average: {three_day_average:.2f} | color=black\n"
    mb_text += f"{state} 14 Day Graph: {death_sparkline} | color=black\n"
    mb_text += f"Data: {tracker_data['name']} | href='{tracker_data['credit_uri']}'"

    return mb_text


def configure():
    conf = {"state": "WA", "data_provider": "COVID_Tracking"}

    return conf


def main():
    trackers = {
        "COVID_Tracking": {
            "name": "COVID Tracking Project",
            "data_uri": "https://covidtracking.com/api/v1",
            "credit_uri": "https://covidtracking.com/",
        },
        "JHU": {
            "name": "JHU CSSE COVID-19 Data Repository",
            "data_uri": "https://github.com/CSSEGISandData/COVID-19",
            "credit_uri": "https://coronavirus.jhu.edu/",
        },
    }

    conf = configure()

    status_code, stats = get_state_data(
        trackers[conf["data_provider"]]["data_uri"], conf["state"]
    )
    if status_code == 200:
        show_data(format_data(stats, conf["state"], trackers[conf["data_provider"]]))
    else:
        show_error(status_code)


if __name__ == "__main__":
    main()

# date,state,positive,negative,pending,hospitalizedCurrently,hospitalizedCumulative,inIcuCurrently,inIcuCumulative,onVentilatorCurrently,onVentilatorCumulative,recovered,hash,dateChecked,death,hospitalized,total,totalTestResults,posNeg,fips,deathIncrease,hospitalizedIncrease,negativeIncrease,positiveIncrease,totalTestResultsIncrease
# 20200429,WA,13842,168673,,490,,156,,,,,af0bcc6ea3de117f946fdf97b697b4411aee928a,2020-04-29T20:00:00Z,786,,182515,182515,182515,53,21,0,2680,156,2836
# 20200428,WA,13686,165993,,436,,158,,,,,1a91d4a0c3ecebe8a321950c713fa1ea82dc7cdd,2020-04-28T20:00:00Z,765,,179679,179679,179679,53,16,0,4037,165,4202
