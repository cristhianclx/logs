# -*- coding: utf-8 -*-

from datetime import datetime
from sys import path as sys__path

from models.bucket import Bucket

data = [
    {
        "name": "store",
        "user_email": "cristhianclx@gmail.com",
        "created_at": datetime(2023, 1, 1),
        "updated_at": datetime(2023, 1, 1),
    },
    {
        "name": "items",
        "user_email": "cristhianclx@gmail.com",
        "created_at": datetime(2023, 1, 1),
        "updated_at": datetime(2023, 1, 1),
    },
]


sys__path.append("/code/")

from data.seed.base import load__data  # noqa:E402 pylint:disable=wrong-import-position

load__data(Bucket, Bucket.name, data, "name")
