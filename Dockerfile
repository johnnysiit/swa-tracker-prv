FROM python:3
RUN pip install requests selenium pandas
ADD main.py /
ADD price_detect.py /
ADD tele_bot.py /
ADD price_database /
ADD trip_list /
CMD ["python", "main.py"]