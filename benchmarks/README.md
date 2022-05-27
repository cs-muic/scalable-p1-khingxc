## How To Load Test

### Kubernetes Stage

#### - kubectl apply -f .  : to create all deployments
#### - helm upgrade --install traefik traefik/traefik : for ingress
#### - kubectl get po : to check all pods  

### Locust Stage
#### - locust -H http://127.0.0.1 -u 30 -r 2 Benchmarks
#### *Remark* : 30 is the number of users | 2 is number of spawn rate | Benchmarks is the name of the class of locustfile.py
