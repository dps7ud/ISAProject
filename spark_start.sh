# Install mysqldb and python3 on masters and clients
# Found locally at .../ISAProject/batch/spark_setup.sh
docker exec -it spark-master /tmp/data/spark_setup.sh
docker exec -it spark-worker /tmp/data/spark_setup.sh
# Start job
docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/hello.py

# Perform job every 120 seconds
watch -n 120 docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/hello.py
