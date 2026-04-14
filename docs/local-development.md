# Local Development

This document describes the Docker-only local setup for `mpt-api-python-client`.

Read [contributing.md](./contributing.md) for the repository workflow and
[usage.md](./usage.md) for installation and runtime examples.

## Prerequisites

- **Docker** and **Docker Compose** plugin (`docker compose` CLI)
- **Make**

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd mpt-api-python-client
```

### 2. Create environment configuration

```bash
cp .env.sample .env
```

Edit `.env` with your actual values. See [Environment Variables](#environment-variables) below.

### 3. Build the Docker images

```bash
make build
```

This builds the `app` image defined in [`compose.yaml`](../compose.yaml).

### 4. Verify the setup

```bash
make test
```

## Working In Docker

Use the repository make targets instead of ad hoc local Python commands.
For the full command catalog, see [usage.md](./usage.md) and [testing.md](./testing.md).

```bash
make bash      # open a shell in the app container
make run       # start an IPython session in the app container
```

## Environment Variables

Docker Compose loads environment variables from `.env`.

- Client variables are documented in [usage.md](./usage.md#configuration).
- E2E-specific variables are documented in [e2e_tests.md](./e2e_tests.md#environment-variables).

## Docker

The development environment runs entirely inside Docker:

- **Base image**: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- **Package manager**: [uv](https://docs.astral.sh/uv/)
- **Service**: `app`, defined in [`compose.yaml`](../compose.yaml), with the repository mounted at `/mpt_api_client`

## Make Targets

Run `make help` to see all available commands.

Shared references:

- [knowledge/make-targets.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/make-targets.md)
- [standards/makefiles.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/makefiles.md)


