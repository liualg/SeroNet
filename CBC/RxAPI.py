import requests
import json

#https://lhncbc.nlm.nih.gov/RxNav/APIs/api-RxNorm.getApproximateMatch.html
SERVIVE_DOMAIN = "https://rxnav.nlm.nih.gov"

SEARCH = "acetominophen"
MAX_VALUES = "5"
OPTION = "0"


# REQUEST = f"/REST/approximateTerm.xml?term={SEARCH}&maxEntries={MAX_VALUES}&option={OPTION}"
# url = SERVIVE_DOMAIN + REQUEST

# print(url)
response = requests.get(SERVIVE_DOMAIN)
response.json()
# print(response.headers.get(REQUEST))

# response.text
