from requests import get
from time import sleep

i = 1
while True:
    request = get(
        'http://localhost//api/expedientes?Dependencia=2&Serie=1&SubSerie=1'
    )
    if request.ok:
        print(f'ping #{i}')
    i += 1
