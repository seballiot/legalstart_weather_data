## Context

Case study using weather data and data analysis in BigQuery

Author : Sébastien Alliot

## Repository content

- `python/` : python scripts for extracting data from API

- `sql/` : BigQuery scripts for analytics

- `documentation/` : Documentation

## Run python app

**Requirements** : Docker is installed

- Create output dir for volume
```
mkdir -p output
```
- Build image from the Dockerfile
```
docker build -t extract_weather_app python/.
```
- Run container with volume mount to collect csv output 
```
docker run --rm -v $(pwd)/output:/app/output extract_weather_app
```
- Check the output
```
head output/historic_data.csv
```