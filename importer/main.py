import json
import urllib.parse
import urllib.request

# response = urllib.request.urlopen('http://localhost:8888/TestamentsDePoilus/api/web/app_dev.php/entities')
# result = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
# print(result)


import requests
url = 'http://localhost:8888/TestamentsDePoilus/api/web/app_dev.php/testators'
data = '''{"fullName": "Test via Python 3", "surname": "Boudeau", "firstnames": "François Jean Étienne", "profession": "", "address": "81 boulevard Poniatowski, Paris (12e)", "dateOfBirth": "1875-11-30", "placeOfBirth": "Lieu de naissance", "dateOfDeath": "1914-09-23", "placeOfDeath": "Nevers (Nièvre)", "deathMention": "Mort pour la France", "memoireDesHommes": "http://www.memoiredeshommes.sga.defense.gouv.fr/fr/ark:/40699/m005239dad8ea05a", "regiment": "46e régiment d’infanterie", "rank": "Lieutenant"}'''
response = requests.post(url, data=data.encode('utf-8'))
print(response.content)
