FROM conda/miniconda3

ARG SPARK_VERSION=2.4.3
ARG HADOOP_VERSION=2.7

# Install Spark runtime
WORKDIR /
RUN apt-get update \
    && apt-get install -y \
        wget \
        apt-transport-https \
        openjdk-8-jdk \
    && wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar -zxf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

ENV SPARK_HOME /spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}

COPY azureml/ci_dependencies.yml /setup/

# activate Conda environment
ENV PATH /usr/local/envs/datops_ci/bin:$PATH

RUN conda update -n base -c defaults conda && \
    conda env create -f /setup/ci_dependencies.yml && \
    /bin/bash -c "source activate datops_ci" && \
    az --version && \
    chmod -R 777 /usr/local/envs/datops_ci/lib
