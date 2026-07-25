FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend/src /app/src
COPY company_profiles /app/company_profiles

ENV PYTHONPATH=/app/src
EXPOSE 8000

CMD ["uvicorn", "careermatch_ai.main:app", "--host", "0.0.0.0", "--port", "8000"]
