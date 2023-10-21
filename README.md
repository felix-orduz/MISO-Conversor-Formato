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
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzgyNzIzNSwianRpIjoiMzBlMTQ0YmItY2EyOC00OTExLThhYjktZTI0OTg0Njk2YWRjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZvcmR1eiIsIm5iZiI6MTY5NzgyNzIzNSwiZXhwIjoxNjk3ODI4MTM1fQ.KhqcuFJNYaYLSTm9TTL4-fiQ4LEO4DkbEy-iStlmVmQ'
```

```bash
curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5Nzg0NTA3OSwianRpIjoiZGVlM2NiMjYtYWJjMC00NDNhLThlM2EtYjgyNDI4MTY2ZWUxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZvcmR1eiIsIm5iZiI6MTY5Nzg0NTA3OSwiZXhwIjoxNjk3ODQ1OTc5fQ.PL2VwZ7fB0Awg3uknrZpFCvNWGeJ6keoP2qAWeH7tZI"  -F "file=@/Users/felixernestoorduzgrimaldo/Downloads/file_example_MP4_480_1_5MG.mp4" -F "newFormat=avi" http://localhost:5001/api/tasks
```

```bash
curl -X GET \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5Nzg0NTA3OSwianRpIjoiZGVlM2NiMjYtYWJjMC00NDNhLThlM2EtYjgyNDI4MTY2ZWUxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZvcmR1eiIsIm5iZiI6MTY5Nzg0NTA3OSwiZXhwIjoxNjk3ODQ1OTc5fQ.PL2VwZ7fB0Awg3uknrZpFCvNWGeJ6keoP2qAWeH7tZI" \
     http://localhost:5001/api/tasks/1
```

```bash
curl -X GET \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5Nzg0NTA3OSwianRpIjoiZGVlM2NiMjYtYWJjMC00NDNhLThlM2EtYjgyNDI4MTY2ZWUxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZvcmR1eiIsIm5iZiI6MTY5Nzg0NTA3OSwiZXhwIjoxNjk3ODQ1OTc5fQ.PL2VwZ7fB0Awg3uknrZpFCvNWGeJ6keoP2qAWeH7tZI" \
     http://localhost:5001/api/tasks
```

```bash
curl -X DELETE \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5Nzg0NTA3OSwianRpIjoiZGVlM2NiMjYtYWJjMC00NDNhLThlM2EtYjgyNDI4MTY2ZWUxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZvcmR1eiIsIm5iZiI6MTY5Nzg0NTA3OSwiZXhwIjoxNjk3ODQ1OTc5fQ.PL2VwZ7fB0Awg3uknrZpFCvNWGeJ6keoP2qAWeH7tZI" \
     http://localhost:5001/api/tasks/1
``````
