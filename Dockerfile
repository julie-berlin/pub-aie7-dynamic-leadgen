# https://medium.com/@devsjc/the-complete-guide-to-pyproject-toml-replace-setup-py-and-requirements-txt-553f899dc267
# Create a virtual environment and install dependencies
# * Only re-execute this step when pyproject.toml changes
FROM python:3.12 AS build-reqs
WORKDIR /app
COPY pyproject.toml pyproject.toml
RUN python -m venv /venv
RUN /venv/bin/python -m pip install -U setuptools wheel
RUN /venv/bin/pip install -q .

# Build binary for the package and install code
# * The README.md is required for the long description
FROM build-reqs AS build-app
COPY src src
COPY README.md README.md
RUN /venv/bin/pip install .

# Copy the virtualenv into a distroless image
# * These are small images that only contain the runtime dependencies
FROM gcr.io/distroless/python3-debian11
WORKDIR /app
COPY --from=build-app /venv /venv
ENTRYPOINT ["/venv/bin/coolprojectcli"]








# FROM python:3.12

# WORKDIR /code

# COPY ./pyproject.toml /code/pyproject.toml

# # RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./src /code

# CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "80"]
