import requests

for i in range(100):
    requests.post('http://localhost:8080/youtube', json={
        'text': 'let it be'
    })


