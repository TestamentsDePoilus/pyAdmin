import csv
import requests


def isfloat(value):
  try:
    float(value)
    return True
  except:
    return False


def compute_resource_order_in_will(will_resource_number):
    if will_resource_number.find('-') != -1:
        scope = will_resource_number[will_resource_number.find('-'):]
    else:
        scope = will_resource_number

    if len(scope) == 1 or (len(scope) == 2 and isfloat(scope[1:])) or (len(scope) == 3 and isfloat(scope[2:])):
        result = scope
    elif (len(scope) == 2 and isfloat(scope[1:]) is not True) or (len(scope) == 3 and isfloat(scope[2:]) is not True):
        result = scope[:1]
    else:
        result = scope

    return result


def build_resource_structure(will_resource_is_envelope, will_resource_vue, will_resource_number, will_resource_note):
    return {
        "type": encode_resource_type(will_resource_is_envelope), # Attention, ça ne renvoie pas exactement la valeur attendue
        "orderInWill": compute_resource_order_in_will(will_resource_number),
        "images": will_resource_number, # Attention, pas exactement la valeur attendue
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
    url = 'http://localhost:8888/TestamentsDePoilus/api/web/app_dev.php/'+type+'?search='+data
    response = requests.get(url)
    print(response.content)
    return response.content


def post_entity(type, data):
    url = 'http://localhost:8888/TestamentsDePoilus/api/web/app_dev.php/'+type
    response = requests.post(url, data=data.encode('utf-8'))
    print(response.content)
    return response.content


def compute_entity(type, content, extraData):
    if len(get_entity(type, content)) > 0:
        # The entity already exist, we return the id
        return get_entity(type, content)[0].id
    else:
        # The entity doesn't exist, we prepare it and the we post it
        if type == "places":
            # ATTENTION, pour les lieux, il est nécessaire de scinder le département du lieu
            data = {
                "name": {
                    "name": content,
                    "updateComment": "Creation of the entity"
                },
                "updateComment": "Creation of the entity"
            }
        elif type == "military-units":
            data = {
                "name": content,
                "updateComment": "Creation of the entity"
            }
        elif type == "testators":
            data = extraData

        entity = post_entity(type, data)
        return entity.id


entities = {}
hosting_organization = input('Please type the name of the hosting organization: ')
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
            entities[will_number]["resources"].append(build_resource_structure(will_resource_is_envelope, will_resource_vue, will_resource_number, will_resource_note))
        else:
            # We don't have info about the will
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
                "description": will_testator_description
            }

            entities[will_number] = {
                "willNumber": will_number,
                "will": {
                    "callNumber": will_call_number,
                    # "minuteLink": TODO,
                    # "title": TODO,
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

for number in entities:
    post_entity("entities", entities[number])