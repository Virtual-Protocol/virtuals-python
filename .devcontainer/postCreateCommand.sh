#! /usr/bin/env bash

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Install Dependencies
uv sync --dev

# Install and configure pre-commit
echo "Installing and configuring pre-commit..."
uv pip install pre-commit
uv run pre-commit install --install-hooks
