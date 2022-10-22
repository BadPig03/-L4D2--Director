import requests

update_url = 'https://api.github.com/repos/BadPig03/-L4D2--Director/releases/latest'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'}

try:
    content = requests.get(update_url, headers=headers).content.decode().split('\n')
except OSError:
    content = ['  "name": "Director ERROR  ']
finally:
    pass


def get_latest_version():
    latest_version = None
    for row in content:
        if row.startswith('  "name":'):
            latest_version = row.split('"name": "Director ')[1][:-2]
    return latest_version
