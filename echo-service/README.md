# Echo Service

Build and run
```bash
docker build -f docker/Dockerfile -t echo-service .
docker run --rm -p 5001:5001 echo-service:latest
```
Access `http://127.0.0.1:5001/` and `http://127.0.0.1:5001/api/echo`