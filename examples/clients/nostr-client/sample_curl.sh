curl -XPOST http://127.0.0.1:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": ["what is the current date and time?"],
    "thread_id": "123"
  }'