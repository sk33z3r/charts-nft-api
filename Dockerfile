FROM python:3 AS build
# upgrade pip
RUN pip install --upgrade pip
# add build pkgs
#RUN apk add --update gcc libc-dev jpeg-dev zlib-dev \
#&& rm  -rf /tmp/* /var/cache/apk/*
# install python modules
ADD dockerfiles/requirements.txt /
RUN pip install -r /requirements.txt

FROM python:3 AS run
# get compiled modules from pervious stage
COPY --from=build /usr/local/lib/python3.10 /usr/local/lib/python3.10
# add the python files for the game
ADD dockerfiles/run.sh /usr/local/bin/run
ADD ./*.py /api/
# finish up container
WORKDIR /api
EXPOSE 5000
CMD ["run"]
