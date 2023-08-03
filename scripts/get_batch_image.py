import requests

image_name = ["2304.05403.pdf_001_00.png","2304.05403.pdf_003_00.png","2304.05403.pdf_004_00.png"]

url = "http://localhost:8010/get_batch_image/"

resp = requests.post(url, json = {
    "image_name_list": image_name
})

if resp.status_code == 200:
    print(resp.request.body)
    print(resp.text)
else:
    print(resp.request.body)