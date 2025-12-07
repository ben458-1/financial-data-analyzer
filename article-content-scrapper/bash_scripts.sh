curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | tee /etc/apt/sources.list.d/msprod.list
apt update
ENV ACCEPT_EULA y
ENV DEBIAN_FRONTEND noninteractive

apt-get update && apt-get install -y curl wget nano -y
apt-get install -y apt-transport-https
#RUN hostname local-postgres-dfm
apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y

sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
#ENV LANG en_US.UTF-8


### Chrome
apt-get update -y && apt-get install -y chromium xvfb python3-tk python3-dev

wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt -f install -y
