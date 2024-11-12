from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("WordCountJob").getOrCreate()

# Replace with your S3 bucket path
input_path = "s3a://your-bucket/input.txt"
output_path = "s3a://your-bucket/output/"

# Read data from S3
data = spark.read.text(input_path)
words = data.selectExpr("split(value, ' ') as words").selectExpr("explode(words) as word")
word_count = words.groupBy("word").count()

# Write results back to S3
word_count.write.csv(output_path, mode="overwrite", header=True)

spark.stop()
