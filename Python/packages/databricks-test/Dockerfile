FROM conda/miniconda3

ARG SPARK_VERSION=2.4.4
ARG HADOOP_VERSION=2.7

# Install Spark runtime
WORKDIR /
RUN apt-get update \
    && apt-get install -y \
        wget \
        apt-transport-https \
        openjdk-8-jdk \
    && wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar -zxf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

ENV SPARK_HOME /spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}

RUN pip install pytest==5.3.1 pytest-mock==1.13.0 flake8==3.7.9 pyspark==${SPARK_VERSION} pyarrow==0.13.0 pandas==0.24.2

CMD ["python"]
