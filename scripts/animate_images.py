import requests

image_name = ["2304.05403.pdf_001_00.png","2304.05403.pdf_003_00.png","2304.05403.pdf_004_00.png","2304.05403.pdf_004_01.png",
              "2304.05403.pdf_005_00.png","2304.05403.pdf_005_01.png","2304.05403.pdf_005_02.png","2304.05403.pdf_005_03.png",
              "2304.05403.pdf_005_04.png","2304.05403.pdf_006_00.png","2304.05403.pdf_007_00.png","2304.05403.pdf_007_01.png",
              "2304.05440.pdf_002_00.png","2304.05440.pdf_004_00.png","2304.05440.pdf_005_00.png"]

url = "http://localhost:8010/animate_images/"

resp = requests.post(url, json = {
    "image_name_list": image_name
})

if resp.status_code == 200:
    print(resp.text)
else:
    print(resp.request.body)