import os
from pyspark.sql import SparkSession

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
ACCESS = os.getenv("MINIO_ACCESS_KEY")
SECRET = os.getenv("MINIO_SECRET_KEY")
BUCKET = os.getenv("MINIO_BUCKET", "bgd")

OUT_PATH = f"s3a://{BUCKET}/_smoke/s3_test_out"

spark = (
    SparkSession.builder
    .appName("s3-smoke-test")
    .getOrCreate()
)

# S3A config
hconf = spark.sparkContext._jsc.hadoopConfiguration()
hconf.set("fs.s3a.endpoint", MINIO_ENDPOINT.replace("http://", "").replace("https://", ""))
hconf.set("fs.s3a.access.key", ACCESS)
hconf.set("fs.s3a.secret.key", SECRET)
hconf.set("fs.s3a.path.style.access", "true")
hconf.set("fs.s3a.connection.ssl.enabled", "false")
hconf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

df = spark.createDataFrame(
    [(1, "a"), (2, "b"), (3, "c")],
    ["id", "val"]
)

# write parquet
df.write.mode("overwrite").parquet(OUT_PATH)

# read back
df2 = spark.read.parquet(OUT_PATH)
print("READ_BACK_COUNT=", df2.count())

spark.stop()
