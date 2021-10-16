from kfp.components import InputPath


def export_model(
    model_dir: InputPath(str),
    export_bucket: str,
    model_name: str,
    model_version: str,
):
    import os
    from minio import Minio
    from pathlib import Path

    client = Minio(
        os.environ.get("MINIO_SERVER"),
        os.environ.get("ACCESS_KEY"),
        os.environ.get("SECRET_KEY"),
        secure=False,
    )

    # Create export bucket if it does not yet exist
    if not client.bucket_exists(export_bucket):
        client.make_bucket(export_bucket)

    # Save model files to minio
    for file in model_dir.glob("**/*.*"):
        minio_path = Path(file).relative_to(model_dir)
        print(file, minio_path)
        client.fput_object(
            export_bucket,
            str(Path(model_name, model_version, minio_path)),
            str(file))

    response = client.list_objects(
        export_bucket,
        prefix=str(Path(model_name) / Path(model_version)),
        recursive=True,
    )

    print(f"All objects in {export_bucket}:")
    for file in response:
        print(file.object_name)
