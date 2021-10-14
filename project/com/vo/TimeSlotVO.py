from project import db
from project.com.vo.BloodBankVO import BloodBankVO


class TimeSlotVO(db.Model):
    __tablename__ = 'timeslotmaster'
    timeSlotId = db.Column('timeSlotId', db.Integer, primary_key=True, autoincrement=True)
    timeSlotName = db.Column('timeSlotName', db.String(100))
    timeSlot = db.Column('timeSlot', db.String(100))
    timeSlot_BloodBankId = db.Column('timeSlot_BloodBankId', db.Integer, db.ForeignKey(BloodBankVO.bloodBankId))

    def as_dict(self):
        return {
            'timeSlotId': self.timeSlotId,
            'timeSlotName': self.timeSlotName,
            'timeSlot': self.timeSlot,
            'timeSlot_BloodBankId': self.timeSlot_BloodBankId
        }


db.create_all()
