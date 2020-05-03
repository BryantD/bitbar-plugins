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
# <bitbar.author.github>BryantD</bitbar.author.github>
# <bitbar.desc>Shows COVID-19 data from the usual sources</bitbar.desc>
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
# This script retrieves data from:
# The COVID Tracking Project API, available at:
#   https://covidtracking.com/api / https://github.com/COVID19Tracking
#
# The JHU CSSE COVID-19 Data Repository, available at:
#   https://github.com/CSSEGISandData/COVID-19

#### CONFIGURATION
# Look for the configure() function. I'd do a config file but this is
# how BitBar rolls.

import requests
import csv
import pygal


def configure():
    # data_provider: 
    #   COVID_Tracking or JHU
    # states:
    #   use abbreviations for COVID_Tracking
    #   use the full state name for JHU
    # countries:
    #   use "US" or nothing for COVID_Tracking (no other country data is available)
    #   use the full country name for JHU (check their data repo for spellings as needed)

    # edit this
    conf = {
        "states": ["WA", "MA"],
        "countries": ["US"],
        "data_provider": "COVID_Tracking",
    }
    
    # don't touch this
    conf['trackers'] = {
        "COVID_Tracking": {
            "name": "COVID Tracking Project",
            "abbr": "ctp",
            "data_uri": "https://covidtracking.com/api/v1",
            "credit_uri": "https://covidtracking.com/",
        },
        "JHU": {
            "name": "JHU CSSE COVID-19 Data Repository",
            "abbr": "jhu",
            "data_uri": "https://github.com/CSSEGISandData/COVID-19",
            "credit_uri": "https://coronavirus.jhu.edu/",
        },
    }

    return conf


def show_menubar():
    print(
        "| templateImage=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"
    )
    print("---")


def show_error(status_code):
    print(f"API error: {status_code}")


def show_data(stats):
    print(f"{stats}")


# Expected data returned by XXX_get_state_data functions:
# {
#   '2020-01-01': {
#       'death_increase': XXX,
#       'case_increase': XXX,
#   }
# }


def ctp_get_state_data(api, state):
    state_data = {}
    r = requests.get(f"{api}/states/{state}/daily.csv")

    if r.status_code == 200:
        content = r.content.decode("utf-8")
        csv_reader = csv.DictReader(content.splitlines(), delimiter=",")
        csv_data = list(csv_reader)[:14]

        for row in csv_data:
            date_stamp = f"{row['date'][0:4]}-{row['date'][4:6]}-{row['date'][6:8]}"
            state_data[date_stamp] = {
                "death_increase": row["deathIncrease"],
                "case_increase": row["positiveIncrease"],
            }

        return r.status_code, state_data

    else:
        return r.status_code, "[Failed]"


def ctp_get_country_data(api):

    return r.status_code, csv_data


def format_state_data(daily_data, state):
    deaths_by_day = []
    cases_by_day = []
    
    good_color = "green"
    bad_color = "darkred"
    
    indent = "--"

    for day in sorted(daily_data.keys()):
        deaths_by_day.append(int(daily_data[day]["death_increase"]))
        cases_by_day.append(int(daily_data[day]["case_increase"]))

        last_death_increase = daily_data[day]["death_increase"]
        last_case_increase = daily_data[day]["case_increase"]
        last_date = day

    three_day_death_average = sum(deaths_by_day[0:3]) / 3
    three_day_case_average = sum(cases_by_day[0:3]) / 3

    if three_day_death_average > int(last_death_increase):
        death_color = good_color
    else:
        death_color = bad_color

    if three_day_case_average > int(last_case_increase):
        case_color = good_color
    else:
        case_color = bad_color

    if death_color == bad_color or case_color == bad_color:
        state_color = bad_color
        state_emoji = ":arrow_upper_right:"
    else:
        state_color = good_color
        state_emoji = ":arrow_lower_right:"

    death_chart = pygal.Line()
    death_chart.add("", deaths_by_day)
    death_sparkline = death_chart.render_sparktext()

    case_chart = pygal.Line()
    case_chart.add("", cases_by_day)
    case_sparkline = case_chart.render_sparktext()

    mb_text = f"{state} {state_emoji}| color={state_color}\n"

    mb_text += (
        f"{indent}New Deaths on {last_date}: {last_death_increase} | color={death_color}\n"
    )
    mb_text += f"{indent}3 Day Average: {three_day_death_average:.2f} | color=black\n"
    mb_text += f"{indent}14 Day Graph: {death_sparkline} | color=black\n"

    mb_text += (
        f"{indent}New Cases on {last_date}: {last_case_increase} | color={case_color}\n"
    )
    mb_text += f"{indent}3 Day Average: {three_day_case_average:.2f} | color=black\n"
    mb_text += f"{indent}14 Day Graph: {case_sparkline} | color=black"

    return mb_text


def show_credits(tracker_data):
    print(f"Data: {tracker_data['name']} | href='{tracker_data['credit_uri']}'")


def main():
    conf = configure()
    trackers = conf["trackers"]

    get_state_data = globals()[
        f"{trackers[conf['data_provider']]['abbr']}_get_state_data"
    ]
    get_country_data = globals()[
        f"{trackers[conf['data_provider']]['abbr']}_get_country_data"
    ]

    show_menubar()

    for state in conf["states"]:
        status_code, stats = get_state_data(
            trackers[conf["data_provider"]]["data_uri"], state
        )
        if status_code == 200:
            show_data(format_state_data(stats, state))
        else:
            show_error(status_code)

    show_credits(trackers[conf["data_provider"]])


if __name__ == "__main__":
    main()
