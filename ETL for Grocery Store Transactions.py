# Databricks notebook source
# MAGIC %md 
# MAGIC By
# MAGIC
# MAGIC Name: Mukul Aggarwal
# MAGIC
# MAGIC Email: msd23007@iiitl.ac.in
# MAGIC
# MAGIC Enrolment Number: MSD23007
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Extraction

# COMMAND ----------

# MAGIC %md
# MAGIC ## Connecting to SQL Server on GCP

# COMMAND ----------

jdbcHostname = "34.72.112.128"
jdbcPort = 3306
jdbcDatabase = "grocery_data"
jdbcUsername = "Mukul"
jdbcPassword = "Aesl$775"

# COMMAND ----------

jdbcUrl = f"jdbc:mysql://{jdbcHostname}:{jdbcPort}/{jdbcDatabase}?user={jdbcUsername}&password={jdbcPassword}"

# COMMAND ----------

connectionProperties = {
    "user" : jdbcUsername,
    "password" : jdbcPassword,
    "driver" : "com.mysql.jdbc.Driver"
}

df = spark.read.jdbc(jdbcUrl, "Transactions", properties=connectionProperties)
# Loaded Transactions table from MySQL
df.show()


# COMMAND ----------

# MAGIC %md
# MAGIC # Transformation

# COMMAND ----------

# MAGIC %md
# MAGIC ## Removing \r at the end of itemDescription

# COMMAND ----------

from pyspark.sql.functions import regexp_replace
processed_df = df.withColumn("itemDescription", regexp_replace(df["itemDescription"], r"\r", ""))
processed_df.show()


# COMMAND ----------

# MAGIC %md
# MAGIC ## Extracting Day, Month, Year and Week from Date

# COMMAND ----------

from pyspark.sql.functions import year, month, dayofmonth, weekofyear

processed_df = processed_df.withColumn("Year", year(processed_df["Date"])) \
                           .withColumn("Month", month(processed_df["Date"])) \
                           .withColumn("Day", dayofmonth(processed_df["Date"])) \
                           .withColumn("WeekOfYear", weekofyear(processed_df["Date"]))

processed_df.show()


# COMMAND ----------

processed_df.describe().show()

# COMMAND ----------

# MAGIC %md
# MAGIC # Load 

# COMMAND ----------

# MAGIC %md
# MAGIC ## Loading into a delta table
# MAGIC
# MAGIC **Delta Table**: A Delta Table is a type of table in the Delta Lake format, an open-source storage layer that brings ACID transactions, schema enforcement, and data versioning to data lakes. Delta Tables provide reliable data storage and management, enabling robust data pipelines and analytics.

# COMMAND ----------

processed_df.write.format("delta").mode("overwrite").saveAsTable("Groceries_Transactions")

# COMMAND ----------

# MAGIC %md
# MAGIC Checking if the data has been stored succesfully in Delta Table

# COMMAND ----------

spark.sql("SELECT COUNT(*) AS RowCount FROM Groceries_Transactions").show()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC **Data Loading Succesful!**
