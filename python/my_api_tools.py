import requests
from time import sleep

def api_call(url, to_retry_status=(500, 502, 503, 504), max_retries=5):
    """
    Make a GET API call using requests, with retry on to_retry_status
    """
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response
            
            # Raise an exception to trigger the retry
            if response.status_code in to_retry_status:
                raise requests.exceptions.HTTPError(f"Received retryable status code {response.status_code}")
            
            # No retry needed, only raise
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            if response.status_code not in to_retry_status:
                # No retry needed
                raise

            retries += 1
            if retries >= max_retries:
                print(f"Faillure after {max_retries} tries : {e}")
                raise
            else:
                sleep_time = (2 ** (retries - 1)) # incremental sleep time
                print(f"{retries}/{max_retries} failed : {e}. New try in {sleep_time}s")
                sleep(sleep_time)
