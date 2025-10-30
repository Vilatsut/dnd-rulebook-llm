# Dockerfile.system
FROM python:3.12-slim-bookworm

# set working dir to project root
WORKDIR /app

# make python quiet and deterministic
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install build tools if any packages need compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates && rm -rf /var/lib/apt/lists/*

# copy dependency files first for better layer caching
COPY pyproject.toml uv.lock* ./

# upgrade pip and install project (reads pyproject.toml)
ENV PIP_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cpu
RUN pip install --upgrade pip setuptools wheel \
    && pip install .

# copy application code
COPY . .

# expose port used by uvicorn
EXPOSE 8000

# run uvicorn (do not use --reload in production)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]