FROM masterandrey/docker-python-base

COPY pip.requirements.txt /pip.requirements.txt
COPY logscript /logscript

RUN  pip install numpy\
    && pip install pandas\
    && pip install matplotlib\
    && apk add zip


#apk --no-cache add musl-dev linux-headers gfortran g++ jpeg-dev zlib-dev cairo-dev \
