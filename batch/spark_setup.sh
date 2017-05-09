#!/usr/bin/env bash
# This script needs to be called from within each instance
# of a docker spark container (master and workers). It will
# install python 3 and mysql packages.
# This must be done before we attempt to run the spark job.
apt-get update &&
apt-get install python3-dev libmysqlclient-dev -y &&
apt-get install python-pip -y &&
pip install mysqlclient &&
apt-get install python-mysqldb
