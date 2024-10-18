-- Create cleaned table if not exists
CREATE TABLE IF NOT EXISTS historical_weather.cleaned_data
(
  city STRING,
  date DATE,
  avg_temp FLOAT64,
  min_temp FLOAT64,
  max_temp FLOAT64,
  humidity INT64,
  description STRING
);

-- Load csv date into raw table using LOAD DATA
LOAD DATA OVERWRITE historical_weather.raw_data
FROM FILES (
  format = 'CSV',
  field_delimiter = ';',
  uris = ['gs://historic_weather_bucket/historic_data.csv']);

-- Insert only new data to the cleaned table, using LEFT JOIN on NULL data from cleaned compare to raw tables
INSERT INTO historical_weather.cleaned_data
SELECT raw.city, raw.date, raw.avg_temp, raw.min_temp, raw.max_temp, raw.humidity, raw.description FROM historical_weather.raw_data AS raw
LEFT JOIN historical_weather.cleaned_data AS cleaned ON raw.city = cleaned.city AND raw.date = cleaned.date
WHERE cleaned.city IS NULL and cleaned.date IS NULL;
