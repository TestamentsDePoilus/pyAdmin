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
# client_id = input('Please type your client id: ')
# client_secret = input('Please type your client secret: ')
url_api = "https://testaments-de-poilus.huma-num.fr/api/web"

login_fom = {
    "grant_type": "password",
    "client_id": "1_l0damhmhybk0g00o8ssk4cg88sw0w0ss4swok4ok4s4gscow",
    "client_secret": "3o2hqkq803acswo0wosk08sos4o04og404s88cck4s0c4ssoss",
    "username": username,
    "password": password
}

url = url_api+'/oauth/v2/token'
response = requests.post(url, data=json.dumps(login_fom).encode('utf-8'))
content = json.loads(codecs.decode(response.content, 'utf-8'))
if "access_token" in content:
    access_token = content["access_token"]
    read_data('data/metadata_AN_2.csv', 'data/numerisation_AN_2.csv', access_token, entities, hosting_organization, url_api, post_agreement)

else:
    print(content)
