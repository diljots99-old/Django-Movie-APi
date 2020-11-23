
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


class FirebaseSources:
    def __init__(self,config):

        

        self.cred = credentials.Certificate( config)
        if config.get("project_id") in firebase_admin._apps:
            self.app =firebase_admin.get_app(config.get("project_id"))
        else:
            self.app = firebase_admin.initialize_app(self.cred,name=config.get("project_id"))

        bucketName = f"{self.cred.project_id}.appspot.com"
        self.bucket = storage.bucket(bucketName,app=self.app)

        print(self.bucket)

    def get_bucket(self):
        return self.bucket

    def list_bucket(self):
        return self.bucket.list_blobs()

    def get_public_url(self,filepath):

        blob = self.bucket.blob(filepath)
        blob.make_public()
        return blob.public_url
