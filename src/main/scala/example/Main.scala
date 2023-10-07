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
    
    // note that spark works differently from python, it seems to have trouble reading
    // a csv with an 'index' column. to avoid this problem, i just used awk to remove 
    // the first column
    val columnsToPrint = Seq("eid","`21022-0.0`","`31-0.0`") // Replace with your column names
    val selectedDF: DataFrame = df.select(columnsToPrint.map(col): _*) 
    
    val outputPath:os.Path = os.pwd/"data"/"ukb40500_selected_cols.csv"
    
    selectedDF
      .coalesce(1)
      .write
      .format("csv")
      .option("header", "true") // Write the header row with column names
      .mode("overwrite") 
      .save(outputPath.toString)

    // get the first item of the list - this only works if we only have one partition - aka
    // the data has already been coalesced
    val oldFilePath: os.Path = os.list(outputPath).filter(file => os.isFile(file) && file.ext == "csv").head

    // create temp file before we remove directory
    val tempFile: os.Path = os.pwd/"data"/"__tmp_conversion_spark.csv"
    
    // move file to folder name 
    os.move(oldFilePath, tempFile)
    os.remove.all(outputPath)
    os.move(tempFile, outputPath)
    os.remove.all(tempFile)

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
