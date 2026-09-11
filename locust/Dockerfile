FROM locustio/locust
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
COPY locustfile.py /mnt/locust/locustfile.py