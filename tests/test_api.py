import os
import tempfile

import pytest
import requests

from coronataiou import

URL = "http://127.0.0.1:5000/api/v1/name"
PARAMS = {'name': 'Joseph'}

r = requests.get(url=URL, params=PARAMS)
print(r)
