# Local Development

This document describes how to set up and run `mpt-api-python-client` locally.

Make sure you have read the [Contributing guidelines](./contributing.md)

## Prerequisites

- **Docker** and **Docker Compose** plugin (`docker compose` CLI)
- **Make**
- [CodeRabbit CLI](https://www.coderabbit.ai/cli) (optional — used for running review checks locally)

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

This creates the Docker images with all required dependencies and the virtual environment.

### 4. Verify the setup

```bash
make test
```

## Running the Client

Start an interactive IPython session with the client available:

```bash
make run
```

Ensure your `.env` file is populated with valid `MPT_API_BASE_URL` and `MPT_API_TOKEN` values.

## Environment Variables

### Application

| Variable           | Default | Example                              | Description                       |
|--------------------|---------|--------------------------------------|-----------------------------------|
| `MPT_API_BASE_URL` | —       | `https://portal.softwareone.com/mpt` | SoftwareONE Marketplace API URL   |
| `MPT_API_TOKEN`    | —       | `eyJhbGciOiJSUzI1N...`               | SoftwareONE Marketplace API Token |

### End-to-End Testing

| Variable                   | Default | Example                            | Description              |
|----------------------------|---------|------------------------------------|--------------------------|
| `MPT_API_TOKEN_CLIENT`     | —       | `eyJhbGciOiJSUzI1N...`             | Client API token         |
| `MPT_API_TOKEN_OPERATIONS` | —       | `eyJhbGciOiJSUzI1N...`             | Operations API token     |
| `MPT_API_TOKEN_VENDOR`     | —       | `eyJhbGciOiJSUzI1N...`             | Vendor API token         |
| `RP_API_KEY`               | —       | `pytest_XXXX`                      | ReportPortal API key     |
| `RP_ENDPOINT`              | —       | `https://reportportal.example.com` | ReportPortal endpoint    |
| `RP_LAUNCH`                | —       | `dev-env`                          | ReportPortal launch name |

## Docker

The development environment runs entirely inside Docker:

- **Base image**: `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- **Package manager**: [uv](https://docs.astral.sh/uv/)
- **Services**: defined in `compose.yaml` — a single `app` service that mounts the project directory.

## Make Targets

Common development workflows are wrapped in the Makefile. Run `make help` to see all available
commands.

[Read make targets for additional information](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/make-targets.md)

### How the Makefile Works

[Read the makefile architecture for python repositories](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/makefiles.md)

# Additional Resources
- [Package architecture](./architecture.md)
- [Python coding standards](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/python-coding.md)
- [Extensions best practices](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/extensions-best-practices.md)
- [Packages and dependencies](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/packages-and-dependencies.md)
- [Testing](./testing.md)
  - [Unit tests](./unit_tests.md)
  - [E2E tests](./e2e_tests.md)
- [Pull requests](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/pull-requests.md)
- [Makefiles](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/makefiles.md)
  - [Makefile targets](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/make-targets.md)




