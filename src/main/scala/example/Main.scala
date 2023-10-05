package example

import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions.{col}
import os._
import ujson._

object Main{
  // create a spark context that should in theory be accessible through the whole object
  val headers: ujson.Value.Value = loadHeaders()
  val dataPath: String = "data/ukb40500_cut_merged.csv"

  def main(args: Array[String]): Unit = {
    // setup at the start of main
    val spark = SparkSession.builder.appName("Simple Application").config("spark.master", "local").getOrCreate()

    val df: DataFrame = spark.read
      .option("header", "true") // Treats the first row as header
      .option("inferSchema", "true") // Infers column data types
      .csv(this.dataPath) 

    val columnsToPrint = Seq("`20008-0.0`", "`20008-0.1`", "`20008-0.2`","`20008-0.3`") // Replace with your column names
    val selectedDF: DataFrame = df.select(columnsToPrint.map(col): _*) 
    selectedDF.show(100)
    
    // teardown at the end of main
    spark.stop()
  }

  def loadHeaders(): ujson.Value.Value = {
    val path: os.Path = os.pwd/"data"/"headers.json"
    val jsonString = os.read(path)
    return ujson.read(jsonString)
  }

  def visualizeData(df: DataFrame){

  }
}
