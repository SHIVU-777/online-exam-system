@echo off
kubectl apply -f k8s\v1.yaml
kubectl apply -f k8s\v2.yaml
kubectl apply -f k8s\v3.yaml
echo.
echo Waiting for pods...
kubectl rollout status deployment/exam-v1 --timeout=120s
kubectl rollout status deployment/exam-v2 --timeout=120s
kubectl rollout status deployment/exam-v3 --timeout=120s
kubectl get deployments
kubectl get svc
echo.
echo Open: http://localhost:8081  http://localhost:8082  http://localhost:8083
start http://localhost:8081
start http://localhost:8082
start http://localhost:8083
pause
