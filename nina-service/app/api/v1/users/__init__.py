from .messenger import Messenger

UploadMessenger = Messenger('http://upload-service:5000/api/v1/upload?blob_name=%s')