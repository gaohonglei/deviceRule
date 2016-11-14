import redis
redisClient=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
redisClient.set(":1:b","12")
value=redisClient.get(":1:b")
print(value)
