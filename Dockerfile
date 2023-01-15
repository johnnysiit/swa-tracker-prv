FROM python:3

RUN apt-get update && apt-get install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4
RUN apt-get install -y google-chrome-stable

RUN wget -N https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver

ENV CHROME_DRIVER_PATH /usr/local/bin/chromedriver

RUN pip install requests selenium pandas
ADD main.py /
ADD price_detect.py /
ADD tele_bot.py /
ADD price_database /
ADD trip_list /
CMD ["python", "main.py"]