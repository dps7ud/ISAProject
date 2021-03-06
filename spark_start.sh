# Install mysqldb and python3 on masters and clients
docker exec -it spark-master bash -c "apt-get update && apt-get install python3-dev libmysqlclient-dev -y && apt-get install python-pip -y && pip install mysqlclient && apt-get install python-mysqldb"
docker exec -it spark-worker bash -c "apt-get update && apt-get install python3-dev libmysqlclient-dev -y && apt-get install python-pip -y && pip install mysqlclient && apt-get install python-mysqldb"

# Start job
docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/hello.py

# Perform job every 120 seconds
while true; do
    sleep 120
    docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/hello.py
done
