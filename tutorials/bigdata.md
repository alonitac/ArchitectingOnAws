# Hadoop File System

## Provision hadoop cluster in k8s cluster

Apply the following Helm chart: 

https://artifacthub.io/packages/helm/apache-hadoop-helm/hadoop

### Explore Hadoop commands

All Hadoop commands, including HDFS and MapReduce, are run as an option under the `hadoop` command. To see the full list of options:

```shell
hadoop
```

We will specifically use the ‘fs’ option to run most of our HDFS commands.
There really aren’t all that many HDFS commands. If you have a linux administration background, these should mostly look familiar.

Let’s begin by doing a listing of the root HDFS folder:

```shell
hadoop fs -ls /
```

Create a directory by:
```shell
hdfs hadoop fs -mkdir /data
```

Verify creation by:

```shell
hadoop fs -ls
```

The copyFromLocal command copies files from the Linux Filesystem to HDFS (Note the case SenSiTiviTy for the copyFromLocal command):

```shell
hadoop fs -copyFromLocal my-local-file.txt /data
```

To see the size for all three files in human readable form:

```shell
 hadoop fs -du -h /data
```

To check the health of the HDFS Filesystem at root:

```shell
hdfs fsck /
```

It is possible to use the HDFS setrep command to change the replica factor for all pre-existing files from 3 down to 1. Let’s try that:
```shell
hadoop fs -setrep -R -w 1 /
```

Now, check the health status of HDFS again:

```shell
hdfs fsck /
```

# Spark Getting started

### Spark Core

We will demonstrate the following getting started guide (up to _Caching_ section):

https://spark.apache.org/docs/3.3.0/quick-start.html

### Spark SQL

1. Read the following dataset
```
df = spark.read.option("header", True).csv("s3a://iec-alonit-22/genome-scores.csv")
```
2. Familiarize yourself with the data and schema
```shell
df.show()
df.printSchema()
```
3. Count by `movieId`
```shell
df.groupBy("movieId").count().show()
```
4. Register the DataFrame as a SQL temporary view 
```shell
df.createOrReplaceTempView("ratings")
```
5. Query your data
```shell
sqlDF = spark.sql("SELECT * FROM ratings WHERE relevance > 0.1")
sqlDF.show()
```

### Spark Streaming 

We will demonstrate the _Quick Example_ tutorial:

https://spark.apache.org/docs/3.3.0/streaming-programming-guide.html#a-quick-example



# Mongo Quick introduction

https://www.mongodb.com/docs/manual/tutorial/getting-started/

# AWS DynamoDB - NoSQL database

### Create a table

1. Open the DynamoDB console at [https://console.aws.amazon.com/dynamodb/](https://console.aws.amazon.com/dynamodb/)
2. In the navigation pane on the left side of the console, choose **Dashboard**.
3. On the right side of the console, choose **Create Table**.
4. Enter the table details as follows:
    1. For the table name, enter a unique table name.
    2. For the partition key, enter `Artist`.
    3. Enter `SongTitle` as the sort key.
    4. Choose **Customize settings**.
    5. On **Read/write capacity settings** choose **Provisioned** mode with autoscale capacity with a minimum capacity of **1** and maximum of **10**.
5. Choose **Create** to create the table.

### Write and read data


1. On DynamoDB web console page, choose **PartiQL editor** on the left side menu.
2. The following example creates several new items in the `<table-name>` table. The [PartiQL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html) is
   a SQL-compatible query language for DynamoDB.

```shell
INSERT INTO "<table-name>" VALUE {'Artist':'No One You Know','SongTitle':'Call Me Today', 'AlbumTitle':'Somewhat Famous', 'Awards':'1'}

INSERT INTO "<table-name>" VALUE {'Artist':'No One You Know','SongTitle':'Howdy', 'AlbumTitle':'Somewhat Famous', 'Awards':'2'}

INSERT INTO "<table-name>" VALUE {'Artist':'Acme Band','SongTitle':'Happy Day', 'AlbumTitle':'Songs About Life', 'Awards':'10'}
                            
INSERT INTO "<table-name>" VALUE {'Artist':'Acme Band','SongTitle':'PartiQL Rocks', 'AlbumTitle':'Another Album Title', 'Awards':'8'}
```

Query the data by

```shell
SELECT * FROM "<table-name>" WHERE Artist='Acme Band' AND SongTitle='Happy Day'
```

### Create and query a global secondary index

1. In the navigation pane on the left side of the console, choose **Tables**.
2. Choose your table from the table list.
3. Choose the **Indexes** tab for your table.
4. Choose **Create** index.
5. For the **Partition key**, enter `AlbumTitle`.
6. For **Index** name, enter `AlbumTitle-index`.
7. Leave the other settings on their default values and choose **Create** index.

8. You query the global secondary index through PartiQL by using the Select statement and providing the index name
```shell
SELECT * FROM "<table-name>"."AlbumTitle-index" WHERE AlbumTitle='Somewhat Famous'
```


### Process new items with DynamoDB Streams and Lambda

#### Enable Streams

1. In the navigation pane on the left side of the console, choose **Tables**.
2. Choose your table from the table list.
3. Choose the **Exports and streams** tab for your table.
4. Under **DynamoDB stream details** choose **Enable**.
5. Choose **New and old images** and click **Enable stream**.

#### (Optional) Create Lambda execution IAM role

1. Open the IAM console at [https://console\.aws\.amazon\.com/iam/](https://console.aws.amazon.com/iam/)\.

2. In the navigation pane, choose **Roles**, **Create role**\.

3. On the **Trusted entity type** page, choose **AWS service** and the **Lambda** use case\.

4. On the **Review** page, enter a name for the role and choose **Create role**\.
5. Edit your IAM role with the following inline policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "lambda:InvokeFunction",
            "Resource": "arn:aws:lambda:<region>:<accountID>:function:<lambda-func-name>*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:<region>:<accountID>:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:DescribeStream",
                "dynamodb:GetRecords",
                "dynamodb:GetShardIterator",
                "dynamodb:ListStreams"
            ],
            "Resource": "arn:aws:dynamodb:<region>:<accountID>:table/<dynamo-table-name>/stream/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```

Change the following placeholders to the appropriate values: `<region>`, `<accountID>`, `<dynamo-table-name>`, `<lambda-func-name>`


The policy has four statements that allow your role to do the following:
+ Run a Lambda function. You create the function later in this tutorial\.
+ Access Amazon CloudWatch Logs\. The Lambda function writes diagnostics to CloudWatch Logs at runtime\.
+ Read data from the DynamoDB stream.
+ Publish messages to Amazon SNS\.

#### Create a Lambda Function

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console\.

2. Choose **Create function**\.

3. Under **Basic information**, do the following:

    1. Enter **Function name**.

    2. For **Runtime**, confirm that **Node\.js 16\.x** is selected\.

    3. For **Permissions** use your created role or `arn:aws:iam::964849360084:role/LambdaDynamoEvents` alternatively.

4. Choose **Create function**\.
5. Enter your function, copy the content of `publishNewSong.js` and paste it in the **Code source**. Change `<TOPIC-ARN>` to your SNS topic ARN you created in the previous exercise.
6. Click the **Deploy** button.
7. On the same page, click **Add trigger** and choose your Dynamo table as a source trigger.
8. Test your Lambda function by creating new items in the Dynamo table and watch for new emails in your inbox. 

