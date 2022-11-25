from requests import get
from time import sleep

i = 1
while True:
    request = get(
        'http://localhost:5000/api/expedientes?Dependencia=2&Serie=3',
        headers={
            'Signature': 'FO5iQwp0iHpw8wRjl52Yimrufs9BL2GfW4mXdhT9SHs='
        }
    )
    if request.ok:
        print(f'ping #{i}')
    sleep(600)
    i += 1
