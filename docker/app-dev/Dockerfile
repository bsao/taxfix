FROM bsao/app-base:latest
MAINTAINER  Robson Junior <bsao@icloud.com> (@bsao)

###########################################
#### CONFIGURE THE PIPELINE APP
###########################################
ADD ./requirements_dev.txt /app
RUN pip install -r /app/requirements_dev.txt
RUN rm /app/requirements_dev.txt

##########################################
### TEST LIBS
##########################################
RUN git clone https://github.com/holdenk/spark-testing-base.git /tmp/spark-testing-base
RUN pip install /tmp/spark-testing-base/python
RUN rm -rf /tmp/spark-testing-base

##########################################
### WORKDIR
##########################################
VOLUME /app
WORKDIR /app
CMD bash
