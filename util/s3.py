from typing import Optional

import os
import boto3

from .functions.normalize_url import normalize_url


class S3:
    def __init__(self):
        self.__s3client = boto3.client('s3')

    @staticmethod
    def generate_link(
        object_name: str,
        bucket_name: Optional[str] = os.environ.get('BUCKET_NAME'),
        s3_region: Optional[str] = os.environ.get('S3_REGION')
    ) -> str:
        """Generates a link to the RSS feed in S3

            Arguments:
                object_name {str} -- File path on S3

            Keyword Arguments:
                bucket_name {str} -- Bucket name (default: {os.environ.get('BUCKET_NAME')})
                s3_region {str} -- S3 region (default: {os.environ.get('S3_REGION')})

            Returns:
                link {str} - Link to object
            """
        return normalize_url('https://{0}.s3.{1}.amazonaws.com/{2}'.format(bucket_name, s3_region, object_name))

    def upload(self, filepath: str, filename: str, bucket_name: Optional[str] = os.environ.get('BUCKET_NAME')) -> None:
        """Uploads the file with the given name in the S3 bucket

        Arguments:
            filepath {str} -- The path to the file
            filename {str} -- Name of the file

        Keyword Arguments:
            bucket_name {str} -- S3 bucket name (default: {os.environ.get('BUCKET_NAME')})
        """
        self.__s3client.upload_file(
            Filename=filepath,
            Bucket=bucket_name,
            Key=filename,
            ExtraArgs={'ContentType': 'application/atom+xml;charset=utf-8'}
        )
