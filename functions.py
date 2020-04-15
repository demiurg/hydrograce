#!/usr/bin/env python3

import glob
import re
from datetime import date, timedelta


dates_re = re.compile(
    r"(?P<range>"
    r"(?P<start>(?P<start_year>\d{4})(?P<start_doy>\d{3}))-"
    r"(?P<stop>(?P<stop_year>\d{4})(?P<stop_doy>\d{3}))"
    r")"
)

dates_months = {
    "2011289-2011319": (2011, 11),
    "2011347-2012011": (2011, 12),
    "2012080-2012109": (2012, 4),
    "2015102-2015131": (2015, 5),
    "2015180-2015212": (2015, 7),
    "2015345-2016003": (2015, 12),
    "2016029-2016060": (2016, 2),
    "2016221-2016247": (2016, 8),
    "2016319-2016345": (2016, 11),
    "2016346-2017006": (2016, 12),
    "2017007-2017034": (2017, 1),
    "2017076-2017104": (2017, 3),
    "2017100-2017128": (2017, 4),
    "2017143-2017179": (2017, 6),
    "2018295-2018313": (2018, 10),
    "2019026-2019065": (2019, 2),
    "2011290-2011320": (2011, 11),
    "2011351-2012015": (2011, 12),
    "2012080-2012110": (2012, 4),
    "2014305-2014336": (2014, 11),
    "2015346-2016003": (2015, 12),
    "2017143-2017180": (2017, 6),
    "2019026-2019063": (2019, 2),
}


def log(*args):
    print("log: " + " ".join(map(str, args)))


def fn2dates(f):
    dates = re.search(dates_re, f).groupdict()
    start = (
        date(int(dates["start_year"]), 1, 1)
        + timedelta(int(dates["start_doy"]) - 1)
    ).date()
    stop = (
        date(int(dates["stop_year"]), 1, 1)
        + timedelta(int(dates["stop_doy"]) - 1)
    ).date()

    dates["start_date"], dates["stop_date"] = start, stop
    if start.year == stop.year and start.month == stop.month:
        dates["year_month"] = (start.year, start.month)
    else:
        dates["year_month"] = dates_months.get(dates["range"])

    return dates


def index_files():
    gldas_files = glob.glob("data/GLDAS*.tif")
    gldas_dates = {}
    log(len(gldas_files), "GLDAS Files")
    for f in sorted(gldas_files):
        dates = fn2dates(f)
        gldas_dates[dates["year_month"]] = (f, dates)
        # log(dates.values())

    grace_files = glob.glob("data/*GR*.tif")
    grace_dates = {}
    log(len(grace_files), "GRACE Files")
    for f in sorted(grace_files):
        dates = fn2dates(f)
        grace_dates[dates["year_month"]] = (f, dates)
        # log(dates.values())

    # for drange, (f, dates) in grace_dates.items():
    #     if drange not in gldas_dates:
    #         print(
    #             dates["start_date"],
    #             dates["stop_date"],
    #             dates.get("year_month"),
    #             dates["range"],
    #         )

    # print("---")

    common_index = {}
    for year_month, (f, dates) in gldas_dates.items():
        if year_month not in grace_dates:
            log(
                dates["start_date"],
                dates["stop_date"],
                dates.get("year_month"),
                dates["range"],
            )
        else:
            common_index[year_month] = {
                "grace": grace_dates[year_month][0],
                "gldas": f,
            }

    return common_index


class GroundWater:
    def __init__(self):
        self.files = [
            (date(k[0], k[1], 1), v) for k, v in index_files().items()
        ]

    def get_dates(self, start: date, stop: date):
        """ Inclusive interval for simplicity """

        found = []
        for idx, files in self.files:
            if idx >= start and idx <= stop:
                found.append((idx, files))

        return found


def main():
    index_files()


if __name__ == "__main__":
    main()
