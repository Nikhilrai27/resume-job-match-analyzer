FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt /app/requirements-backend.txt
RUN pip install --no-cache-dir -r /app/requirements-backend.txt streamlit

COPY backend/src /app/backend/src
COPY company_profiles /app/company_profiles
COPY frontend_streamlit/app.py /app/frontend_streamlit/app.py

ENV PYTHONPATH=/app/backend/src
EXPOSE 8501

CMD ["streamlit", "run", "frontend_streamlit/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
