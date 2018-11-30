FROM masterandrey/docker-python-base

COPY pip.requirements.txt /pip.requirements.txt
COPY logscript /logscript

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && mkdir -p ~/.fonts \
    && apk --no-cache add musl-dev linux-headers gfortran g++ jpeg-dev zlib-dev cairo-dev \
    && pip install numpy\
    && pip install pandas\
    && pip install matplotlib\
    && apk add zip


