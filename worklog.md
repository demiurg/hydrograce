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
	2. gdal_translate netCDF to GeoTIFF with EPSG:4326 projection
2. -
