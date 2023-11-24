# Problem

同型機定義會讓人往同樣功能或同樣硬體機型的方向去思考，然而若是從產品應用層面思考，
我們需要的是可以共享不同機台的 Approved List, Exception List, CPSDR Baseline...等等．

與其說是同型機，不如說機台上作業系統的版本是一樣，安裝的軟體也是一樣，這樣的機台就可以定義為同型機．
因為這樣的機台，具備有相當接近的基因，因此可以共享相關的資訊．

# Inspiration

局部敏感哈希（Locality Sensitive Hashing，縮寫為LSH）是一種非常實用的技巧。大多數人使用它進行近鄰搜索(near-neighbor search)，但它對於草圖算法(sketching algorithms)和高維數據分析也很有幫助。

LSH的主要思想是將高維數據點映射到低維空間，並保持數據點之間的局部相似性。換句話說，如果兩個數據點在高維空間中是相鄰的，那麼在低維空間中，這兩個點也應該是相鄰的。這種方法可以大大提高搜索效率，特別是在處理大規模高維數據時。

總的來說，局部敏感哈希是一種強大的工具，可以用於各種數據科學和機器學習應用。它的主要優點是能夠有效地處理高維數據，並提供快速的近鄰搜索和數據草圖功能。這使得它在許多情況下都非常有用，包括推薦系統、圖像識別和自然語言處理等領域。

讓我們來看看LSH的一些常見應用：

* 近似重複檢測 - LSH常用於對大量的文件、網頁和其他文件進行去重(deduplicate)
* 基因組研究 - LSH可以用於識別基因數據庫中的相似基因表達
* 圖像和視頻搜索 - 可以使用LSH進行大規模搜索
* 視頻指紋識別 - 在多媒體技術中，LSH被廣泛用作音視頻數據的指紋識別技術

# Poof of Concept

## Data Source

* Agent telemetry data

|serverguid|guid|cpuname|oscaption|osversion|cpucaption|osarchitecture|cpuarchitecture|
|----------|----|-------|---------|---------|----------|--------------|---------------|
|00eb13f0-bd54-11ed-9290-00155da02f20|006437bb-46a9-4fbb-bf45-ef921cdf25bd| |Microsoft Windows 10 企業版 LTSC|10.0.17763| |64 位元| |

* Agent installed application data

|serverguid|guid|caption|identifyingnumber|name|skunumber|vendor|version|installlocation|
|----------|----|-------|-----------------|----|---------|------|-------|---------------|
|00eb13f0-bd54-11ed-9290-00155da02f20|02031215-83d1-49dc-bcd0-786341a6bf8a|StellarProtect|{8D895A2C-B3C5-4BE6-A0FC-A482452AA970}|StellarProtect| |TXOne|2.1.0.1048|C:\Program Files\TXOne\StellarProtect\|

## Data Processing (process-data.py)

* Agent telemetry data
  * Drop columns cpu*, b/c most of data point are empty/null

* Agent installed application data
  * Drop columns skunumber, installlocation, b/c most of data point are empty/null
  * Drop columns identifyingnumber, version, which are not impact to application identification
  * Sort by columns caption, name, vendor and remove duplicated rows
  * Concatenate columns caption, name, vendor as a new column named "apps" for application identification per agent

* Merge agent telemetry data and agent installed application data by serverguid and guid

* Calculate hash values for each agent

* Group agents by serverguid and write to a file named "agent-apps-{serverguid}.csv"

## Data Analysis (analysis-data.py)

* Specify a file named "agent-apps-{serverguid}.csv" for analysis

* Specify a n-th agent for analysis, and compare its hash value with other agents

* Calculate the similarity between the n-th agent and other agents

* Sort the similarity and output the result to a file named "agent-apps-{serverguid}-similarity.csv"