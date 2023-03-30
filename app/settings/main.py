# -*- coding: utf-8 -*-

from ssm_parameter_store import EC2ParameterStore

from settings.base import *  # noqa:F401,F403 pylint:disable=wildcard-import,unused-wildcard-import

SSM_REGION = "us-east-1"

store = EC2ParameterStore(region_name=SSM_REGION)


##
# stage
##

STAGE = "main"

parameters = store.get_parameters_with_hierarchy(f"/logs.demo.pe/{STAGE}/")


##
# database
##

DATABASE_URL: str = "postgresql://{}:{}@{}:{}/{}".format(  # pylint:disable=consider-using-f-string
    parameters["database"]["user"],
    parameters["database"]["password"],
    parameters["database"]["host"],
    parameters["database"]["port"],
    parameters["database"]["name"],
)


##
# cache
##

CACHE_URL: str = "redis://{}:{}/0".format(  # pylint:disable=consider-using-f-string
    parameters["cache"]["host"],
    parameters["cache"]["port"],
)


##
# immuDB
##

IMMUDB_URL: str = "{}:{}".format(  # pylint:disable=consider-using-f-string
    parameters["logs"]["host"],
    parameters["logs"]["port"],
)
