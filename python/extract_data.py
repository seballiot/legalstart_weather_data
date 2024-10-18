import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

from my_api_tools import api_call

print(f"Script start")

# Load env variable
load_dotenv()

# API secrets & params
api_key = os.getenv('API_KEY')
api_base_url = 'https://api.weatherapi.com/v1'
city = 'Paris'
start_dt = (datetime.now() - timedelta(days=7)).date()
end_dt = datetime.now().date()

# CSV file infos
output_dir = '/app/output'
file_name = 'historic_data.csv'
file_columns = ['city', 'date', 'avg_temp', 'min_temp', 'max_temp', 'humidity', 'description']

os.makedirs(output_dir, exist_ok=True)

# API call
try:
    url = f"{api_base_url}/history.json?key={api_key}&q={city}&dt={start_dt}&end_dt={end_dt}"
    response = api_call(url)
except requests.exceptions.HTTPError as e:
    print(f"Error during API call")
    print(e.response.text)
    raise SystemExit(e)

# Parse the response, ex of output :
# {
#   "location": {
#     "name": "Paris",
#     [...]
#   },
#   "forecast": {
#     "forecastday": [
#       {
#         "date": "2024-10-17",
#         "day": {
#           "maxtemp_c": 18.5,
#           [...]
#           "condition": {
#             "text": "Light rain shower",
#             [...]
#           },
#         },
#       }
#     ]
#   }
# }
recent_df = pd.DataFrame(columns=file_columns)
for el in response.json()['forecast']['forecastday']:
    print(f"Processing date {el['date']}...")
    tmp = el['day']
    recent_df = pd.concat([
        recent_df if not recent_df.empty else None,
        pd.DataFrame([[city,el['date'],tmp['avgtemp_c'],tmp['mintemp_c'], tmp['maxtemp_c'], tmp['avghumidity'], tmp['condition']['text']]], columns=recent_df.columns)
        ], ignore_index=True)

# Cast date to correct type
recent_df['date'] = pd.to_datetime(recent_df['date'], format='%Y-%m-%d')
recent_df.sort_values(by=['date'], inplace=True)

# Load previous historic csv if exists
if os.path.isfile(f"{output_dir}/{file_name}"):
    old_df = pd.read_csv(f"{output_dir}/{file_name}", sep=';', header=0, usecols=file_columns)
    old_df['date'] = pd.to_datetime(old_df['date'], format='%Y-%m-%d')

    # Concat previous data to new ones
    df_to_write = pd.concat([old_df, recent_df], ignore_index=True)
    del old_df, recent_df

    # Remove duplicates on keeping fresh data
    df_to_write.drop_duplicates(subset=['city', 'date'], keep='last', inplace=True)
else:
    df_to_write = recent_df

print("Dataframe to write :")
print(df_to_write)

df_to_write.to_csv(f"{output_dir}/{file_name}", sep=';', index=False)
print(f"Write csv {output_dir}/{file_name} OK")
