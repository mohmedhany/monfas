FROM python:3.12

# Set the working directory in the container to /app
WORKDIR /app

COPY . /app
# Copy the requirements file
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir  -r requirements.txt

# Copy the application code
COPY ./app /code/app

# Run the command to start the development server when the container launches
CMD ["uvicorn", "app.main:app" , "--host","0.0.0.0","--port","8000"]