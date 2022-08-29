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

