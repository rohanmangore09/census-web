from app import db

class HouseholdMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    household_id = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    married = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"<Member {self.name}>"
