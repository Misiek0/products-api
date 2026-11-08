FROM python:3.12-slim

# Logi Pythona od razu na stdout, widoczne w `docker compose logs`
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kod dopiero po zależnościach (zmienia się najczęściej).
COPY app ./app

# W compose jest nadpisywane komendą z --reload.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]