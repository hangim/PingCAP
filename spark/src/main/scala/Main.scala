import org.apache.spark.{SparkConf, SparkContext}

object Main {
  def main(args: Array[String]): Unit = {
    val sparkConf = new SparkConf()
      .setAppName("PingCAP")
      .setMaster("local[4]") // local debug
//      .setMaster("spark://localhost:7077") // for submit to compute cluster
//      .setJars(List("/PATHTO/PingCAP/out/artifacts/PingCAP/PingCAP.jar")) // for idea debug
//      .set("spark.executor.instances", "2")
//      .set("spark.executor.memory", "4g")
//      .set("spark.executor.cores", "4")
    val sc = new SparkContext(sparkConf)

    val textFile = sc.textFile("/data/1.txt")

    val result = textFile.flatMap(line =>
      line.replaceAll("""[^a-zA-Z0-9 ]"""," ").split(" "))    // word
      .zipWithIndex()                                             // word, index
      .map(word_index => (word_index._1, (word_index._2, 1)))     // word, (index, count=1)
      .reduceByKey((a, b) => (Math.min(a._1, b._1), a._2 + b._2)) // word, (index.min, count.sum)
      .filter(_._2._2 == 1)                                       // word, (index, count == 1)
      .map(x => (x._2._1, x._1))                                  // index, word
      .sortByKey()

    val printed_data = result.take(10)
    for (item <- printed_data)
      println(s"location: \t${item._1}, \tword: \t${item._2}")
  }
}
