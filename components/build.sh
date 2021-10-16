export IMAGE_NAME=minio_kubeflow
export IMAGE_TAG=v1
export FULL_IMAGE_NAME=${IMAGE_NAME}:${IMAGE_TAG}

docker build -t "${FULL_IMAGE_NAME}" .
docker tag ${FULL_IMAGE_NAME} localhost:5000/${FULL_IMAGE_NAME}
docker push localhost:5000/${FULL_IMAGE_NAME}