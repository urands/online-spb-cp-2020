FROM python:3.7-rc-slim as backend

RUN pip install pipenv

# install app dependencies
COPY Pipfile ./app/
#COPY Pipfile.lock ./app/

RUN cd app/ && pipenv install
RUN cd app/ && pipenv lock --requirements > requirements.txt 
RUN cd /app && pip install -r requirements.txt
RUN cd /app && pip install xlrd

# add app
COPY . ./

# set working directory
WORKDIR /app

#EXPOSE 5000

# start app
CMD ["python", "app.py"]

