# MISO-Conversor-Formato

```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    export DATABASE_URL=postgresql://postgres:postgrespwd@127.0.0.1:5432/conversor
    flask run --port 5001 --debug
```

```bash
curl -X POST \
  http://127.0.0.1:5001/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "forduz",
    "password": "12345"
}'
```

```bash
curl -X GET \
  http://127.0.0.1:5001/api/tasks \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5Nzc2Mjc4MCwianRpIjoiODAxMmI5OGUtZTBiNS00NWFmLWJmYWEtMmY0NWZhN2FhYzlkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZvcmR1eiIsIm5iZiI6MTY5Nzc2Mjc4MCwiZXhwIjoxNjk3NzYzNjgwfQ.hR_Pp7M5si76xoxp6nhV_G2MawVIhOVwh7P-bT-n3as'
```
