# Databricks notebook source
import pickle
#import pandas as pd
#import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import azure.cosmos.cosmos_client as cosmos_client

# COMMAND ----------

dbutils.widgets.text("output", "","")
dbutils.widgets.get("output")
FilePath = getArgument("output")

# COMMAND ----------

dbutils.widgets.text("filename", "","")
dbutils.widgets.get("filename")
filename = getArgument("filename")
storage_account_name = "simplitesting"
storage_account_access_key = "hePUhzTzQo2tXxEfEvpPrPI0Hl2TjySGy2CGxq5AwgQCbU4lA1Jx4QD9BzX8n5TvwpnF7PC6YKHNJUcCwPxUsQ=="

# COMMAND ----------

spark.conf.set(
"fs.azure.account.key."+storage_account_name+".blob.core.windows.net",
storage_account_access_key)

# COMMAND ----------

file_location = "wasbs://reviewblob@simplitesting.blob.core.windows.net"+FilePath+"/"+filename
print(file_location)
file_type = "csv"

# COMMAND ----------

df = spark.read.format(file_type).option("inferSchema", "true").load(file_location)
df.show()

# COMMAND ----------

train=df.toPandas()

# COMMAND ----------

x=train.iloc[2:len(train),2:4].values

y=train.iloc[2:len(train),:1].values

# COMMAND ----------

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)
reg = LinearRegression()
reg.fit(x_train,y_train)

# COMMAND ----------

file_name = 'House_Price.pkl'
pkl_file = open(file_name, 'wb')
model = pickle.dump(reg, pkl_file)
pkl_file.close()
#import base64
#with open(PickleFilePath, 'wb') as fp:
    #data = pickle.dumps(reg, pkl_file)
    #encoded = base64.b64encode(data)
    #fp.write(encoded)

# COMMAND ----------

#to check all created files on driver
display(dbutils.fs.ls("file:/databricks/driver/"))

# COMMAND ----------

#to unmount
#dbutils.fs.unmount(mount_point = "/mnt/gayatri")

# COMMAND ----------

#mount code
dbutils.fs.mount(
 source = "wasbs://reviewblob@simplitesting.blob.core.windows.net",
 mount_point = "/mnt/gayatri",
 extra_configs = {"fs.azure.account.key.simplitesting.blob.core.windows.net": "hePUhzTzQo2tXxEfEvpPrPI0Hl2TjySGy2CGxq5AwgQCbU4lA1Jx4QD9BzX8n5TvwpnF7PC6YKHNJUcCwPxUsQ=="})

# COMMAND ----------

#to check your pickle file
dbutils.fs.ls("mnt/gayatri")

# COMMAND ----------

#to copy your file
dbutils.fs.cp("file:/databricks/driver/House_Price.pkl","/mnt/gayatri")

# COMMAND ----------

#to read your pickle file
file_loc = "/dbfs/mnt/gayatri/House_Price.pkl"
with open("/dbfs/mnt/gayatri/House_Price.pkl", mode='rb') as f:
 pkl_file = pickle.load(f)
 #model_pkl = pickle.load(pkl_file)
 y_pred = pkl_file.predict(x_test)
 print("prediction",y_pred)

# COMMAND ----------

y_pred1=pd.DataFrame(y_pred)
df = spark.createDataFrame(y_pred1)

# COMMAND ----------

config = {
   'ENDPOINT': 'https://azurecosomsdb.documents.azure.com:443/',
   'PRIMARYKEY': '1Ip7RQywi0IkLrLWUdKFMqN2EPkOKLe5uYpL5CGNjCKmLVzVSqHxLjnmzEGEY3Owgd6m3GEcuMaYTdpPZDDIew==',
   'DATABASE': 'BlobDataCopy',
   'COLLECTION': 'blobdata'
}

# COMMAND ----------

client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={'masterKey': config['PRIMARYKEY']})

# COMMAND ----------

DatabaseID = 'BlobDataCopy'
database_link = 'dbs/' + config['DATABASE']
database = client.ReadDatabase(database_link)

# COMMAND ----------

collection_link = database_link + '/colls/{0}'.format(config['COLLECTION'])
collection = client.ReadContainer(collection_link)

client.CreateItem(collection_link, {
   "Cloud_Service": 0
   })

# COMMAND ----------


