# -*- coding: utf-8 -*-
"""This module is for commonly shared pydantic basemodels.

"""
import pydantic


class Pagination(pydantic.BaseModel):
    more: bool
    total: int
