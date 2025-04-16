FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

COPY . .

# Run the application
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]