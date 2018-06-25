FROM centos:centos7
WORKDIR /app
ADD . /app
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm && yum install -y python36u python36u-libs python36u-devel python36u-pip g++ gcc make && yum clean all
RUN pip3.6 install --upgrade pip
RUN pip3.6 install pandas sklearn scipy
RUN pip3.6 install --upgrade django uwsgi django-cors-headers
