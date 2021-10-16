import kfp
import kfp.components as components

from components.download import download_dataset
from components.export import export_model

BASE_IMAGE = "192.168.0.104:5000/minio_kubeflow:v1"

train = components.load_component_from_file("components/train.yaml")


def train_and_export(
    dataset_path: str,
    export_bucket: str,
    model_name: str,
    model_version: str,
    config: str,
    load_from: str,
    resume_from: str,
    num_epoch: int,
):
    downloadOP = components.func_to_container_op(
        download_dataset, base_image=BASE_IMAGE
    )(dataset_path)
    downloadOP.execution_options.caching_strategy.max_cache_staleness = "P0D"
    trainOp = train(
        dataset_path=downloadOP.output,
        load_from=load_from,
        resume_from=resume_from,
        config=config,
        num_epoch=num_epoch,
    )
    exportOp = components.func_to_container_op(export_model, base_image=BASE_IMAGE)(
        trainOp.output, export_bucket, model_name, model_version
    )


kfp.compiler.Compiler().compile(
    pipeline_func=train_and_export, package_path="train_pipeline.yaml"
)
