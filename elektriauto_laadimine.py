import requests

#api = requests.get("https://dashboard.elering.ee/api/nps/price?start=2026-09-29T00%3A00%3A00.000Z&end=2026-09-29T20%3A59%3A59.999Z")
#print(api.text)

api = "https://dashboard.elering.ee/api/nps/price?start=2026-09-29T00%3A00%3A00.000Z&end=2026-09-29T20%3A59%3A59.999Z"
response = requests.get(api)
data = response.json()

for el in data[data][ee]:
    print(el)