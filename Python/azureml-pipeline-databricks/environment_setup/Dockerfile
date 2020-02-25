FROM conda/miniconda3

COPY azureml/ci_dependencies.yml /setup/

# Install Spark runtime
WORKDIR /
RUN apt-get update \
    && apt-get install -y \
        curl \
        apt-transport-https \
        openjdk-8-jdk \
    && curl -O https://www-eu.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz \
    && tar -zxf spark-2.4.4-bin-hadoop2.7.tgz \
    && rm spark-2.4.4-bin-hadoop2.7.tgz

ENV SPARK_HOME /spark-2.4.4-bin-hadoop2.7

# activate Conda environment
ENV PATH /usr/local/envs/mlopspython_ci/bin:$PATH

RUN conda update -n base -c defaults conda && \
    conda env create -f /setup/ci_dependencies.yml && \
    /bin/bash -c "source activate mlopspython_ci" && \
    az --version && \
    chmod -R 777 /usr/local/envs/mlopspython_ci/lib
