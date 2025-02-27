import requests

url = "https://car-data.p.rapidapi.com/cars"

querystring = {"limit":"50","page":"0"}

headers = {
	"x-rapidapi-key": "a4e80050a9mshcb28b0906efb88fp1475fejsn3567a553014e",
	"x-rapidapi-host": "car-data.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())