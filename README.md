# Kubernetes Crawler

This app explores Kubernetes resources, creates a graph representing their dependencies and displays it using d3. Data is sent to the frontend over WebSockets.

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