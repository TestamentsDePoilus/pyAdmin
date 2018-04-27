import csv
import requests
import json
import codecs
from tdpImporter.uploader import read_data


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


with open('env/parameters.json', encoding='utf-8-sig') as json_file:
    parameters = json.load(json_file)

entities = {}
hosting_organization = input('Please type the name of the hosting organization (Archives nationales): ')
username = input('Please type your username: ')
password = input('Please type your password: ')
post_agreement = str2bool(input('Do you want to post the entities: '))

login_fom = {
    "grant_type": "password",
    "client_id": parameters['dev']['client_id'],
    "client_secret": parameters['dev']['client_secret'],
    "username": username,
    "password": password
}

url_api = 'https://tdp.karl-pineau.fr/api/web'

url = 'https://tdp.karl-pineau.fr/api/web/oauth/v2/token'
response = requests.post(url, data=json.dumps(login_fom).encode('utf-8'))
content = json.loads(codecs.decode(response.content, 'utf-8'))
if "access_token" in content:
    access_token = content["access_token"]

    read_data('data/data-metadata2.csv', 'data/data-numerisation2.csv', access_token, entities, hosting_organization, url_api, post_agreement)

else:
    print(content)

