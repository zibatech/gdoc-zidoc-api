from requests import get
from time import sleep

i = 1
while True:
    request = get(
        'http://localhost//api/expedientes?Dependencia=2&Serie=1&SubSerie=1',
        {
            'headers': {
                'Signature': 'FO5iQwp0iHpw8wRjl52Yimrufs9BL2GfW4mXdhT9SHs='
            }
        }
    )
    if request.ok:
        print(f'ping #{i}')
    sleep(60)
    i += 1
