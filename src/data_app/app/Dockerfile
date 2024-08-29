FROM python:3.12.4-slim

RUN pip install poetry

COPY . .

RUN poetry install --no-cache

CMD [ "poetry", "run", "python", "./app.py" ]

CMD ["poetry", "run", "sh", "-c", "flask run --host=0.0.0.0 & streamlit run data_pipeline/streamlit_app.py --server.port 8501"]
