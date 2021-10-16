from kfp.components import OutputPath


def download_dataset(input_path: str, output_path: OutputPath(str)):
    """Download the data set to the Kubeflow Pipelines
    volume to share it among all steps"""
    import tarfile
    import os
    from minio import Minio

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    client = Minio(
        os.environ.get("MINIO_SERVER"),
        os.environ.get("ACCESS_KEY"),
        os.environ.get("SECRET_KEY"),
        secure=False,
    )
    bucket, file_name = input_path.replace("minio://", "").split("/", maxsplit=1)
    client.fget_object(bucket, file_name, file_name.rsplit("/", maxsplit=1)[-1])
    tar = tarfile.open(name=file_name.rsplit("/", maxsplit=1)[-1], mode="r|gz")
    tar.extractall(path=output_path)
