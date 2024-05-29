# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install numpy
RUN pip install numpy
RUN pip install pillow

# Copy the entire application code into the container
COPY . .

# Install uvicorn
RUN pip install uvicorn

# Set the PYTHONPATH environment variable to include the current directory
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Make port 8002 available to the world outside this container
EXPOSE 8002

# Run the command to start uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]