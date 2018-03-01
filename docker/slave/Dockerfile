FROM bsao/app-base:latest
MAINTAINER  Robson Junior <bsao@icloud.com> (@bsao)

CMD env && /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker $MASTER_PORT_7077_TCP_ADDR:7077
