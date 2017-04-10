from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
from kafka.common import NodeNotReadyError
import logging
import json

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
        task_consumer = KafkaConsumer("task_topic", group_id='listing_indexer'
                , bootstrap_servers=['kafka:9092'])
        for message in task_consumer:
            #  Push to es instead of logging
            logger.error(message)
