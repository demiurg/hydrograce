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
2. Prototype timeseries for point
3. Prototype 

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
