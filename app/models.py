import uuid
from . import db

def generate_uuid():
    return str(uuid.uuid4())

class Image(db.Model):
    id = db.Column(db.String(200), primary_key=True, default=generate_uuid, unique=True)
    file_name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "ID: {}, Image Name: {}".format(self.id, self.file_name)