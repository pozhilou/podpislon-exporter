from prometheus_client import start_http_server, Gauge
import time
import requests
import warnings
warnings.filterwarnings("ignore")
orgs = {
    'company1': 'api1',
    'company2': 'api2',
    'company3': 'api3',
    'company4': 'api4',
}
stats_podpislon = Gauge('podpislon', 'Podpislon statistics', ['org', 'type'])
def get_stats():
    for org in orgs.values():
        url = 'https://podpislon.ru/integration/get-info'
        headers = {
            'Accept': '*/*',
            'x-api-key': org
        }
        req = requests.get(url, headers=headers, verify=False)
        data = req.json()
        name = data['company']['name']
        stats_podpislon.labels(name, 'signings').set(data['signings'])
        if org == 'api4':
            time.sleep(10)
if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        get_stats()
        time.sleep(1)
