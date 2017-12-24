import csv
import requests
import json
import codecs
from importer.uploader import read_data


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


entities = {}
hosting_organization = input('Please type the name of the hosting organization: ')
username = input('Please type your username: ')
password = input('Please type your password: ')
post_agreement = str2bool(input('Do you want to post the entities: '))

login_fom = {
    "grant_type": "password",
    "client_id": "1_3bcbxd9e24g0gk4swg0kwgcwg4o8k8g4g888kwc44gcc0gwwk4",
    "client_secret": "4ok2x70rlfokc8g0wws8c8kwcokw80k44sg48goc0ok4w0so0k",
    "username": username,
    "password": password
}

url_api = 'http://localhost:8888/TestamentsDePoilus/api/web/app_dev.php'

url = 'http://localhost:8888/TestamentsDePoilus/api/web/app_dev.php/oauth/v2/token'
response = requests.post(url, data=json.dumps(login_fom).encode('utf-8'))
content = json.loads(codecs.decode(response.content, 'utf-8'))
if "access_token" in content:
    access_token = content["access_token"]

    read_data('data/data-metadata.csv', 'data/data-numerisation.csv', access_token, entities, hosting_organization, url_api, post_agreement)

else:
    print(content)

