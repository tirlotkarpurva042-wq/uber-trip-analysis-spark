from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, min, max, to_timestamp, round, month
import pandas as pd

# Create Spark session
spark = SparkSession.builder \
    .appName("Uber Trip Analysis") \
    .master("local[*]") \
    .getOrCreate()

# Load dataset
file_path = "data/My Uber Drives - 2016.csv"

df = spark.read.csv(
    file_path,
    header=True,
    inferSchema=True
)

# Rename columns
df = df.withColumnRenamed("START_DATE*", "START_DATE") \
       .withColumnRenamed("END_DATE*", "END_DATE") \
       .withColumnRenamed("CATEGORY*", "CATEGORY") \
       .withColumnRenamed("START*", "START") \
       .withColumnRenamed("STOP*", "STOP") \
       .withColumnRenamed("MILES*", "MILES") \
       .withColumnRenamed("PURPOSE*", "PURPOSE")

# -------------------------------
# STEP 1: CLEAN MISSING VALUES
# -------------------------------

# Replace missing PURPOSE values
df = df.fillna({"PURPOSE": "Unknown"})

# Remove rows with missing important information
df = df.dropna(
    subset=["END_DATE", "CATEGORY", "START", "STOP"]
)

print("===== RECORDS AFTER CLEANING =====")
print(df.count())

# -------------------------------
# STEP 2: CONVERT DATE/TIME
# -------------------------------

df = df.withColumn(
    "START_DATE",
    to_timestamp("START_DATE", "M/d/yyyy H:mm")
)

df = df.withColumn(
    "END_DATE",
    to_timestamp("END_DATE", "M/d/yyyy H:mm")
)

# -------------------------------
# STEP 3: CALCULATE TRIP DURATION
# -------------------------------

df = df.withColumn(
    "DURATION_MINUTES",
    round(
        (col("END_DATE").cast("long") -
         col("START_DATE").cast("long")) / 60,
        2
    )
)

# Show data types
print("===== DATA TYPES AFTER CONVERSION =====")
df.printSchema()

# Show trip duration
print("===== TRIP DURATION =====")

df.select(
    "START_DATE",
    "END_DATE",
    "START",
    "STOP",
    "MILES",
    "DURATION_MINUTES"
).show(10, truncate=False)

# -------------------------------
# STEP 4: BUSINESS VS PERSONAL
# -------------------------------

category_analysis = df.groupBy("CATEGORY") \
    .count() \
    .orderBy(col("count").desc())

category_analysis.show()

category_analysis.toPandas().to_csv(
    "output/category_analysis.csv",
    index=False
)


# -------------------------------
# STEP 5: TRIP PURPOSE ANALYSIS
# -------------------------------

print("===== TRIP PURPOSE ANALYSIS =====")

purpose_analysis = df.groupBy("PURPOSE") \
    .count() \
    .orderBy(col("count").desc())

purpose_analysis.show(20, truncate=False)

purpose_analysis.toPandas().to_csv(
    "output/purpose_analysis.csv",
    index=False
)

# -------------------------------
# STEP 6: LOCATION ANALYSIS
# -------------------------------

print("===== TOP 10 START LOCATIONS =====")

start_location_analysis = df.groupBy("START") \
    .count() \
    .orderBy(col("count").desc())

start_location_analysis.show(10, truncate=False)

start_location_analysis.toPandas().to_csv(
    "output/start_location_analysis.csv",
    index=False
)
print("===== TOP 10 STOP LOCATIONS =====")

stop_location_analysis = df.groupBy("STOP") \
    .count() \
    .orderBy(col("count").desc())

stop_location_analysis.show(10, truncate=False)

stop_location_analysis.toPandas().to_csv(
    "output/stop_location_analysis.csv",
    index=False
)

# -------------------------------
# STEP 7: MILES ANALYSIS
# -------------------------------

from pyspark.sql.functions import col, sum, avg, min, max, to_timestamp, round, month
print("===== MILES ANALYSIS =====")

miles_analysis = df.select(
    round(sum("MILES"), 2).alias("TOTAL_MILES"),
    round(avg("MILES"), 2).alias("AVERAGE_MILES"),
    round(min("MILES"), 2).alias("MINIMUM_MILES"),
    round(max("MILES"), 2).alias("MAXIMUM_MILES")
)

miles_analysis.show()

miles_analysis.toPandas().to_csv(
    "output/miles_analysis.csv",
    index=False
)

# -------------------------------
# STEP 8: MONTHLY TRIP ANALYSIS
# -------------------------------

print("===== MONTHLY TRIP ANALYSIS =====")

monthly_analysis = df.withColumn(
    "MONTH",
    month("START_DATE")
).groupBy("MONTH") \
 .count() \
 .orderBy("MONTH")

monthly_analysis.show()

monthly_analysis.toPandas().to_csv(
    "output/monthly_analysis.csv",
    index=False
)

# -------------------------------
# STEP 9: TRIP DURATION ANALYSIS
# -------------------------------

print("===== TRIP DURATION ANALYSIS =====")

duration_analysis = df.select(
    round(sum("DURATION_MINUTES"), 2).alias("TOTAL_DURATION_MINUTES"),
    round(avg("DURATION_MINUTES"), 2).alias("AVERAGE_DURATION_MINUTES"),
    round(min("DURATION_MINUTES"), 2).alias("MINIMUM_DURATION_MINUTES"),
    round(max("DURATION_MINUTES"), 2).alias("MAXIMUM_DURATION_MINUTES")
)

duration_analysis.show()

duration_analysis.toPandas().to_csv(
    "output/duration_analysis.csv",
    index=False
)

# STEP 10: EXPORT CLEANED DATA FOR POWER BI

cleaned_data = df.select(
    "START_DATE",
    "END_DATE",
    "CATEGORY",
    "START",
    "STOP",
    "MILES",
    "PURPOSE",
    "DURATION_MINUTES"
)

cleaned_data.toPandas().to_csv(
    "output/cleaned_uber_data.csv",
    index=False
)

print("===== CLEANED DATA EXPORTED FOR POWER BI =====")
print("File: output/cleaned_uber_data.csv")

# Stop Spark
spark.stop()