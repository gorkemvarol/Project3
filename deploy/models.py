def create_classes(db):
    class Patient(db.Model):
        __tablename__ = 'patients'

        id = db.Column(db.Integer, primary_key=True)
        sex = db.Column(db.Integer)
        sex = db.Column(db.Integer)
        cp =db.Column(db.Integer)
        trestbps =db.Column(db.Integer)
        chol = db.Column(db.Integer)
        fbs = db.Column(db.Integer)
        restecg =db.Column(db.Integer)
        thalach = db.Column(db.Integer)
        exang = db.Column(db.Integer)
        oldpeak = db.Column(db.Float)
        slope = db.Column(db.Integer)
        ca = db.Column(db.Integer)
        def __repr__(self):
            return '<Patient %r>' % (self.name)
    return Patient
