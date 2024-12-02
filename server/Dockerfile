FROM python:3.13

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY /management.py management.py
CMD ["flask", "run"]