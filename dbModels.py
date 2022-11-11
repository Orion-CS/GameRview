
from app import db


# === Database Models ===
# Model for Movie table
class Movie(db.Model):
    __tablename__ = 'Movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.REAL, nullable=False)

    def __str__(self):
        return f"Movie(title={self.title}, year={self.year}, budget={self.buget})"

    def __repr__(self):
        return f"Movie({self.title})"