from pyspark import SparkContext
# import _mysql
# import MySQLdb
import urllib.parse
import urllib.request

#http://stackoverflow.com/questions/5106228/getting-every-possible-combination-in-a-list
def make_combos(listInput):
    tuples = [(x,y) for x in listInput for y in listInput if x != y ]
    for entry in tuples:
        if (entry[1], entry[0]) in tuples:
            if entry[1] < entry[0]:
                tuples.remove(entry)
            else:
                tuples.remove((entry[1], entry[0]))
    return tuples

sc = SparkContext("spark://spark-master:7077", "PopularItems")
# each worker loads a piece of the data file
data = sc.textFile("/tmp/data/logfile.txt", 2)
# tell each worker to split each line of it's partition

# (uid_1, tid)
pairs = data.map(lambda line: line.split(","))  

# (uid_1, [tid1, ...])
pairs2 = pairs.groupByKey().mapValues(list)

# (uid_1, [(tid1, tid2), (tid1, tid3),...]
pairs3 = pairs2.map(lambda x: (x[0], make_combos(x[1])))

# (uid_1, (tid1, tid2)), (uid_2, (tidx, tidy))
pairs4 = pairs3.flatMapValues(lambda x: x)

# ((tid1, tid2), uid_1), ((tidx, tidy), uid_2)
pairs5 = pairs4.map(lambda x: reversed(x))

# ((tid1, tid2), [uid_1, ..., uid_n])
pairs6 = pairs5.groupByKey().mapValues(list)

# ((tid1, tid2), n)
pairs7 = pairs6.map(lambda x: (x[0], len(x[1])))

# ((tid1, tid2), n), where n > 2
pairs8 = pairs7.filter(lambda x: x[1] > 2)
output = pairs8.collect() # bring the data back to the master node so we can print it out
recoDict = {}
counter = 1
for page_id, count in output:
    recoDict[counter] = str(page_id[0]) + " " + str(page_id[1])
    counter = counter + 1
    print ("page_id " + str(page_id) +  " count " + str(count))
print ("Popular items done")

sc.stop()

# #db = _mysql.connect(host="db", user="www", passwd="$3cureUS", db="cs4501")
# db = MySQLdb.connect(host="db", user="www", passwd="$3cureUS", db="cs4501")
# #db.query("""TRUNCATE TABLE model_app_recommendation""")
# c = db.cursor()
# # c.execute("""TRUNCATE TABLE model_app_recommendation""")
# count = 3
# # recoList = []
# for page_id, outputCount in output:
# 	# recoList.append((count, page_id[0], page_id[1]))
# 	c.execute("""INSERT INTO model_app_recommendation (id, task_first_id, task_second_id) VALUES (%s, %s, %s)""", (count, page_id[0], page_id[1]))
# 	# c.commit()
# 	count = count + 1
# #c.executemany("""INSERT INTO model_app_recommendation VALUES (%s, %s, %s)""", recoList)
# # db.query("""SELECT * FROM model_app_recommendation""")
# # r = db.store_result()
# # print(r.fetch_row(maxrows=0))
# c.execute("""SELECT * FROM model_app_recommendation""")
# print(c.fetchall())

# c.close()
# db.close()
print(recoDict)
post_encoded = urllib.parse.urlencode(recoDict).encode('utf-8')
req = urllib.request.Request('http://models-api:8000/api/v1/recommendationsSpark/', 
        data=post_encoded, method='POST')
resp_json = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
print(resp_json)
