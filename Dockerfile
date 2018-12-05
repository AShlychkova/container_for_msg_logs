FROM masterandrey/docker-python-base

COPY logscript /logscript

RUN 

RUN apk --no-cache add musl-dev gfortran g++ jpeg-dev  \
    && pip install numpy\
    && pip install pandas\
    && pip install matplotlib\
    && apk add zip


#linux-headers zlib-dev cairo-dev