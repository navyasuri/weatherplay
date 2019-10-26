import access, requests

url = "https://accounts.spotify.com/api/token"
headers = {"Authorization": access.AUTH}
payload = {"grant_type": "authorization_code", "code": access.CODE, "redirect_uri":"http://google.com"}
res = requests.post(url, data=payload)

# url = "https://api.spotify.com/v1/search"
# headers = {"Authorization": access.ACCESS_TOKEN}
# payload = {"q":"sleepy", "type":"playlist"}
# res = requests.get(url, headers=headers, params=payload)
print(res.json)