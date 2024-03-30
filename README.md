# Kubernetes Crawler

This app explores Kubernetes resource, creates a graph representing their dependencies and displays it using d3.

## Prerequisites

- poetry
- pnpm

## Running

Install dependencies
```shell
make install
```

In separate terminals:
```shell
make backend
```

```shell
make frontend
```

## Demo app
To populate the kubernetes environment with objects run `make install-otel-demo`