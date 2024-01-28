# Use an official Conda runtime as a parent image
FROM python:3.11.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# Quelques librairies ne sont pas requirements.txt et doivent etre ajoutées
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Rend le posrt 8000 visible par host
EXPOSE 8000

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

