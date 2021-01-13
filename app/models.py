from . import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return "ID: {}, Image Link: {}".format(self.id, self.link)