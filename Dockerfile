# set base image (host OS)
FROM python:3.6

# set the working directory in the container
WORKDIR /bot

# install dependencies
RUN pip install -U discord.py

# copy the content of the local src directory to the working directory
COPY bot/ .

# command to run on container start
CMD [ "python", "./GEObot.py" ]
