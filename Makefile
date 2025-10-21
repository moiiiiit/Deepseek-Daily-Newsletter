apply-local-secret:
	bash apply-local-secret.sh

apply-manifests:
	microk8s kubectl apply -f k8s/

setup:
	make apply-local-secret
	make apply-manifests
