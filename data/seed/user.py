# -*- coding: utf-8 -*-

from datetime import datetime
from sys import path as sys__path

from models.user import User

data = [
    {
        "email": "cristhianclx@gmail.com",
        "first_name": "Cristhian",
        "last_name": "Cueva",
        "password": "$2b$12$FkOr0xO/03GuT8n4pSCuIudAueua751QJ4C5ieKA0y/dBo9pY4Ex6",
        "is_active": True,
        "created_at": datetime(2023, 1, 1),
        "updated_at": datetime(2023, 1, 1),
    },
]


sys__path.append("/code/")

from data.seed.base import load__data  # noqa:E402 pylint:disable=wrong-import-position

load__data(User, User.email, data, "email")
