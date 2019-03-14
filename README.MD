# PingCAP 题目

### 题目要求

有一个 100GB 的文件，里面内容是文本：

1. 找出第一个不重复的词

2. 只允许扫一遍文件

### 实现思路（Spark）

1. 扫描文件，提取出所有单词

    (line) --> flatmap --> (word)

2. 对所有单词，依次添加 index，记录出现位置, 初始化计数 count=1

    (word) --> zipWithIndex --> (word, (index, count=1))

3. 进行 reduceByKey 操作，对于相同的 word，index 取最小值，count 累加

    (word, (index, count=1)) --> reduceByKey --> (word, (index.min, count.sum))

4. 进行 filter, 取出 count == 1 的部分

    (word, (index, count)) --> filter(where count==1) --> (word, index)

5. 根据 index 排序，取出第一个

    (word, index) --> sort by index, take(1) --> answer word

### 实现思路（Python）

1. 类似 Spark，根据 word 首字母，将源文件分割为 62 个子文件（[a-zA-Z0-9].txt），同时添加 index 和 count=1 标志

2. 依次处理各个子文件，各个子文件大小一般不大，直接读入内存，存放到 dict = {word: [index.min, count.sum]} 里面

3. 记录并提取出各个 dict 中 index 最小且 count == 1 的结果，进行比较，得出最终结果

### 测试及存在问题

1. Spark 单机测试了 10GB 数据，耗时 10min。（分配了 4 核，用了 2GB 内存，HDD）

2. Python 单机测试了 1GB 数据，耗时 8min。(单线程，少量内存，HDD)

3. Python 实现的单线程版本过于缓慢。
