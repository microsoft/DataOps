FROM conda/miniconda3

RUN apt-get update
RUN apt-get install -y gcc wget openjdk-8-jdk

WORKDIR /
RUN wget -q https://www-eu.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
RUN tar -zxf spark-2.4.4-bin-hadoop2.7.tgz
RUN rm spark-2.4.4-bin-hadoop2.7.tgz
ENV SPARK_HOME /spark-2.4.4-bin-hadoop2.7

RUN pip install pytest==5.3.1 pytest-mock==1.13.0 flake8==3.7.9 pyspark==2.4.4 pyarrow==0.13.0

RUN pip install pandas==0.24.2

CMD ["python"]
