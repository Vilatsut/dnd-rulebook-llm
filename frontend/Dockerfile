# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip setuptools wheel --no-cache-dir \
	&& pip install --no-cache-dir gradio requests

# Copy the Gradio application code
COPY frontend.py .

# Make port 7860 available to the world outside this container
EXPOSE 7860

# Run the application
CMD ["python", "frontend.py"]
