
# make a string with the request type in it:
method = "POST"
# create a handler. you can specify different handlers here (file uploads etc)
# but we go for the default
handler = urllib.request.HTTPHandler()
# create an openerdirector instance
opener = urllib.request.build_opener(handler)
# build a request
data = urllib.parse.urlencode({"fullName": "Test", "surname": "Boudeau", "firstnames": "François Jean Étienne", "profession": "", "address": "81 boulevard Poniatowski, Paris (12e)", "dateOfBirth": "1875-11-30", "placeOfBirth": "Lieu de naissance", "dateOfDeath": "1914-09-23", "placeOfDeath": "Nevers (Nièvre)", "deathMention": "Mort pour la France", "memoireDesHommes": "http://www.memoiredeshommes.sga.defense.gouv.fr/fr/ark:/40699/m005239dad8ea05a", "regiment": "46e régiment d’infanterie", "rank": "Lieutenant"})
binary_data = data.encode('utf-8')
request = urllib.request.Request('http://localhost:8888/TestamentsDePoilus/api/web/app_dev.php/testators', binary_data)
# add any other information you want
request.add_header("Content-Type", 'application/json;version=1.0')
# overload the get method function with a small anonymous function...
request.get_method = lambda: method
# try it; don't forget to catch the result
try:
    connection = opener.open(request)
except urllib.request.HTTPError as e:
    connection = e
    print(e.reason)

# check. Substitute with appropriate HTTP code.
if connection.code == 200:
    data = connection.read()
    print(data)
elif connection.code == 400:
    data = connection.read()
    print(data)
else:
    print(connection)
    # handle the error case. connection.read() will still contain data
    # if any was returned, but it probably won't be of any use
