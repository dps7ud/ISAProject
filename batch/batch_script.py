from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
from kafka.common import NodeNotReadyError
import logging
import json
import urllib.request
import time

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    while True:
        try:
            es = Elasticsearch(['es'])
            task_consumer = KafkaConsumer("task_topic", group_id='listing_indexer'
                    , bootstrap_servers=['kafka:9092'])
            break
        except NodeNotReadyError:
            continue
    while True:
        with open('es.json', mode='rb') as file: # b is important -> binary
            fileContent = file.read()
        reqES = urllib.request.Request('http://es:9200/_bulk', data=fileContent, method='POST')
        reqES.add_header('Content-Type', 'application/x-ndjson/')
        try:
            respES_json = urllib.request.urlopen(reqES).read().decode('utf-8')
            logger.error("respES_json: " + str(respES_json)) 
            break
        except:
            time.sleep(5)
            continue
    while True:
        task_consumer = KafkaConsumer("task_topic", group_id='listing_indexer'
                , bootstrap_servers=['kafka:9092'])
        for message in task_consumer:
            #  Push to es instead of logging
            logger.error(message)
