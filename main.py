from select import select
from xml.sax.saxutils import escape

import pyspark

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import *
from pyspark.sql.functions import regexp_replace, col
# SparkSession
spark = SparkSession.builder \
    .appName("GooglePlayStore") \
    .getOrCreate()

#Create Dataframe
df = spark.read \
    .format('csv') \
    .option('sep', ',') \
    .option('header', 'true') \
    .option('inferSchema', 'true') \
    .load('/app/googleplaystore.csv')



df = df.drop("size" , "Content Rating" , "Last Updated", "Current Ver", "Android Ver")


# "Reviews" ve "Price" sütunlarını Integer türüne dönüştürür
df = df.withColumn("Reviews", col("Reviews").cast(IntegerType()))
df = df.withColumn("Price", col("Price").cast(IntegerType()))

# "Installs" sütunundaki tüm non-numerik karakterleri kaldırır
df = df.withColumn("Installs", regexp_replace(col("Installs"), "[^0-9]", ""))

# "Installs" sütununu Integer türüne dönüştürür
df = df.withColumn("Installs", col("Installs").cast(IntegerType()))

# "Price" sütunundaki dolar işaretlerini kaldırın ve Integer türüne dönüştürür
df = df.withColumn("Price", regexp_replace(col("Price"), "[$]", ""))

#df.printSchema()
#df.show()

#AGENDA : We have google playstore dataset containing information of different apps installed rating and versions and other details and we are going to do analysis based on the data we have
#3.Category wise distribution.
#4.TOP paid apps.
#5.Top paid rating apps.

# Geçici bir view oluşturur
df.createOrReplaceTempView("apps")

#1.Find out TOP 10 reviews given to the apps.
result = spark.sql("""
    SELECT App, SUM(Reviews) AS TotalReviews
    FROM apps
    GROUP BY App
    ORDER BY TotalReviews DESC
""")

# Sonuçları gösterir
result.show()

#2.TOP 10 installs apps and distribution of type (free/paid).

df.createOrReplaceTempView("apps2")

result = spark.sql("""
    SELECT App, SUM(Installs) AS TotalInstalls
    FROM apps2
    GROUP BY App
    ORDER BY TotalInstalls DESC
""")

# Sonuçları gösterir
result.show()

#3.Category wise distribution.

df.createOrReplaceTempView("apps3")

result = spark.sql("""
    SELECT Category, SUM(Installs) AS TotalInstalls
    FROM apps3
    GROUP BY Category
    ORDER BY TotalInstalls DESC
""")

# Sonuçları gösterir
result.show()
