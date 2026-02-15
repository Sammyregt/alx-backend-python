FROM python:3.10

WORKDIR /messaging_app


# Copy requirements
COPY requirements.txt .


# Install dependencies
RUN pip install -r requirements.txt


COPY . .

# Expose port
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
