FROM python:3.8-rc-slim as backend

RUN pip install pipenv

# install app dependencies
COPY app/Pipfile ./app/
COPY app/Pipfile.lock ./app/


RUN cd app/ && pipenv lock --requirements > requirements.txt 
RUN cd /app && pip install -r requirements.txt

# add app
COPY . ./

# set working directory
WORKDIR /app

#EXPOSE 5000

# start app
CMD ["python", "app.py"]

