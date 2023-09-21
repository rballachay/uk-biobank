package example

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{SparkSession, DataFrame}
import os._
import ujson._

object Hello{
  // This is the dictionary with what must be the 
  val descrDict: os.Path = os.pwd/"data"/"descr_dict.json"

  val loadedDict = loadDescDict(descrDict)

  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder.appName("Simple Application").config("spark.master", "local").getOrCreate()

    val csvFilePath = "data/ukb40500_cut_merged.csv"
    val df: DataFrame = spark.read
      .option("header", "true") // Treats the first row as header
      .option("inferSchema", "true") // Infers column data types
      .csv(csvFilePath) 
    //val logData = spark.read.textFile(logFile).cache()
    //val numAs = logData.filter(line => line.contains("a")).count()
    //val numBs = logData.filter(line => line.contains("b")).count()
    //println(s"Lines with a: $numAs, Lines with b: $numBs")
    spark.stop()
  }
  /*
  val spark = SparkSession
    .builder()
    .appName("Spark")
    .config("spark.master", "local")
    .getOrCreate()

  // For implicit conversions like converting RDDs to DataFrames
  import spark.implicits._
  */
  def loadDescDict(path: os.Path): ujson.Value.Value = {
    val jsonString = os.read(path)
    return ujson.read(jsonString)
  }
}
