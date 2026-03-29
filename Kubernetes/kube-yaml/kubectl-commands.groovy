
Nodes:
-------

    . Nodes are the worker machines in Kubernetes that run the containerized applications.
    . They can be physical or virtual machines, and each node runs a container runtime, such as Docker, along with the necessary Kubernetes components.
    . Nodes are responsible for running the pods and providing the necessary resources, such as CPU, memory, and storage, to the applications.
    . Each node is managed by the Kubernetes control plane, which schedules the pods to run on the appropriate nodes based on resource availability and other constraints.

    > kubectl get nodes -o wide


-------------------------------------------------------------------------------------

Pods:
-----

    . Pods are the smallest deployable units in Kubernetes that can be created, scheduled, and managed.
    . A pod can contain one or more containers that share the same network namespace and storage volumes.
    . Pods are ephemeral and can be created, destroyed, and recreated by Kubernetes as needed.

    > kubectl apply -f kube-yaml/pods/mysql-pod.yaml

    > kubectl get pods
    > kubectl get pods -o wide
    > kubectl describe pod mysql-pod


    > kubectl exec -it mysql-pod -- sh # Access the shell of the mysql-pod
    > kubectl exec -it mysql-pod -- /bin/sh # Access the shell of the mysql-pod
    > kubectl exec -it mysql-pod -- /bin/sh -c "ls /" # List the files in the root directory of the mysql-pod
    > kubectl logs mysql-pod # View the logs of the mysql-pod

    > mysql -u root -p 
    > password: root

    > Mysql commands


    

-------------------------------------------------------------------------------------

Deployments:
------------
    . Deployments are used to manage the lifecycle of pods. 
    . They provide features like rolling updates, scaling, and self-healing.
    . A deployment ensures that a specified number of pod replicas are running at any given time.
    . You can update the deployment to change the pod template, and Kubernetes will automatically roll out the changes.
    . Can maintain version history of the application, allowing you to roll back to a previous version if needed.

    > kubectl apply -f kube-yaml/deployment/mysql-deployment.yaml

    > kubectl scale deployment mysql-deployment --replicas=3 # If 0 no pods will be created
    > kubectl get deployments
    > kubectl describe deployment mysql-deployment
    > kubectl delete deployment mysql-deployment
    > kubectl rollout history deployment mysql-deployment
    > kubectl rollout undo deployment mysql-deployment --to-revision=1

    > kubectl exec -it mysql-pod -- sh # Access the shell of the pod

    > kubectl get svc
    > kubectl describe pod -l app=front-deployment-pod

-------------------------------------------------------------------------------------


Services:
----------

    . Services are used to expose the application running in the pods to the outside world or to other pods within the cluster.
    . They provide a stable IP address and DNS name for the pods, allowing other components to communicate with them.
    . Services can be of different types, such as ClusterIP (default), NodePort, LoadBalancer, and ExternalName.
    . Services can also perform load balancing across multiple pod replicas.

    > kubectl apply -f kube-yaml/services/mysql-service.yaml
    > kubectl get services
    > kubectl delete service mysql-service
    > kubectl describe service mysql-service
    > kubectl get endpoints mysql-service

    > kubectl get svc
    > kubectl port-forward svc/front-service 8080:80 # Access the front-end application running in the cluster on localhost:8080


-------------------------------------------------------------------------------------

ConfigMaps:

    . ConfigMaps are used to store configuration data in key-value pairs. 
    . They allow you to decouple configuration from the application code, making it easier to manage and update configurations without redeploying the application.
    . ConfigMaps can be consumed by pods as environment variables, command-line arguments, or as configuration files mounted as volumes.

    > kubectl apply -f kube-yaml/config-map/back-config.yaml
    > kubectl get configmaps
    > kubectl describe configmap back-config
    > kubectl delete configmap back-config
    > kubectl create configmap <cm-name>   --from-file=Application.yml



-------------------------------------------------------------------------------------

StatefulSets:

    . StatefulSets are used to manage stateful applications that require stable network identities and persistent storage.
    . They provide features like stable pod names, ordered deployment and scaling, and persistent storage management.
    . StatefulSets are typically used for applications like databases, where each pod needs to maintain its own state.

    > kubectl apply -f kube-yaml/statefulset/back-stateful.yaml
    > kubectl get statefulsets
    > kubectl describe statefulset back-stateful
    > kubectl delete statefulset back-stateful

    > kubectl exec -it mysql-pod -- sh # Access the shell of the pod

    # Backend Application can be use Mysql using the below
        > jdbc:mysql://mysql-0.mysql:3306/db
            # mysql-0 is the pod name
            # mysql is the service name. 
            # This is possible because of the stable network identity provided by StatefulSets and the service discovery mechanism in Kubernetes.

-------------------------------------------------------------------------------------

kubectl apply -f kube-yaml/deployment/front-deployment.yaml
kubectl apply -f kube-yaml/services/front-service.yaml
kubectl apply -f kube-yaml/config-map/front-config.yaml

