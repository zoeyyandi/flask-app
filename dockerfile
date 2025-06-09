FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry==2.1.2

RUN poetry --version

RUN poetry install --no-root --no-dev

COPY . .

EXPOSE 4500

CMD ["poetry", "run", "python", "run.py"]