FROM python:3.9

WORKDIR /usr/src/app

ARG passwd

RUN groupadd -g 61000 batch && \
    useradd -u 61001 -g 61000 -m \
    -p $(perl -e 'print crypt(${passwd}, "\$6\$salt03")') \
    -s /bin/bash pybatch

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install selenium \
    && pip install requests \
    && pip install Selenium-Screenshot

RUN mkdir /home/pybatch/bin

# コンテナ起動時にシェルを立ち上げる
CMD ["/bin/bash"]
