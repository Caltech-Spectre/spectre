FROM centos:7

MAINTAINER IMSS ADS <imss-ads-staff@caltech.edu>

USER root

#RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh && echo -e "StrictHostKeyChecking no" > /root/.ssh/config
#ADD jenkins.key /root/.ssh/id_rsa
#RUN chmod 0600 /root/.ssh/id_rsa && echo "IdentityFile /root/.ssh/id_rsa" >> /root/.ssh/config

RUN yum -y install epel-release && yum -y makecache fast && yum -y update && yum -y install \
    gcc \
    git \
    openssl-devel \
    mod_ssl \
    mysql-devel \
    nginx \
    python36 \
    python36-devel \
    && yum -y clean all

RUN ln -s /usr/bin/python3.6 /usr/bin/python3
RUN ln -s /usr/bin/pip3.6 /usr/bin/pip3

# set our timezone to pacific time
WORKDIR /etc
RUN rm -rf localtime && ln -s /usr/share/zoneinfo/America/Los_Angeles localtime

RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" && python get-pip.py

# ---------------
# Supervisord
# ---------------
RUN pip install supervisor
COPY etc/docker/supervisord.conf /etc/supervisord.conf

# ---------------
# Entrypoint
# ---------------
RUN pip install awscli

# ---------------
# django_imss
# ---------------
ENV PYCURL_SSL_LIBRARY=nss
RUN python3 -m venv /spectreve
ENV PATH /spectreve/bin:$PATH
COPY . /spectre
WORKDIR /spectre
RUN pip3 install --upgrade pip && pip3 install -r /spectre/requirements.txt && \
    pip3 install -e . && \
    cp /spectre/etc/docker/gunicorn_logging.conf /etc/gunicorn_logging.conf && \
#    cp /spectre/etc/docker/context.conf /etc/context.conf && \
    python manage.py collectstatic --noinput

# ----------------
# nginx
# ----------------
COPY etc/docker/nginx.conf /etc/nginx/nginx.conf
RUN mkdir /spectre_certs
RUN cp /etc/pki/tls/private/localhost.key /spectre_certs
RUN cp /etc/pki/tls/certs/localhost.crt /spectre_certs
RUN chmod a+r /spectre_certs/*

RUN adduser -r gunicorn

EXPOSE 80 443 8042

ENTRYPOINT ["deploy", "entrypoint"]
