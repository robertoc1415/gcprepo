FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
# FROM tiangolo/uvicorn-gunicorn-fastapi
COPY ./pecaa /app
WORKDIR /app
# RUN python3 -m venv /env
RUN python3 -m venv /env
ENV PATH="/env/bin:$PATH"
RUN . /env/bin/activate
RUN /env/bin/python3 -m pip install --upgrade pip
# RUN apt-get install vim -y
RUN git clone https://github.com/robertoc1415/iqoptionapi-master2.git
WORKDIR /app/iqoptionapi-master2/iqoptionapi-master
RUN pip3 install -r requirements.txt
RUN python3 setup.py install
# WORKDIR /home
RUN apt-get update && apt-get install -y \
  wget \
  build-essential \
  automake \
  pkg-config \
  libtool \
  python3-dev \
  python3-setuptools

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

RUN python3 -m pip install ta-lib
# s
# RUN sudo -H pip3 install pyodbc
# RUN pip3 install --no-binary :all: pyodbc
RUN pip3 install pyodbc
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]