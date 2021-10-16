Training
Training can be run only on the machine with GPU.
#Creating docker images

Run build.sh for creating docker image of the component of training
Run components/build.sh for creating docker image of components of download and export
#Creating cluster on minikube with GPU and Kubeflow Pipelines
minikube start --insecure-registry="0.0.0.0/0" --kubernetes-version=v1.21.5 --driver=none
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.9.0/nvidia-device-plugin.yml
Install Kubeflow Pipelines

export PIPELINE_VERSION=1.7.0
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
#Model training parameters

dataset-path on minio in format minio://bucket_name/.../dataset_name.tar.gz

export bucket - output bucket for saving model
model name - name for saving model
model_version - version for saving model
config -  by default will be used configs/CASCADE_RCNN_COCO.py, but you could redefine it and provide your config. Use the next format to choose your config: minio://bucket_name/.../config_name.py

resume_from - you could use it if training was interrupted for some reason, use the next format to choose a file of epoch: minio://bucket_name/.../epoch_name.pth

num_epoch - num epochs for training