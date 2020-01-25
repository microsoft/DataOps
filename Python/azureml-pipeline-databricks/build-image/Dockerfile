FROM conda/miniconda3

RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    openjdk-8-jdk \
    gcc

# Install dotnet runtime used to generate code coverage report
RUN curl -O https://packages.microsoft.com/config/ubuntu/19.04/packages-microsoft-prod.deb
RUN dpkg -i packages-microsoft-prod.deb
RUN apt-get update && apt-get install -y dotnet-runtime-3.1

# Install Spark runtime
WORKDIR /
RUN curl -O https://www-eu.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
RUN tar -zxf spark-2.4.4-bin-hadoop2.7.tgz
RUN rm spark-2.4.4-bin-hadoop2.7.tgz
ENV SPARK_HOME /spark-2.4.4-bin-hadoop2.7

# Install Python modules
COPY *.txt /setup/
RUN pip install --upgrade -r /setup/requirements.txt
