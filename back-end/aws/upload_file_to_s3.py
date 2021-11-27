import logging
from config import S3_LOCATION

def upload_file_to_s3(aws_ob, src_path, file_name, bucket_name, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        aws_ob.upload_file(
            src_path,
            bucket_name,
            file_name,
            ExtraArgs={
                "ACL": acl
            }
        )

    except Exception as e:
        logging.error("upload file {} failed! {}".format(file_name, e))
        return e

    return "{}{}".format(S3_LOCATION, file_name)