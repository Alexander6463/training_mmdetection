import os
from minio import Minio
import logging


def create_client_minio(service: str, login: str, password: str):
    client = Minio(service, login, password, secure=False)
    return client


def download_from_path(path: str, source: str) -> None:
    client = create_client_minio(
        os.environ.get("MINIO_SERVER"),
        os.environ.get("ACCESS_KEY"),
        os.environ.get("SECRET_KEY"),
    )
    input_bucket, file_name = path.replace("minio://", "").split("/", maxsplit=1)
    try:
        client.fget_object(input_bucket, file_name, source)
    except IOError:
        logging.error("File does not exist, check input path")
