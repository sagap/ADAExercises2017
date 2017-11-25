# An event analysis through Twitter

## Table of Contents:

1. [Preliminaries](#1-preliminaries)
2. [The data](#2-the-data)
3. [Running jobs on the cluster](3-running-jobs-on-the-cluster)
4. [A job template](4-a-job-template)


### 1. Preliminaries

In order to make the development pipeline less frustrating, consider doing the following.

- If you are off campus and want to use the cluster, make sure that you are connected to the EPFL <a href="https://epnet.epfl.ch/" target="_blank">VPN</a>.
- Instead of modifying your environment, run `. load_yarn.sh` every time before starting your development.


### 2. The data

The data is a single text (CSV, tab-separated) file and is located at the `/datasets/tweets-leon` path in HDFS (Hadoop file system) on the cluster. You can access it by logging in the main node `iccluster060.iccluster.epfl.ch` and running `hadoop fs -ls /datasets/tweets-leon`. The file size is about 2.2 terabytes, therefore any analysis should be done through the cluster by submitting jobs.


### 3. Running jobs on the cluster

#### First things first

**Important:** Edit the `username` file to contain your GASPAR username!

Even though one can follow the <a href="https://github.com/epfl-ada/ADA2017-Tutorials/tree/master/05%20-%20Using%20the%20cluster" target="_blank">tutorial</a> to submit jobs from their local machine, I was not able to do this on a Mac (tried for about two hours and I gave up). Therefore I have created a script to upload the `tweeter_events` directory to the cluster in order to be able to submit the job while logged in via SSH.

The `upload_to_cluster.sh` script will `rsync` the `tweeter_events` directory to the cluster, appending your GASPAR username at the end. This is to ensure that each one has his/her own place to put his/her code and that we do not delete each other's files.

**WARNING:** The script will *synchronise* the directory tree to the cluster. This means that any files deleted locally, will also be deleted remotely.

#### Creating a job

In order to run a job on the cluster you have to submit your Python script file with the following command:

```
spark-submit spark_job.py
```

Most of the times, the job will use external libraries. You will have to provide a `zip` archive with those dependencies, via the `--py-files` option, so the `spark-submit` command will look like this:

```
spark-submit --py-files dependencies.zip spark_job.py
```

To create the `dependencies.zip` archive:

  1. Create a file named `requirements.txt` (or any other name) and place one dependency per line. Those dependencies must be installable with `pip`.
  2. Create a directory named `dependencies` (or any other name).
  3. Run:
     ```
     pip install -t dependencies -r requirements.txt
     cd dependencies
     zip -r ../dependencies.zip .
     ```
  4. Add the following to your Python job script:
     ```python
     from pyspark import SparkContext

     sc = SparkContext()
     sc.addPyFile("dependencies.zip")
     ```

**Note:** Don't try and add dependencies such as `pandas` or `numpy`. These libraries are not `pip`-installable and need to be built. Chances are that even if you manage to build them, they will only work on your machine and not on the cluster.



### 4. A job template

Since the most common task will be to iterate over the rows of the data file, an "iteration" template has been created within the source directory (`tweeter_events`). Use it as a basis for any job you want to run.
