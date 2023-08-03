# 需要一个上传图片的函数，返回的是上传图片的访问地址
import os
import oss2
from app.config import config as cfg
endpoint = cfg["OSS"]["ENDPOINT"]
auth = oss2.Auth(cfg["OSS"]["AccessKeyId"], cfg["OSS"]["AccessKeySecret"])
bucket = oss2.Bucket(auth, endpoint, cfg["OSS"]["BucketName"])

def upload_image(image_path):
    bucket.put_object_from_file(os.path.basename(image_path), image_path)
    return os.path.basename(image_path)

def download_image(image_path, local_path):
    bucket.get_object_to_file(image_path, os.path.join(local_path, image_path))
    return os.path.join(local_path, image_path)