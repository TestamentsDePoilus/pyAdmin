import csv
import requests
import json
import codecs


def isfloat(value):
  try:
    float(value)
    return True
  except:
    return False


def compute_resource_order_in_will(will_resource_number):
    if will_resource_number.find('-') != -1:
        scope = will_resource_number[will_resource_number.find('-')+1:]
    else:
        scope = will_resource_number
    print(scope)

    if (len(scope) == 3 and not isfloat(scope[0:2])) or (len(scope) == 2 and isfloat(scope[1:2])):
        result = scope
    else:
        result = "0"+scope

    print(result)
    return result


def build_resource_structure(will_resource_is_envelope, will_resource_vue, will_resource_number, will_resource_note):
    return {
        "type": encode_resource_type(will_resource_is_envelope),
        "orderInWill": compute_resource_order_in_will(will_resource_number),
        "images": [will_resource_number],
        "notes": will_resource_note,
        "transcript": {
            "status": "todo",
            "updateComment": "Creation of the transcript"
        }
    }


def encode_resource_type(type):
    if type == "N":
        return "page"
    elif type == "O":
        return "envelope"
    else:
        return "page"


def get_entity(type, data):
    print("> Get Entity")
    url = 'https://testaments-de-poilus.huma-num.fr/api/web/'+type+'?search='+data
    response = requests.get(url)
    content = json.loads(codecs.decode(response.content, 'utf-8'))

    print(content)
    return content


def post_entity(type, data, access_token):
    print("> Post Entity")

    headers = {
        "Authorization": "Bearer "+access_token
    }
    url = 'https://testaments-de-poilus.huma-num.fr/api/web/'+type
    response = requests.post(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    content = json.loads(codecs.decode(response.content, 'utf-8'))

    print(content)
    return content


def compute_entity(type, content, extraData):
    print("> Compute Entity")
    if len(get_entity(type, content)) > 0:
        # The entity already exist, we return the id
        print(get_entity(type, content)[0])
        return get_entity(type, content)[0]['id']
    else:
        if content != None and content != "" and content != " ":
            # The entity doesn't exist, we prepare it and the we post it
            if type == "places":
                print(content)
                # ATTENTION, pour les lieux, il est nécessaire de scinder le département du lieu
                data = {
                    "names": [{
                        "name": content,
                        "updateComment": "Creation of the entity"
                    }],
                    "updateComment": "Creation of the entity"
                }
            elif type == "military-units":
                data = {
                    "name": content,
                    "updateComment": "Creation of the entity"
                }
            elif type == "testators":
                data = extraData
                print(data)

            entity = post_entity(type, data, access_token)
            return entity['id']
        else:
            return None


entities = {}
hosting_organization = input('Please type the name of the hosting organization: ')
username = input('Please type your username: ')
password = input('Please type your password: ')

login_fom = {
    "grant_type": "password",
    "client_id": "1_43bzn5kn2hycwk8wwkk8s00c4kkwoockg04s4wg0w804gwcwsw",
    "client_secret": "1eo7bryw41lw084c8gskgockcs4g40gowc8w8og40ok8cw08wk",
    "username": username,
    "password": password
}
url = 'https://testaments-de-poilus.huma-num.fr/api/web/oauth/v2/token'
response = requests.post(url, data=json.dumps(login_fom).encode('utf-8'))
content = json.loads(codecs.decode(response.content, 'utf-8'))
if "access_token" in content:
    access_token = content["access_token"]

    with open('data/data-numerisation.csv', newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            print(row)

            # Fields description:
            will_number = row[0]
            validation_resp = row[1]
            insert_resp = row[2]
            will_study = row[3]
            will_call_number = row[5]
            will_minute_date = row[6]
            will_writing_date = row[7]
            will_writing_place = row[8]
            will_testator_name = row[9]
            will_testator_surname = row[11]
            will_testator_firstnames = row[12]
            will_testator_profession = row[13]
            will_testator_address = row[14]
            will_testator_date_of_death = row[15]
            will_testator_place_of_death = row[16]
            will_testator_death_mention = row[17]
            will_testator_memoire_des_hommes = row[18]
            will_testator_military_unit = row[19]
            will_testator_rank = row[20]
            will_testator_date_of_birth = row[21]
            will_testator_place_of_birth = row[22]
            will_testator_description = row[23]
            will_notes = row[24]
            will_phys_desc = row[25]
            will_nb_pages = row[26]
            will_resource_vue = row[27]
            will_resource_nb_vues = row[28]
            will_resource_number = row[29]
            will_resource_name_image = row[30]
            will_resource_is_envelope = row[31]
            will_resource_note = row[32]

            if will_number in entities:
                # We already have information about the will, we add a new view
                computed_order = compute_resource_order_in_will(will_resource_number)
                is_exist_resource = False
                for resource in entities[will_number]["resources"]:
                    if resource['orderInWill'] == computed_order:
                        is_exist_resource = True
                        resource['images'].append(will_resource_number)

                if is_exist_resource is False:
                    entities[will_number]["resources"].append(build_resource_structure(will_resource_is_envelope, will_resource_vue, will_resource_number, will_resource_note))
            else:
                # We don't have info about the will
                if will_testator_memoire_des_hommes.find(',') != -1:
                    will_testator_memoire_des_hommes = will_testator_memoire_des_hommes.split(',')
                else:
                    will_testator_memoire_des_hommes = [will_testator_memoire_des_hommes]

                testatorData = {
                    "name": will_testator_name,
                    "surname": will_testator_surname,
                    "firstnames": will_testator_firstnames,
                    "profession": will_testator_profession,
                    # "addressNumber": TODO,
                    "addressStreet": will_testator_address,
                    # "addressDistrict": TODO,
                    # "addressCity": TODO,
                    "dateOfBirth": will_testator_date_of_birth,
                    "yearOfBirth": will_testator_date_of_birth[len(will_testator_date_of_birth)-4:],
                    "placeOfBirth": compute_entity("places", will_testator_place_of_birth, None),
                    "dateOfDeath": will_testator_date_of_death,
                    "yearOfDeath": will_testator_date_of_death[len(will_testator_date_of_death)-4:],
                    "placeOfDeath": compute_entity("places", will_testator_place_of_death, None),
                    "deathMention": will_testator_death_mention,
                    "memoireDesHommes": will_testator_memoire_des_hommes,
                    "militaryUnit": compute_entity("military-units", will_testator_military_unit, None),
                    "rank": will_testator_rank,
                    "description": will_testator_description,
                    "updateComment": "Creation of the entity"
                }

                entities[will_number] = {
                    "willNumber": will_number,
                    "will": {
                        "callNumber": will_call_number,
                        # "minuteLink": TODO,
                        "title": "Testament "+will_call_number,
                        "minuteDate": will_minute_date,
                        "minuteYear": will_minute_date[len(will_minute_date)-4:],
                        "willWritingDate": will_writing_date,
                        "willWritingYear": will_writing_date[len(will_writing_date)-4:],
                        "willWritingPlace": compute_entity("places", will_writing_place, None),
                        "testator": compute_entity("testators", will_testator_name, testatorData),
                        # "pagePhysDescSupport": TODO,
                        # "pagePhysDescHeight": TODO,
                        # "pagePhysDescWidth": TODO,
                        # "pagePhysDescHand": TODO,
                        # "envelopePhysDescSupport": TODO,
                        # "envelopePhysDescHeight": TODO,
                        # "envelopePhysDescWidth": TODO,
                        # "envelopePhysDescHand": TODO,
                        "hostingOrganization": hosting_organization,
                        "identificationUser": insert_resp
                    },
                    "resources": [build_resource_structure(will_resource_is_envelope, will_resource_vue, will_resource_number, will_resource_note)]
                }
    print(entities)

    print("Post entities >>>>")
    for number in entities:
        print(entities[number])
        post_entity("entities", entities[number], access_token)

else:
    print(content)
