# Info

Showcases the (Metacontroller)[https://github.com/GoogleCloudPlatform/metacontroller] infinite loop problem when using ClusterRole with namespace property. Of course, ClusterRole with a namespace is not valid k8s, but an infinite loop is not really helpful in finding out the issue. 

# How to reproduce

``` bash
# install metacontroller, then:
kubectl apply -f deploy
kubectl create configmap super-namespace-controller --from-file=sync.py
kubectl apply -f webhook.yaml

# now attach to metacontroller logs, e.g.
kubectl logs metacontroller-0 -n metacontroller -f

# deploy and observe logs in metacontroller
kubectl apply -f super-namespace.yaml
```

You should see the metacontroller stuck in an infinite loop:

I0614 08:43:27.171177       1 controller.go:406] sync SuperNamespace /test
I0614 08:43:27.175649       1 manage_children.go:171] SuperNamespace test: deleting ClusterRole test-ns-my-special-role
I0614 08:43:27.365996       1 request.go:485] Throttling request took 190.228619ms, request: DELETE:https://172.20.0.1:443/apis/rbac.authorization.k8s.io/v1/clusterroles/test-ns-my-special-role
I0614 08:43:27.379378       1 controller.go:368] SuperNamespace /test: child ClusterRole test-ns-my-special-role deleted
I0614 08:43:27.379474       1 manage_children.go:254] SuperNamespace test: creating ClusterRole test-ns/test-ns-my-special-role
I0614 08:43:27.565995       1 request.go:485] Throttling request took 185.436921ms, request: POST:https://172.20.0.1:443/apis/rbac.authorization.k8s.io/v1/clusterroles
I0614 08:43:27.592928       1 controller.go:307] SuperNamespace /test: child ClusterRole test-ns-my-special-role created or updated
I0614 08:43:27.765972       1 request.go:485] Throttling request took 173.019227ms, request: GET:https://172.20.0.1:443/apis/conplement.cloud/v1/supernamespaces/test
I0614 08:43:27.769416       1 controller.go:406] sync SuperNamespace /test
I0614 08:43:27.778921       1 manage_children.go:171] SuperNamespace test: deleting ClusterRole test-ns-my-special-role
I0614 08:43:27.965841       1 request.go:485] Throttling request took 186.853221ms, request: DELETE:https://172.20.0.1:443/apis/rbac.authorization.k8s.io/v1/clusterroles/test-ns-my-special-role
I0614 08:43:27.981555       1 controller.go:368] SuperNamespace /test: child ClusterRole test-ns-my-special-role deleted
I0614 08:43:27.981716       1 manage_children.go:254] SuperNamespace test: creating ClusterRole test-ns/test-ns-my-special-role
I0614 08:43:28.165856       1 request.go:485] Throttling request took 184.032122ms, request: POST:https://172.20.0.1:443/apis/rbac.authorization.k8s.io/v1/clusterroles
I0614 08:43:28.187942       1 controller.go:307] SuperNamespace /test: child ClusterRole test-ns-my-special-role created or updated
I0614 08:43:28.365880       1 request.go:485] Throttling request took 177.598024ms, request: GET:https://172.20.0.1:443/apis/conplement.cloud/v1/supernamespaces/test
I0614 08:43:28.376124       1 controller.go:406] sync SuperNamespace /test
I0614 08:43:28.386813       1 manage_children.go:171] SuperNamespace test: deleting ClusterRole test-ns-my-special-role
I0614 08:43:28.565868       1 request.go:485] Throttling request took 178.986724ms, request: DELETE:https://172.20.0.1:443/apis/rbac.authorization.k8s.io/v1/clusterroles/test-ns-my-special-role
I0614 08:43:28.575654       1 controller.go:368] SuperNamespace /test: child ClusterRole test-ns-my-special-role deleted
I0614 08:43:28.575954       1 manage_children.go:254] SuperNamespace test: creating ClusterRole test-ns/test-ns-my-special-role
I0614 08:43:28.765844       1 request.go:485] Throttling request took 188.104921ms, request: POST:https://172.20.0.1:443/apis/rbac.authorization.k8s.io/v1/clusterroles
I0614 08:43:28.781693       1 controller.go:307] SuperNamespace /test: child ClusterRole test-ns-my-special-role created or updated
I0614 08:43:28.965869       1 request.go:485] Throttling request took 183.927322ms, request: GET:https://172.20.0.1:443/apis/conplement.cloud/v1/supernamespaces/test
I0614 08:43:28.970025       1 controller.go:406] sync SuperNamespace /test
I0614 08:43:28.979548       1 manage_children.go:171] SuperNamespace test: deleting ClusterRole test-ns-my-special-role
I0614 08:43:29.165881       1 request.go:485] Throttling request took 186.267721ms, request: DELETE:https://172.20.0.1:443/apis/rbac.authorization.k8s.io/v1/clusterroles/test-ns-my-special-role
I0614 08:43:29.177726       1 controller.go:368] SuperNamespace /test: child ClusterRole test-ns-my-special-role deleted
I0614 08:43:29.177768       1 manage_children.go:254] SuperNamespace test: creating ClusterRole test-ns/test-ns-my-special-role
I0614 08:43:29.365933       1 request.go:485] Throttling request took 187.85522ms, request: POST:https://172.20.0.1:443/apis/rbac.authorization.k8s.io/v1/clusterroles
I0614 08:43:29.381154       1 controller.go:307] SuperNamespace /test: child ClusterRole test-ns-my-special-role created or updated
I0614 08:43:29.565839       1 request.go:485] Throttling request took 184.137722ms, request: GET:https://172.20.0.1:443/apis/conplement.cloud/v1/supernamespaces/test
I0614 08:43:29.569764       1 controller.go:406] sync SuperNamespace /test
I0614 08:43:29.577355       1 manage_children.go:171] SuperNamespace test: deleting ClusterRole test-ns-my-special-role
I0614 08:43:29.765891       1 request.go:485] Throttling request took 187.92552ms, request: DELETE:https://172.20.0.1:443/apis/rbac.authorization.k8s.io/v1/clusterroles/test-ns-my-special-role
I0614 08:43:29.780775       1 manage_children.go:254] SuperNamespace test: creating ClusterRole test-ns/test-ns-my-special-role
I0614 08:43:29.780777       1 controller.go:368] SuperNamespace /test: child ClusterRole test-ns-my-special-role deleted
I0614 08:43:29.965832       1 request.go:485] Throttling request took 184.767322ms, request: POST:https://172.20.0.1:443/apis/rbac.authorization.k8s.io/v1/clusterroles
I0614 08:43:29.983982       1 controller.go:307] SuperNamespace /test: child ClusterRole test-ns-my-special-role created or updated
I0614 08:43:30.165836       1 request.go:485] Throttling request took 181.898923ms, request: GET:https://172.20.0.1:443/apis/conplement.cloud/v1/supernamespaces/test
I0614 08:43:30.184874       1 controller.go:406] sync SuperNamespace /test
