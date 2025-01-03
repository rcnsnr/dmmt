from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

# ELK yapılandırması
ELK_HOST = os.getenv("ELK_HOST")
ELK_PORT = os.getenv("ELK_PORT")
INDEX_NAME = "disk-monitoring-logs"

es = Elasticsearch([{'host': ELK_HOST, 'port': ELK_PORT}])

def send_log_to_elk(log_data):
    """
    Log verilerini ELK'ya gönderir.
    """
    try:
        res = es.index(index=INDEX_NAME, body=log_data)
        print(f"Log ELK'ya gönderildi: {res['result']}")
    except Exception as e:
        print(f"ELK'ya log gönderme başarısız: {str(e)}")
