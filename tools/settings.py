#Ubuntu with imagemagic q16 and pythonmagic API. 
#https://hub.docker.com/r/daniells/imagemagick/

#NOTE: README: https://stackoverflow.com/questions/45775394/how-to-convert-pdf-to-png-efficiently
# 

#Using a single Memcached server:
#result_backend = 'cache+memcached://127.0.0.1:11211/'
#

#Docker memcached memory server
#https://hub.docker.com/_/memcached
#Using multiple Memcached servers:
result_backend = """
    cache+memcached://172.19.26.240:11211;172.19.26.242:11211/
""".strip()



#The “memory” backend stores the cache in memory only:
result_backend = 'cache'
cache_backend = 'memory'



# CELERY MONGODB
#https://docs.celeryproject.org/en/stable/userguide/configuration.html#std:setting-cache_backend_options

# Use MongoDB backend for vector storage
#result_backend = 'mongodb://localhost:27017/'
#mongodb_backend_settings = {
#    'database': 'mydb',
#    'taskmeta_collection': 'my_taskmeta_collection',
#}
