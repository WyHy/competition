FROM daocloud.io/ubuntu:16.04
RUN apt update
RUN apt install -y build-essential
RUN apt install -y libopenslide0 libstdc++6 software-properties-common python-software-properties
RUN apt update
RUN apt install -y python3 python3-pip
RUN apt install -y tesseract-ocr tesseract-ocr-chi-sim
ADD ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ADD ./tslide /tslide
RUN cp -r /tslide/*.so* /usr/lib/
ADD ./ /

