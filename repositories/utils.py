

import os
import uuid
from dotenv import load_dotenv
from models.product.product_image_schema import CreateProductImageDto
import boto3

def upload_image_to_s3(request: CreateProductImageDto):
    
    load_dotenv()
    
    image_extension = request.image.filename.split(".")[-1]

    # Create unique file name and save to S3
    filename = str(uuid.uuid4()) + "." + image_extension

    bucket_name = os.environ['S3_BUCKET_NAME']

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    
    bucket.upload_fileobj(request.image.file, filename, ExtraArgs = {"ACL": "public-read"})

    url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"

    return url