import requests

update_url = 'https://api.github.com/repos/BadPig03/-L4D2--Director/releases/latest'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'}
content = requests.get(update_url, headers=headers).content.decode().split('\n')


def get_latest_version():
    latest_version = None
    for row in content:
        if row.startswith('  \"name\":'):
            latest_version = row.split('"name": "Director ')[1][:-2]
    return latest_version


'''
url = 'https://dl.hdslb.com/mobile/fixed/bili_win/bili_win-install.exe?v=1.6.1'
filename = 'bili_installer.exe'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'}
print('Downloading...')
response = requests.get(url, headers=headers)
content = response.content

with open(filename, 'wb') as file:
    file.write(content)
print('Downloaded %s' % filename)
'''
