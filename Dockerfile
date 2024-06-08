FROM python:3.12-slim

RUN pip install --no-cache-dir poetry==1.8.3

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --without dev --no-root

COPY main.py ./main.py
COPY src ./src
RUN mkdir -p /app/data

RUN poetry install --without dev

CMD ["bash"]
