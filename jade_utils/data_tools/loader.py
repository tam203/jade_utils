from boto.s3.connection import S3Connection
import os

class Loader:
    """Class to discover data files."""
    def __init__(self):
        self.local_path = '/usr/local/share/notebooks/data'

    def list_datasets(self):
        """List available datasets."""
        return os.listdir(self.local_path)

    def list_files(self, dataset):
        """
        List files from specific dataset.

        Args:

        * dataset:
            Name of dataset to search for.
        """
        files = self._list_keys(dataset)
        return [os.path.join(self.local_path, f) for f in files]

    def _list_keys(self, bucket):
        conn = S3Connection()
        s3_bucket = conn.get_bucket(bucket)
        return ['{}/{}'.format(k.bucket.name, k.key) for k in s3_bucket]
