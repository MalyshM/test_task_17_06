import asyncio
import io
import os
from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from dotenv import load_dotenv

class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self,
            file_path: str,
    ):
        object_name = file_path.split("/")[-1]  # /users/artem/cat.jpg
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file,
                    )
                print(f"File {object_name} uploaded to {self.bucket_name}")
        except ClientError as e:
            print(f"Error uploading file: {e}")

    async def upload_file_bytes(
            self,
            file_data: bytes,
            object_name: str
    ):
        try:
            async with self.get_client() as client:
                file_stream = io.BytesIO(file_data)
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file_stream,
                )
                print(f"File {object_name} uploaded to {self.bucket_name}")
        except ClientError as e:
            print(f"Error uploading file: {e}")

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")

    async def get_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                data = await response["Body"].read()
                return data
                # with open(destination_path, "wb") as file:
                #     file.write(data)
                # print(f"File {object_name} downloaded to {destination_path}")
        except ClientError as e:
            print(f"Error downloading file: {e}")

    async def get_file_link(self, object_name: str) -> str:
        try:
            async with self.get_client() as client:
                # resp = await client.get_object_acl(Bucket= self.bucket_name, Key=object_name)
                # print(resp)
                params = {"Bucket": self.bucket_name, "Key": object_name}
                url = await client.generate_presigned_url(
                    "get_object", Params=params, ExpiresIn=3600
                )
                return url
        except ClientError as e:
            print(f"Error getting file link: {e}")
            return ""

load_dotenv()

s3_client = S3Client(
    access_key=os.getenv("ACCESS_KEY"),
    secret_key=os.getenv("SECRET_KEY"),
    endpoint_url=os.getenv("ENDPOINT_URL"),
    bucket_name=os.getenv("BUCKET_NAME"),
)
