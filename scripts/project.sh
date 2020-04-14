set -e

err_report() {
    echo "Error on line $1"
}
trap 'err_report $LINENO' ERR


for f in ../data/*.nc; do
	t="${f%.nc}.tif"
    echo "Projecting ${f} to ${t}"
    gdal_translate -a_srs EPSG:4326 netCDF:$f:TWS_monthly  -of GTiff $t
done