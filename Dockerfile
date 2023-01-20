FROM python:3

RUN apt-get -y update
RUN pip install --upgrade pip
RUN apt-get install zip -y
RUN apt-get install unzip -y

RUN wget -N https://chromedriver.storage.googleapis.com/72.0.3626.69/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver

# Install chrome broswer
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable

ENV PATH "$PATH:/usr/local/bin/chromedriver"
# install selenium
RUN pip install selenium==3.8.0

RUN pip install requests pandas
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