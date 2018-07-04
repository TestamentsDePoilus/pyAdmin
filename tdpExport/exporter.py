import requests
import json
import codecs


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1", "oui", "O")


def get_entities(dataType, data, url_api, profile):
    profileStr = ""
    if profile is not None:
        profileStr = "&profile="+profile

    if dataType is None or data is None or url_api is None:
        return []

    url = url_api+'/entities?'+dataType+"="+data+profileStr
    response = requests.get(url)
    content = json.loads(codecs.decode(response.content, 'utf-8'))

    print(url)
    print("> Get Entities: " + str(content))
    return content


def get_export(id, url_api):
    if id is None or url_api is None:
        return []

    url = url_api+'/xml?id='+id
    response = requests.get(url)
    content = json.loads(codecs.decode(response.content, 'utf-8'))

    print(url)
    print("> Get Export: " + str(content))
    return content


def exporter_lot(type, value, url_api, url_strict):
    entities = get_entities(type, value, url_api, "id")
    list_urls = []

    for entity in entities:
        list_urls.append(url_strict+str(get_export(str(entity['id']), url_api)['link']))

    print('Voici la liste de vos exports :')
    for url in list_urls:
        print(url)

def exporter(url_api, url_strict):
    with open('env/parameters.json', encoding='utf-8-sig') as json_file:
        parameters = json.load(json_file)

    entities = {}
    username = input('Please type your username: ')
    password = input('Please type your password: ')

    login_fom = {
        "grant_type": "password",
        "client_id": parameters['prod']['client_id'],
        "client_secret": parameters['prod']['client_secret'],
        "username": username,
        "password": password
    }
    url = url_api+'/oauth/v2/token'

    response = requests.post(url, data=json.dumps(login_fom).encode('utf-8'))
    content = json.loads(codecs.decode(response.content, 'utf-8'))
    if "access_token" in content:
        access_token = content["access_token"]
        export_type = int(input('Souhaitez-vous exporter une (tapez 1) ou plusieurs (tapez 2) notices ? '))

        if export_type == 1:
            id_to_export = input('Veuillez indiquer l\'identifiant de la notice à exporter : ')
            print("Cliquez sur le lien suivant pour télécharger votre contenu : "+url_strict+str(get_export(id_to_export, url_api)['link']))

        elif export_type == 2:
            q1 = str2bool(input('Voulez-vous exporter un lot de fiches en fonction de leur statut ? (oui/non) '))
            if q1 is True:
                q11 = input('Veuillez indiquer le statut à exporter : ')
                exporter_lot("status", q11, url_api, url_strict)
            else:
                q2 = str2bool(input('Voulez-vous exporter un lot de fiches en fonction de leur institution de provenance ? (oui/non) '))
                if q2 is True:
                    q21 = input('Veuillez indiquer le code de l\'institution : ')
                    exporter_lot("hosting-organization", q21, url_api, url_strict)
                else:
                    print('Nous n\'avons pas d\'autres critères à vous proposer.')
    else:
        print(content)