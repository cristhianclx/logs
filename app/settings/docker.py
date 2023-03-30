# -*- coding: utf-8 -*-

from settings.base import *  # noqa:F401,F403 pylint:disable=wildcard-import,unused-wildcard-import

##
# stage
##

STAGE = "docker"

##
# database
##

DATABASE_URL: str = "postgresql://api:password@data:5432/bbdd"


##
# cache
##

CACHE_URL: str = "redis://cache:6379/0"


##
# immuDB
##

IMMUDB_URL: str = "logs:3322"
