FROM python:3.5

MAINTAINER  Robson Junior <bsao@icloud.com> (@bsao)

###########################################
#### INSTALL TOOLS
###########################################
RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libpq-dev cron build-essential
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf get-pip.py
RUN pip install "python-daemon<3.0"

###########################################
#### CREATE SPARK ENV
###########################################

LABEL version="spark_2.1.1_hadoop_2.7"
ARG JAVA_MAJOR_VERSION=8
ARG SPARK_VERSION="2.1.1"
ARG MAJOR_HADOOP_VERSION="2.7"
ARG SPARK_HOME="/opt/spark"

RUN \
  echo oracle-java${JAVA_MAJOR_VERSION}-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | \
    tee /etc/apt/sources.list.d/webupd8team-java.list && \
  echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | \
    tee -a /etc/apt/sources.list.d/webupd8team-java.list && \
  apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886 && \
  apt-get update && \
  apt-get install -y oracle-java${JAVA_MAJOR_VERSION}-installer oracle-java${JAVA_MAJOR_VERSION}-set-default && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /var/cache/oracle-jdk${JAVA_MAJOR_VERSION}-installer
ENV JAVA_HOME /usr/lib/jvm/java-${JAVA_MAJOR_VERSION}-oracle

RUN mkdir -p ${SPARK_HOME}
RUN wget http://d3kbcqa49mib13.cloudfront.net/spark-${SPARK_VERSION}-bin-hadoop${MAJOR_HADOOP_VERSION}.tgz
RUN tar -xvf spark-${SPARK_VERSION}-bin-hadoop${MAJOR_HADOOP_VERSION}.tgz -C ${SPARK_HOME} --strip=1
ENV SPARK_HOME ${SPARK_HOME}
ENV PYSPARK_PYTHON=python3

###########################################
#### CREATE USER TO RUN THE PIPELINE
###########################################
ARG user=app
ARG group=app
ARG uid=2101
ARG gid=2101

# The luigi app is run with user `app`, uid = 2101
RUN groupadd -g ${gid} ${group} \
    && useradd -u ${uid} -g ${group} -m -s /bin/bash ${user}

###########################################
#### CONFIGURE THE PIPELINE APP
###########################################
RUN mkdir -p /app
ADD ./requirements.txt /app
RUN pip install -r /app/requirements.txt
RUN rm /app/requirements.txt

##########################################
### PYTHON PATH
##########################################
ENV PYTHONPATH $PYTHONPATH:${SPARK_HOME}/python/lib/pyspark.zip:${SPARK_HOME}/python/lib/py4j-0.10.4-src.zip

##########################################
### WORKDIR
##########################################
WORKDIR /app
CMD ["/opt/spark/bin/pyspark"]
