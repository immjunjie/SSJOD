FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip && pip install pipenv

COPY Pipfile* ./

RUN pipenv install --system --deploy --ignore-pipfile

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.simulator.main:app", "--host", "0.0.0.0", "--port", "8000"]