import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

CATALOG = 'glue_catalog'
DATABASE = "iceberg_demo"
TABLE = "icebergtt"
INPUT_BASE_PATH = 's3://amazon-reviews-pds/parquet'
PRODUCT_CATEGORIES = ['Apparel', 'Camera', 'PC', 'Software', 'Video']
INPUT_CATEGORIES = [f'{INPUT_BASE_PATH}/product_category={category}/' for category in PRODUCT_CATEGORIES]

IncrementalInputDyF = glueContext.create_dynamic_frame.from_catalog(database = "iceberg_demo", table_name = "raw_csv_input", transformation_ctx = "IncrementalInputDyF")
IncrementalInputDF = IncrementalInputDyF.toDF()

IncrementalInputDF.createOrReplaceTempView("tmptab")

query = f"""
CREATE TABLE glue_catalog.iceberg_demo.lentra
USING iceberg
TBLPROPERTIES ("format-version"="2")
AS SELECT * FROM tmptab
"""
spark.sql(query)

print("done")
##Committed job

