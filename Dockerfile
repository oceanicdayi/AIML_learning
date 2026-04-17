FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and knowledge files
COPY app.py .
COPY ai_tech_map_report.md .
COPY anki_terms.csv .
COPY readme.md .
COPY README_HF.md .
COPY Group*/ ./

# HF Spaces expects port 7860
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860
EXPOSE 7860

CMD ["python", "app.py"]
