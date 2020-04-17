## Questions

* Demonstrate a basic understanding of what the data is, and how it is distributed.
    * How do you access just the data you want?
    * Are there multiple products, which is the right one?
    * What are the units?
* Demonstrate your ability to communicate by making this information approachable
    * graphs, charts, visualizations, etc. within the Notebook.
* Explain what the challenges are with accessing and using this data?
    * Is there additional processing that can or should be done?
* What would be some potential challenges in scaling up analysis for large areas, and how
would you approach this?

## Tasks

1. Download right data
    1. identify product
    2. download product
2. Timeseries for point
    1. open file
    2. get point for x, y, time, band
3. Aggregate for polygon
4. Aggregate timeseries for polygon

## Browsing data steps

1. https://grace.jpl.nasa.gov/applications/overview/#hydrology
2. https://grace.jpl.nasa.gov/applications/groundwater/
    * background on data usage
3. https://grace.jpl.nasa.gov/data/get-data/
    * categorizes data
4. https://grace.jpl.nasa.gov/data/get-data/monthly-mass-grids-land/
    * Furthermore, the gain factors tend to be dominated by the annual cycles of water storage variations, and may thus not be suitable to quantify trends from the GRCTellus land data.
    * g'(x,y,t) = g(x,y,t) * s(x,y)
    * netCDF contains scaling cooficient for x, y
5. https://podaac.jpl.nasa.gov/GRACE
    * Data is provided as global gravity anomoly from 3 institutions:
        * GFZ (GeoforschungsZentrum Potsdam)
        * CSR (Center for Space Research at University of Texas, Austin)
        * JPL (Jet Propulsion Laboratory)
6. https://podaac.jpl.nasa.gov/dataset/TELLUS_GLDAS-NOAH-3.3_TWS-ANOMALY_MONTHLY?ids=DataFormat:ProcessingLevel&values=NETCDF:*3*&search=GRACE
    * Level 3 data is GLDAS hydrology model
7. https://docserver.gesdisc.eosdis.nasa.gov/public/project/hydrology/GRACEGroundwater.pdf
    * dG = dTWS(GRACE) - (dSoilMoisture(GLDAS) + dSnowWaterEquivalent(GLDAS))


## Data

* GLDAS
    * https://podaac.jpl.nasa.gov/dataset/TELLUS_GLDAS-NOAH-3.3_TWS-ANOMALY_MONTHLY
        * 2002 - Present
        * NetCDF only
* GRACE-FO
    * https://podaac.jpl.nasa.gov/dataset/TELLUS_GRFO_L3_CSR_RL06_LND_v03
        * 2018 - Present
        * GeoTIFF with projection
* GRACE
    * https://podaac.jpl.nasa.gov/dataset/TELLUS_GRAC_L3_CSR_RL06_LND_v03
        * 2002 - 2017
        * GeoTIFF with projection
* No valid temporal coverage metadata from the server
    * OWSLib dataset url not clear for time coverage, only individual files
    * Opening HTTP URL did not work, subsetting using pydap did not work
    * pydap errors:
    ```
        TTPError: 400 Bad Request
        Error {
            code = 400;
            message = "libdap error transmitting DataDDS: Constraint expression parse error: No such identifier in dataset: TWS_monthly.TWS_monthly[0";
        }
    ```
* No valid projection on netcdf grid and no TIFF files for GLDAS
    * Download GeoTIFF for GRACE/FO data, because it is georeferenced
    * Convert NetCDF to GeoTIFF with projection

## Actions

1. Prepare the data
    1. Download the data.
        1. parse filenames from HTML, save as files
        2. write wget script to download all files by url
    2. gdal_translate netCDF to GeoTIFF with EPSG:4326 projection
2. Align the time index
    1. Notes
        1. Some GLDAS date ranges did not align, but were contained within GRACE from CSR
        2. Some dates were extended out
        3. It is possible that other institutions have generated different date ranges
    2. Create [(year, month): filename] map
        1. Identify exceptions to the ordered dates:
        ```
        2011-08-01 2011-08-31 (2011, 8) 2011213-2011243 
        2011-09-01 2011-09-30 (2011, 9) 2011244-2011273 
        2011-10-01 2011-10-31 (2011, 10) 2011274-2011304 
        2011-10-16 2011-11-15 None 2011289-2011319 grace not in gldas
        2011-12-13 2012-01-11 None 2011347-2012011 grace not in gldas
        2012-01-01 2012-01-31 (2012, 1) 2012001-2012031 
        2012-02-01 2012-02-29 (2012, 2) 2012032-2012060 
        2012-03-01 2012-03-31 (2012, 3) 2012061-2012091 
        2012-03-20 2012-04-18 None 2012080-2012109 grace not in gldas
        2012-06-01 2012-06-30 (2012, 6) 2012153-2012182 
        # becomes
        dates_months = {
            "2011289-2011319": (2011, 11),
            "2011347-2012011": (2011, 12),
            "2012080-2012109": (2012, 4),
        }
        ```
2. Build functions
    1. Create class for reusability of any state, from memory, such as file handles or intermediary aggregates
    2. Add mothod
        1. takes start date, end date, and a shapely shape object
        2. finds all files between the dates
        3. clips all files to shape object
        4. aggregates mean value
        5. combines aggregated by 'mean' values into timeseries array
    3. Test

## Things TODO

1. There are multiple improvements to how data can be accessed.
    1. Find and use time catalog or service that would allow to request specific data by time.
    2. Use a data client to request specific spacial range from raster files.
2. There are possible improvements to data processing
    1. Use the mean of all 3 GRACE dataset
    2. Optimize aggregation algorithm to rasterize a polygon, and then apply a mask to improve speed
