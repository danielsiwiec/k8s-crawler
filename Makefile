.PHONY: backend
backend:
	pushd backend && poetry run uvicorn main:app --reload

.PHONY: frontend
frontend:
	pushd frontend && pnpm start

.PHONY: install
install:
	pushd frontend && pnpm install && popd && pushd backend && poetry install


.PHONY: install-otel-demo
install-otel-demo:
	helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts && helm upgrade --install my-otel-demo open-telemetry/opentelemetry-demo -n otel-demo --create-namespace