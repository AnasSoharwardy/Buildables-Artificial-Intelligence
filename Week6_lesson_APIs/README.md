# API Tasks

## Task 1 – Flask API
**Run with terminal:**
```bash
cd Flask
python app.py
```

**Test Task 1:**
```bash
# Add todo
curl -X POST -H "Content-Type: application/json" -d '{"task":"Complete Buildables Week 6"}' http://127.0.0.1:5000/todos

# Get todos
curl http://127.0.0.1:5000/todos
```


## Task 2 – FastAPI
**Run with terminal:**
```bash
cd FastAPI
uvicorn main:app --reload
```

**Test Task 2:**

```bash
# Add todo
curl -X POST -H "Content-Type: application/json" -d '{"task":"Finish all tasks"}' http://127.0.0.1:8000/todos

# Get todos
curl http://127.0.0.1:8000/todos

```


## Task 3 - Extend FastAPI with Auth & DELETE Endpoint
**Run with terminal:**
```bash
cd Auth_(FastAPI)
uvicorn main:app --reload
```

**Test Task 3:**

```bash
# Add todo
curl -X POST -H "Content-Type: application/json" -d '{"task":"Complete Assignment"}' http://127.0.0.1:8000/todos

# Get todos
curl http://127.0.0.1:8000/todos

# Delete todo (requires API key)
curl -X DELETE -H "X-API-Key: secret" http://127.0.0.1:8000/todos/1

```
Or test via Swagger UI:
`
http://127.0.0.1:8000/docs
`

