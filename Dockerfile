FROM python:3

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN apt -f install -y

# install chromedriver
RUN apk-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# install selenium
RUN pip install selenium==3.8.0

RUN pip install requests pandas selenium
ADD main.py /app/main.py
ADD price_detect.py /app/price_detect.py
ADD tele_bot.py /app/tele_bot.py
ADD price_database /app/price_database
ADD trip_list /app/trip_list

COPY swa.cronjob /etc/cron.d/swa.cronjob
RUN apt-get update 
RUN apt-get install -y cron 
RUN chmod 0644 /etc/cron.d/swa.cronjob 
RUN crontab /etc/cron.d/swa.cronjob
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log