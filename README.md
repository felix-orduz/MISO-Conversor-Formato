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
curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzgzMzY0NCwianRpIjoiMjRhNTRjMWYtODU3ZS00ZjU2LTk1NTEtZTExN2EzMzNkNzZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZvcmR1eiIsIm5iZiI6MTY5NzgzMzY0NCwiZXhwIjoxNjk3ODM0NTQ0fQ.QWGLqiCdbzjPily2H7w0sm9LJIvpaTvVrtrq0X8NCyE"  -F "file=@/Users/felixernestoorduzgrimaldo/Downloads/file_example_MP4_480_1_5MG.mp4" -F "newFormat=avi" http://localhost:5001/api/tasks
```
