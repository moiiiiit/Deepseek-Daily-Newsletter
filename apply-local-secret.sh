#!/bin/bash
# Apply local-secret.yaml as a Kubernetes secret
set -e
source_file="k8s/local-secret.yaml"
secret_name="deepseek-secrets"

if [ ! -f "$source_file" ]; then
  echo "local-secret.yaml not found!"
  exit 1
fi

api_key=$(grep DEEPSEEK_API_KEY "$source_file" | cut -d ':' -f2- | xargs)
if [ -z "$api_key" ]; then
  echo "DEEPSEEK_API_KEY not found in local-secret.yaml!"
  exit 1
fi

microk8s kubectl create secret generic $secret_name --from-literal=DEEPSEEK_API_KEY="$api_key" --dry-run=client -o yaml | microk8s kubectl apply -f -
echo "Kubernetes secret '$secret_name' applied from local-secret.yaml."