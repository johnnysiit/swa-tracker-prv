FROM python:3
RUN pip install requests selenium pandas
ADD main.py /
CMD ["python", "main.py"]