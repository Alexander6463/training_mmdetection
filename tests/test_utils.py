import os

from unittest.mock import patch

from components.train import utils


@patch.object(utils, "Minio")
def test_create_client_minio(MockMinio):
    client = utils.create_client_minio("service", "login", "password")
    MockMinio.assert_called_once_with("service", "login", "password", secure=False)
    assert client is MockMinio()


@patch.object(utils, "Minio")
def test_download_from_path(MockMinio, monkeypatch):
    envs = {"MINIO_SERVER": "SERVER", "ACCESS_KEY": "LOGIN", "SECRET_KEY": "PASSWORD"}
    monkeypatch.setattr(os, "environ", envs)
    utils.download_from_path("minio://datasets/data.tar.gz", "data.tar.gz")
    MockMinio.assert_called_once_with("SERVER", "LOGIN", "PASSWORD", secure=False)
    MockMinio().fget_object.assert_called_once_with(
        "datasets", "data.tar.gz", "data.tar.gz"
    )
