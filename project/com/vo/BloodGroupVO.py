from project import db


class BloodGroupVO(db.Model):
    __tablename__ = 'bloodgroupmaster'
    bloodGroupId = db.Column('bloodGroupId', db.Integer, primary_key=True, autoincrement=True)
    bloodGroupName = db.Column('bloodGroupName', db.String(100))

    def as_dict(self):
        return {
            'bloodGroupId': self.bloodGroupId,
            'bloodGroupName': self.bloodGroupName
        }


db.create_all()
