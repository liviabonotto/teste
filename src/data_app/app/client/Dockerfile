FROM python:3.12.4-slim

RUN pip install poetry

COPY . .

RUN poetry install --no-cache

EXPOSE 5000 8501

CMD [ "poetry", "run", "streamlit", "run", "./app.py"]