FROM python:3.11.11-slim
LABEL maintainer "Vicky"

RUN mkdir -p /article_analyzer

# set working directory in the container
WORKDIR /article_analyzer
RUN pip install --upgrade pip


# copy the requirements file into the container
COPY requirements.txt .

# Copy the rest of the code into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]