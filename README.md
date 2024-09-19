# BIM360/ACC Data to AWS QuickSight with Lambda

This repository provides a Lambda function that converts CSV data from Autodesk ACC (or BIM360) into Parquet format and stores it in your own S3 bucket. This allows you to efficiently generate reports in AWS QuickSight from your data stored in Parquet format.

## Overview

### Problem

Users of Autodesk Construction Cloud (ACC) or BIM360 who want to leverage the reporting power of AWS QuickSight need their data in a format suitable for QuickSight consumption. Parquet files provide an efficient, compressed format ideal for this purpose. This Lambda function automates the process of converting CSV files to Parquet, ensuring that your data is ready for QuickSight.

### Solution

This project provides an AWS Lambda function that:

1. As input:  Provide a "signed CSV file URL", and a "filename" for the destination parquet file.
2. Converts the CSV file to Parquet format using DuckDB.
3. Uploads the Parquet file to a specified S3 bucket ( specified in the AWS Lambda configurations ).

> You can set up a scheduled job or trigger this Lambda function automatically whenever new data is available, via an ACC webhook.

> See Reference documentation, to see how you can retrieve the [individual signURL for a CSV file from BIM360 Data-Connector API](https://aps.autodesk.com/en/docs/bim360/v1/tutorials/data-connector/dc-tutorial-retrieve-data-extract/#step-3-retrieve-a-file-from-a-data-extract) 

### What is Serverless?

Serverless computing is a cloud computing execution model in which the cloud provider runs the server, dynamically managing the allocation of machine resources. In this model, you can build and run applications without managing infrastructure, scaling automatically based on demand. AWS Lambda is one such service that allows you to execute code without provisioning or managing servers.

<hr>

## Architecture

Here is a high-level overview of how the solution works:

![mermaid-diagram-2024-09-19-142944](https://github.com/user-attachments/assets/b5ba09dc-2d70-4c3d-bed9-91f10dff7459)



#### Items:
- `Data Source`: ACC or BIM360 generates CSV files.
- `Signed URL`: The CSV file is accessed via a signed URL
-  `Event`: This is a webhook event, that comes from ACC/BIM360 when a CSV file changes. The event contains a signed-URL (of the 'source' CSV ) and a filename (the 'destination' parquet file)  
- `AWS Lambda`: The Lambda function processes the CSV and converts it to Parquet format.
- `S3 Bucket`: The resulting Parquet file is stored in your own S3 bucket.
- `AWS QuickSight`: QuickSight generates reports from the Parquet files.

<hr>

## Getting Started

### Prerequisites

-	An Amazon Web Services (AWS) account.
-	Access to Autodesk Construction Cloud (ACC) or BIM360 to generate CSV data.
-	A configured S3 bucket to store Parquet files.
-	AWS IAM permissions: Ensure that the Lambda function has permissions to read from the signed CSV URL and write to the S3 bucket.


#### 1. Create the Lambda handler

1. Create a new Lambda function in your favorite region.
2. Copy/Paste the [handler.py](handler.py) code and replace the default handler 
3. Make the lambda function publicly (URL publicly accessible).
4. Upload your 'duckDB.zip' file into a new 'duckDB' layer (`see step 2 below`)
5. Attach the 'duckDB' layer to this handler
6. Setup your environment variables under the configuration section (`see step 3 below`)

#### 2. Create a "DuckDB" Lambda Layer 

You need to create a Lambda Layer that includes DuckDB as a dependency.

> A. Create a directory for the dependencies, Install DuckDB into the directory, Package the layer:

```bash
mkdir duckdb_layer
cd duckdb_layer

mkdir -p python
pip install --target ./python duckdb

zip -r9 duckdb_layer.zip python
```

#### 3. Set Up Environment Variables in Lambda

Go to the AWS Lambda console and configure the following environment variables:

-	AWS_ACCESS_KEY_ID: Your AWS Access Key ID.
-	AWS_SECRET_ACCESS_KEY: Your AWS Secret Access Key.
-	AWS_REGION: Your preferred AWS region (e.g., us-east-1).
-	BUCKET_FOLDER: The S3 bucket folder where the Parquet files will be stored (e.g., s3://your-bucket-name/folder/).

#### 4. Test it

> C. Example Usage

```bash
aws lambda invoke \
    --function-name your-lambda-function-name \
    --payload '{"source_url": "https://signed-url-to-csv-file", "destination_filename": "output.parquet"}' \
    response.json
```

<hr>

## How It Works

-	DuckDB is used within the Lambda function to efficiently convert CSV files to Parquet format.
-	AWS S3 is the storage location for the Parquet files.
-	AWS Lambda provides a serverless way to handle the data conversion without the need for managing infrastructure.
-	AWS QuickSight can then use these Parquet files to generate insightful reports.

#### Security Considerations

-	AWS IAM Roles: Ensure that your Lambda function is using a role with the least privileges necessary to read from the signed URL and write to your S3 bucket.
-	Secrets Management: Consider using AWS Secrets Manager to store your AWS credentials securely.

## Conclusion

This setup helps you automatically convert Autodesk ACC (or BIM360) data into a format suitable for AWS QuickSight reporting. By leveraging serverless infrastructure with AWS Lambda, this solution is both scalable and cost-effective.
