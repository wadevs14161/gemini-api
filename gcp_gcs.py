class gcs_signed_url_v4:

    from google.cloud import storage
    import datetime
    import os
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= 'google_secret_key.json'

    def __init__(self, bucket_name, blob_name):
        __class__.bucket_name = bucket_name
        __class__.blob_name = blob_name
        __class__.storage_client = __class__.storage.Client()
        __class__.bucket = __class__.storage_client.bucket(__class__.bucket_name)
        __class__.blob = __class__.bucket.blob(__class__.blob_name)

    def generate_upload_signed_url_v4(self):
        """Generates a v4 signed URL for uploading a blob using HTTP PUT.

        Note that this method requires a service account key file. You can not use
        this if you are using Application Default Credentials from Google Compute
        Engine or from the Google Cloud SDK.
        """

        url = __class__.blob.generate_signed_url(
            version="v4",
            # This URL is valid for 15 minutes
            expiration=__class__.datetime.timedelta(minutes=15),
            # Allow PUT requests using this URL.
            method="PUT",
            content_type="audio/mpeg",
        )

        print("Generated PUT signed URL:")
        print("-" * 30)
        print(url)
        print("-" * 30)

        return url


    def generate_download_signed_url_v4(self):
        """Generates a v4 signed URL for downloading a blob.

        Note that this method requires a service account key file. You can not use
        this if you are using Application Default Credentials from Google Compute
        Engine or from the Google Cloud SDK.
        """

        url = __class__.blob.generate_signed_url(
            version="v4",
            # This URL is valid for 15 minutes
            expiration=__class__.datetime.timedelta(minutes=15),
            # Allow GET requests using this URL.
            method="GET",
        )

        print("Generated GET signed URL for\n\tBUCKET_NAME/{}:\n\tBLOB_NAME/{}:".format(__class__.bucket_name, __class__.blob_name))
        print("-" * 30)
        print(url)
        print("-" * 30)

        return url


        
if __name__ == "__main__":
    signed_url = gcs_signed_url_v4("wenshin-tts-bucket", "test_class.mp3")
    upload_url = signed_url.generate_upload_signed_url_v4()

    from upload import upload_audio

    upload_audio(upload_url)

    download_url = signed_url.generate_download_signed_url_v4()
