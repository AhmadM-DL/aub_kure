FROM python:3.12-slim


RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt .
COPY app.py .


RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]