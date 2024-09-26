import duckdb
import os

def lambda_handler(event, context):
    """
    PURPOSE:
    Get CSV URL, convert it to .Parquet format, save .Parquet file to specific S3 Bucket
    """

    # Extract source URL and destination filename from event
    source_url = event['source_url']  # CSV file signed URL
    destination_filename = event['destination_filename']  # Destination filename (e.g., 'output.parquet')

    # Fetch environment variables
    aws_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION')
    bucket_folder = os.getenv('BUCKET_FOLDER')  # S3 bucket folder (e.g., 's3://your-bucket-name/folder/')

    # Construct full S3 destination path
    destination_url = f"{bucket_folder}{destination_filename}"

    # Connect to DuckDB in memory
    conn = duckdb.connect(database=':memory:')

    # Create the secret for S3 access using environment variables
    conn.execute(f"""
        CREATE SECRET secret1 (
            TYPE S3,
            KEY_ID '{aws_key_id}',
            SECRET '{aws_secret}',
            REGION '{aws_region}'
        )
    """)

    # Load the CSV directly from the source URL and write it to the destination S3 bucket
    conn.execute(f"""
        COPY (SELECT * FROM read_csv_auto('{source_url}'))
        TO '{destination_url}' 
        (FORMAT 'parquet', OVERWRITE_OR_IGNORE TRUE)
    """)

    return {
        'statusCode': 200,
        'body': f"CSV converted to Parquet and uploaded to {destination_url} successfully!"
    }
