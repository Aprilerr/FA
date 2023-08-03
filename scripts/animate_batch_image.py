import requests

images_dir = "/tmp/1690966696.0097697"

resp = requests.get("http://localhost:8010/animate_batch_image/", params={
    "images_dir": images_dir
})

if resp.status_code == 200:
    print(resp.text)
else:
    print(resp.request.body)