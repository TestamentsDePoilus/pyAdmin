import csv
import requests
import json
import codecs
from operator import itemgetter


def read_data(metadata_file_url, numerisation_file_url, access_token, entities, hosting_organization):
    ho_id = get_entity('hosting-organizations', hosting_organization).id

    with open(metadata_file_url, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            print(row)

            # Fields description:
            entity__will_number = row[0]
            entity__is_shown = row[1]
            will__validation_resp = row[2]
            will__lawyer_study_roman_number = row[3]
            will__lawyer_study_arab_number = row[4]
            will__lawyer_study_crpcen = row[5]
            will__call_number = row[6]
            will__minute_date_string = row[7]
            will__minute_date_normalized = row[8]
            will__will_writing_date_string = row[9]
            will__will_writing_date_normalized = row[10]
            will__will_writing_date_end_normalized = row[11]
            will__will_writing_place_string = row[12]
            will__will_writing_place_normalized = row[13]
            testator__fullname = row[14]
            testator__lastname = row[15]
            testator__firstnames = row[16]
            testator__index_name = row[17]
            testator__other_names = row[18]
            testator__profession = row[19]
            testator__address_string = row[20]
            testator__address_number_normalized = row[21]
            testator__address_street_normalized = row[22]
            testator__address_city_normalized = row[23]
            testator__death_date_string = row[24]
            testator__death_date_normalized = row[25]
            testator__death_date_end_normalized = row[26]
            testator__death_place_string = row[27]
            testator__death_place_normalized = row[28]
            testator__memoire_des_hommes = row[29]
            testator__deployment_string = row[30]
            testator__regiment_number_normalized = row[31]
            testator__regiment_name_normalized = row[32]
            testator__rank_string = row[33]
            testator__birth_date_string = row[34]
            testator__birth_date_normalized = row[35]
            testator__birth_place_string = row[36]
            testator__birth_place_normalized = row[37]
            testator__biography_string = row[38]
            testator__biography_link = row[39]
            will__notes = row[40]
            will__is_letter = row[41]
            will__will_phys_support = row[42]
            will__will_phys_hand = row[43]
            will__will_phys_dimensions = row[44]
            will__codicil_phys_support = row[45]
            will__codicil_phys_hand = row[46]
            will__codicil_phys_dimensions = row[47]
            will__envelope_phys_support = row[48]
            will__envelope_phys_hand = row[49]
            will__envelope_phys_dimensions = row[50]
            will__total_pages_number = row[51]
            will__total_view_number = row[52]
            will__photoshop = row[53]
            entity__resources = []

            with open(numerisation_file_url, newline='', encoding='utf-8') as csvfilenumerisation:
                spamreader_numerisation = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row_numerisation in spamreader_numerisation:
                    if row_numerisation[0] == entity__will_number:
                        order_in_will = compute_resource_order_in_will(row_numerisation[2])
                        gen = (resource for resource in entity__resources if resource['orderInWill'] == order_in_will)
                        if len(gen) > 0:
                            gen[0]["images"].append(row_numerisation[2])
                        else:
                            entity__resources.append({
                                "type": encode_resource_type(row_numerisation[1]),
                                "orderInWill": order_in_will,
                                "images": [row_numerisation[2]],
                                "notes": None,
                                "transcript": {
                                    "status": "todo",
                                    "updateComment": "Creation of the transcript"
                                }
                            })
            print(entity__resources)

            if entity__will_number not in entities:
                # Name of the testator
                if testator__fullname != '':
                    name = testator__fullname
                else:
                    name = testator__firstnames + " " + testator__lastname

                # Index name of the testator
                if testator__index_name != '':
                    index_name = testator__index_name
                else:
                    index_name = + testator__lastname.upper() + " " + testator__firstnames

                # Will type management
                if will__is_letter == "":
                    will_type = "Testament olographe"
                else:
                    will_type = "Lettre de dernières volontés"
                will_type_id = get_entity('will-types', will_type).id

                testator_data = {
                    "name": name,
                    "indexName": index_name,
                    "surname": testator__lastname,
                    "firstnames": testator__firstnames,
                    "otherNames": testator__other_names,
                    "profession": testator__profession,
                    "addressString": testator__address_string,
                    "addressNumber": testator__address_number_normalized,
                    "addressStreet": testator__address_street_normalized,
                    "addressDistrict": extract_value(testator__address_city_normalized, 'a'),
                    "addressCity": compute_entity("places", extract_value(testator__address_city_normalized, False), None, access_token),
                    "dateOfBirthString ": testator__birth_date_string,
                    "yearOfBirth": testator__birth_date_normalized[len(testator__birth_date_normalized)-4:],
                    "dateOfBirthNormalized": testator__birth_date_normalized,
                    "dateOfBirthEndNormalized": None,
                    "placeOfBirthString": testator__birth_place_string,
                    "placeOfBirthNormalized": compute_entity("places", testator__birth_place_normalized, None, access_token),
                    "dateOfDeathString": testator__death_date_string,
                    "yearOfDeath": testator__death_date_normalized[len(testator__death_date_normalized)-4:],
                    "dateOfDeathNormalized": testator__death_date_normalized,
                    "dateOfDeathEndNormalized": testator__death_date_end_normalized,
                    "placeOfDeathNormalized": compute_entity("places", testator__death_place_normalized, None, access_token),
                    "placeOfDeathString": testator__death_place_string,
                    "deathMention": "mort pour la France",
                    "memoireDesHommes": arrayfy(testator__memoire_des_hommes),
                    "militaryUnitNormalized": compute_entity("military-units", [testator__regiment_number_normalized, testator__regiment_name_normalized], None, access_token),
                    "militaryUnitString": testator__regiment_name_normalized,
                    "militaryUnitDeploymentString": testator__deployment_string,
                    "rank": testator__rank_string,
                    "description": testator__biography_string,
                    "isOfficialVersion": True,
                    "updateComment": "Creation of the entity"
                }
                testator_entity_id = compute_entity("testators", name, testator_data, access_token)

                # Bibliography management:
                if testator__biography_link != "":
                    if testator__biography_link.find('|') != -1:
                        testator_bibliography_data = testator__biography_link.split('|')
                    else:
                        testator_bibliography_data = [testator__biography_link]

                    for biblio in testator_bibliography_data:
                        post_entity("reference-items", {
                            "freeReference": biblio,
                            "testator": testator_entity_id,
                            "updateComment": "Creation of the reference"
                        }, access_token)

                # Entity management:
                entities[entity__will_number] = {
                    "willNumber": entity__will_number,
                    "isShown": entity__is_shown,
                    "will": {
                        "callNumber": will__call_number,
                        "notaryNumber": will__lawyer_study_arab_number,
                        "crpcenNumber": will__lawyer_study_crpcen,
                        "title": "Testament "+will__call_number + " du " + testator__death_date_normalized + " de " + name,
                        "minuteLink": None,
                        "minuteDateString": will__minute_date_string,
                        "minuteDateNormalized": will__minute_date_normalized,
                        "minuteDateEndNormalized": None,
                        "minuteYear": will__minute_date_normalized[len(will__minute_date_normalized)-4:],
                        "willWritingDateString": will__will_writing_date_string,
                        "willWritingDateNormalized": will__will_writing_date_normalized,
                        "willWritingDateEndNormalized": will__will_writing_date_end_normalized,
                        "willWritingYear": will__will_writing_date_normalized[len(will__will_writing_date_normalized)-4:],
                        "willWritingPlaceNormalized": compute_entity("places", will__will_writing_place_normalized, None, access_token),
                        "willWritingPlaceString": will__will_writing_place_string,
                        "testator": testator_entity_id,
                        "pagePhysDescSupport": will__will_phys_support,
                        "pagePhysDescHeight": get_dimension(will__will_phys_dimensions, 'h'),
                        "pagePhysDescWidth": get_dimension(will__will_phys_dimensions, 'w'),
                        "pagePhysDescHand": will__will_phys_hand,
                        "pagePhysDescNumber": None,
                        "envelopePhysDescSupport": will__envelope_phys_support,
                        "envelopePhysDescHeight": get_dimension(will__envelope_phys_dimensions, 'h'),
                        "envelopePhysDescWidth": get_dimension(will__envelope_phys_dimensions, 'h'),
                        "envelopePhysDescHand": will__envelope_phys_hand,
                        "codicilPhysDescSupport": will__codicil_phys_support,
                        "codicilPhysDescHeight": get_dimension(will__codicil_phys_dimensions, 'h'),
                        "codicilPhysDescWidth": get_dimension(will__codicil_phys_dimensions, 'h'),
                        "codicilPhysDescHand": will__codicil_phys_hand,
                        "codicilPhysDescNumber": None,
                        "hostingOrganization": ho_id,
                        "identificationUser": will__validation_resp,
                        "willType": will_type_id,
                        "description": will__notes,
                        "isOfficialVersion": True,
                    },
                    "resources": entity__resources
                }
    print(entities)


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


def encode_resource_type(type_of_resource):
    if type_of_resource == "testament":
        return "page"
    elif type_of_resource == "enveloppe":
        return "envelope"
    elif type_of_resource == "codicille":
        return "codicil"
    else:
        return "page"


def get_entity(type_of_entity, data):
    print("> Get Entity")
    url = 'http://localhost:8888/TestamentsDePoilus/api/web/app_dev.php/'+type_of_entity+'?search='+data
    response = requests.get(url)
    content = json.loads(codecs.decode(response.content, 'utf-8'))

    print(content)
    return content


def post_entity(type_of_entity, data, access_token):
    print("> Post Entity")

    headers = {
        "Authorization": "Bearer "+access_token
    }
    url = 'http://localhost:8888/TestamentsDePoilus/api/web/app_dev.php/'+type_of_entity
    response = requests.post(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    content = json.loads(codecs.decode(response.content, 'utf-8'))

    print(content)
    return content


def compute_entity(type_of_entity, normalized_entity, extra_data, access_token):
    print("> Compute Entity")

    if type_of_entity == "military-units":
        normalized_name = compute_entity_from_source(normalized_entity[1], ['MDH', 'NOT', 'TES', 'EC', 'AS'])
        normalized_number = compute_entity_from_source(normalized_entity[0], ['MDH', 'NOT', 'TES', 'EC', 'AS'])

        if normalized_number is not None and normalized_name is not None:
            normalized_entity = normalized_number + "e " + normalized_name
        elif normalized_number is None and normalized_name is not None:
            normalized_entity = normalized_name
        else:
            normalized_entity = None

    if len(get_entity(type_of_entity, normalized_entity)) > 0:
        # The entity already exist, we return the id
        print(get_entity(type_of_entity, normalized_entity)[0])
        return get_entity(type_of_entity, normalized_entity)[0]['id']
    else:
        if normalized_entity is not None and normalized_entity != "" and normalized_entity != " ":
            # The entity doesn't exist, we prepare it and the we post it
            if type_of_entity == "places":
                print(normalized_entity)
                data = {
                    "names": [{
                        "name": extract_value(normalized_entity, None),
                        "updateComment": "Creation of the entity"
                    }],
                    "updateComment": "Creation of the entity",
                    "isOfficialVersion": True,
                }
                if extract_value(normalized_entity, True) is not None:
                    data['frenchDepartements'].append({
                        "name": extract_value(normalized_entity, True),
                        "updateComment": "Creation of the entity"
                    })
                if extract_value(normalized_entity, "p") is not None:
                    data['countries'].append({
                        "name": extract_value(normalized_entity, True),
                        "updateComment": "Creation of the entity"
                    })
                if extract_value(normalized_entity, "r") is not None:
                    data['countries'].append({
                        "name": extract_value(normalized_entity, True),
                        "updateComment": "Creation of the entity"
                    })
            elif type_of_entity == "military-units":
                data = {
                    "name": normalized_entity,
                    "updateComment": "Creation of the entity",
                    "isOfficialVersion": True,
                }
            elif type_of_entity == "testators":
                data = extra_data
                print(data)

            entity = post_entity(type_of_entity, data, access_token)
            return entity['id']
        else:
            return None


def arrayfy(string):
    if string.find(',') != -1:
        string = string.split(',')
    else:
        string = [string]
    return string


def extract_value(string, type_of_value):
    if string.find('(') == -1 and type_of_value is False:
        # We are looking for the name of the place
        return string
    elif string.find('(') == -1 and type_of_value is not False:
        # We are looking for something else than the name of the place but there is nothing else
        return None
    elif string.find('(') != -1:
        # If there is specifications
        if type_of_value is False:
            # We just want the name of the place
            return string[:string.find('(')-1]
        elif type_of_value is not False:
            if type_of_value is True:
                # We want the french departement
                specification_content = string[string.find('(')+1:string.find(')')-1]
                if specification_content.find(':') == -1:
                    return specification_content
                else:
                    if specification_content.find(','):
                        array_specifications = specification_content.split(',')
                        for spec in array_specifications:
                            if spec.find(':') == -1:
                                return spec
                    else:
                        return None
            else:
                # We want something else
                specification_content = string[string.find('(')+1:string.find(')')-1]
                print(specification_content)
                if specification_content.find(type_of_value+':') != -1:
                    if specification_content.find(','):
                        array_specifications = specification_content.split(',')
                        for spec in array_specifications:
                            if spec.find(type_of_value+':') != -1:
                                return spec[spec.find(type_of_value + ':') + len(type_of_value + ':'):len(spec)]
                    else:
                        return specification_content[specification_content.find(type_of_value+':')+len(type_of_value+':'):len(specification_content)]
                else:
                    return None


def get_dimension(string, type_of_dimension):
    array_dimension = string.split(' x ')
    if type_of_dimension == 'h':
        return array_dimension[0]
    else:
        return array_dimension[1]


def compute_entity_from_source(string, array_source):
    if string != '':
        if string.find('|') != -1:
            array_content = string.split('|')
            content_list = []
            for value in array_content:
                source = value[value.find('[')+1:value.find(']')-1]
                content_list.append({
                    'value': value[:value.find('[')-1],
                    'source': source,
                    'order': array_source.find(source)
                })

            content_list_order = sorted(content_list, key=itemgetter('order'))
            return content_list_order[0]['value']
        else:
            if string.find('[') != -1:
               return string[:string.find('[')-1]
            else:
                return string
    else:
        return None
