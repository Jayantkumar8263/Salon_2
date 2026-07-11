from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):# a class that inherits from S3Boto3Storage and is used to handle static files in an S3 bucket. this class is used to store static files in an S3 bucket
    location = "static"
    default_acl = None # default_acl = None means that the files will not be publicly accessible by default. This is a security measure to prevent unauthorized access to your files. You can change this setting to 'public-read' if you want your files to be publicly accessible.
    querystring_auth = False    # querystring_auth = False means that the files will not be publicly accessible by default. This is a security measure to prevent unauthorized access to your files. You can change this setting to 'public-read' if you want your files to be publicly accessible.

class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    default_acl = None
    querystring_auth = False