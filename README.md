# Metrics viewer

An application that shows metrics aggregation with backend and frontend. See: http://metrics-viewer.com. 

It's deployed on AWS EKS with Application load balancing Controller and Route 53 as a DNS server.

## Environment setting

To create a new virtual environment with all dependencies in it, execute (virtualenv should be installed):
```commandline
make env-create
```

## Formatting and linting

To apply isort and black, execute:
```commandline
make format
```

To check isort, black (without changing files) and flake8, execute:
```commandline
make check-lint
```

## Developing

To run the whole application with docker-compose, execute:
```commandline
make dev-compose-up
```

The swagger for API will be available at link http://localhost:8004/api/docs, frontend will be available at http://localhost:8502. Variables for development (ports, prefixes, api key, etc) can be changed in [.env-dev file](.env-dev).

To shut down the application, execute:
```commandline
make dev-compose-down
```

To debug parts of application, a script should be run from [root directory](.), environmental variables will be loaded from [.env-dev file](.env-dev). Workarounds for this:
```commandline
make run-frontend
```
```commandline
make run-backend
```

## Migrations

To make a revision, run:
```commandline
NAME=[name of revision] make db-revision
```

To downgrade:
```commandline
make db-downgrade
```

To upgrade (it happens automatically when docker-compose is up):
```commandline
make db-migrate
```

## Deploying

Prerequisites:
* k8s cluster
* namespace ("metrics" by default, can be changed in [Makefile](Makefile))
* installed kubectl and helm

Create k8s Secret `kube-secret.yml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: metrics-secret
  namespace: metrics
stringData:
  POSTGRES_USER: 
  POSTGRES_PASSWORD: 
  POSTGRES_NAME: 
  API_KEY: 
```
Apply it:
```commandline
kubectl apply -f kube-secret.yml
```

Push images to registry (change DOCKER_REGISTRY in [.env-dev](.env-dev)):
```commandline
make dev-compose-push
```

To deploy application, run:
```commandline
make helm-install
```
To uninstall:
```commandline
make helm-uninstall
```

## Further plans

- [ ] Skaffold for more convenient testing
- [ ] CI/CD for deploying, automatic tests and linters
- [ ] Logging
- [ ] Monitoring
- [ ] Move to external DB
- [ ] Prepare raw data automatically
- [ ] Consider different DB
