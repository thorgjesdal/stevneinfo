import os
from pprint import pprint
import requests

def fetch_json(url):
    #
    url = url.strip('/') + '/json'
    idx = url.index('opentrack.run/')+14
    #print(idx)
    BASE_URL = url[0:idx]
    #print('x', url, BASE_URL)

    username = os.environ["OTUSER"]
    password = os.environ["OTPASSWD"]
    #print(username, password)

    r = requests.post(BASE_URL + "api/get-auth-token/", data=dict(username=username, password=password))
    #print(f"Authenticating.  Response: {r.status_code}")
    j2 = r.json()
    #pprint(j2)
    token = j2["token"]

    """
    # check authentication works
    r = requests.get(BASE_URL + "api/hello/", headers={
                 "Authorization": "Token " + token
                 })
    #print(r.json())
    """

# now use the token in a header to request the json for the competition
    #print(url)
    r  = requests.get(url, headers={ "Authorization": "Token " + token})
    j = r.json()

    return j

