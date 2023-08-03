import requests

image_name = "2304.05403.pdf_001_00.png"

url = "http://localhost:8010/get_image/"

resp = requests.post(url, json={
    "image_name": image_name
})

if resp.status_code == 200:
    print(resp.text)
else: 
    print(resp.request.body)