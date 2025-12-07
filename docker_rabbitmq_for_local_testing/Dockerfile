# Use the official RabbitMQ base image
FROM rabbitmq:3.9.29-management

# Set environment variables for RabbitMQ
# Example: default user, password, and enabling plugins
ENV RABBITMQ_DEFAULT_USER=admin
ENV RABBITMQ_DEFAULT_PASS=admin
ENV RABBITMQ_DEFAULT_VHOST=/

# (Optional) Copy custom configuration file to the container
# Uncomment if you have a custom rabbitmq.conf
# COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

# (Optional) Enable additional RabbitMQ plugins
RUN rabbitmq-plugins enable --offline rabbitmq_stomp rabbitmq_shovel rabbitmq_shovel_management

# Expose ports
# 5672: RabbitMQ messaging
# 15672: RabbitMQ Management UI
EXPOSE 5672 15672

# Start RabbitMQ server
CMD ["rabbitmq-server"]
