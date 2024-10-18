-- Use CTE to get the min and max temperature of the last 7 days
WITH calculated AS (
  SELECT MIN(min_temp) AS minimum, MAX(max_temp) AS maximum 
  FROM historical_weather.cleaned_data
  WHERE city = 'Paris' and date > DATE_ADD(CURRENT_DATE(), INTERVAL -7 DAY)
)
-- Join over cleaned table to get only the 2 rows, with : date, min_temps and max_temp
SELECT cleaned.date, cleaned.min_temp, cleaned.max_temp 
FROM historical_weather.cleaned_data AS cleaned
INNER JOIN calculated ON cleaned.min_temp = calculated.minimum OR cleaned.max_temp = calculated.maximum;