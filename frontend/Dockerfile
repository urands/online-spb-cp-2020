FROM python:3.7-rc-slim as frontend

RUN apt-get update && \
  apt-get install -y --no-install-recommends gcc python-dev python-mysqldb python3-pip && \
  apt-get remove -y gcc python-dev && \
  apt-get autoremove -y

RUN pip3 install pipenv

# install app dependencies
COPY Pipfile ./app/
#COPY Pipfile.lock ./app/
RUN cd app/ && pipenv install
RUN cd app/ && pipenv lock --requirements > requirements.txt 
RUN cd /app && pip install -r requirements.txt

# add app
COPY . ./

# set working directory
WORKDIR /app

#EXPOSE 5000

# start app
CMD ["python", "app.py"]

