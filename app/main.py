from fastapi import FastAPI
from app.OSSutils import *
from pydantic import BaseModel
import time
app = FastAPI()

class GET_IMAGE_IMP(BaseModel):
    image_name: str

class GET_BATCH_IMAGE_IMP(BaseModel):
    image_name_list: list

@app.post("/get_image/")
def getImage(GET_IMAGE_IMP: GET_IMAGE_IMP):
    image_path = download_image(image_path=GET_IMAGE_IMP.image_name, local_path="./")
    print(image_path)
    return image_path

@app.post("/get_batch_image/")
def getBatchImage(GET_BATCH_IMAGE_IMP: GET_BATCH_IMAGE_IMP):
    TIME_NOW = str(time.time())
    output_dir = os.path.join("/tmp",TIME_NOW)
    os.makedirs(output_dir, exist_ok=True)
    image_path_list = []
    for image_name in GET_BATCH_IMAGE_IMP.image_name_list:
        image_path = download_image(image_path=image_name, local_path=output_dir)
        image_path_list.append(image_path)
    return image_path_list, output_dir

@app.get("/animate_batch_image/")
def animate_batch_image(images_dir: str):
    os.system(f"python figure_animation.py --input {images_dir} --output_dir {os.path.join(images_dir,'outputs')} --presentation_dir {os.path.join(images_dir,'presentation')}")
    presentation_list = []
    for file in os.listdir(os.path.join(images_dir,'presentation')):
        if file.endswith((".gif")):
            presentation_list.append(os.path.join(images_dir,'presentation',file))
    return presentation_list

@app.post("/animate_images/")
def animate_images(GET_BATCH_IMAGE_IMP: GET_BATCH_IMAGE_IMP):
    image_path_list, output_dir = getBatchImage(GET_BATCH_IMAGE_IMP)
    presentation_list = animate_batch_image(output_dir)
    return presentation_list
