FROM python:3.9
ADD main.py .
RUN pip install requests selenium pandas
CMD ["python", "main.py"]