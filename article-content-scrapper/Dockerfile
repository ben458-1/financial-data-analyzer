FROM python:3.11.11-slim
LABEL maintainer="Vicky"

USER root
ENV ACCEPT_EULA=Y
COPY ./bash_scripts.sh ./bash_scripts.sh
RUN chmod +x /bash_scripts.sh
RUN ./bash_scripts.sh
ENV LANG en_US.UTF-8

RUN mkdir -p /article-content-scrapper

# set working directory in the container
WORKDIR /article-content-scrapper
RUN pip install --upgrade pip


# copy the requirements file into the container
COPY requirements.txt .

# Copy the rest of the code into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install PyAutoGUI

# Set display port and dbus env to avoid hanging
#ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null

# Expose the port the app runs on
EXPOSE 9005

CMD ["/bin/bash", "run.sh"]
