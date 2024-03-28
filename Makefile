.PHONY: backend
backend:
	pushd backend && poetry run uvicorn main:app --reload

.PHONY: frontend
frontend:
	pushd frontend && pnpm start

.PHONY: install
install:
	pushd frontend && pnpm install && popd && pushd backend && poetry install