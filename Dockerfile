FROM python:3.7-alpine
WORKDIR /app
RUN pip install requests configparser json sys os datetime
RUN apk add --no-cache git
RUN git clone -b main https://github.com/RiffSphere/Collectarr /app
CMD sh /app/folders.sh && python /app/collectarr.py /config

VOLUME /config

