from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BloodBankVO import BloodBankVO
from project.com.vo.BloodGroupVO import BloodGroupVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.TimeSlotVO import TimeSlotVO


class AppointmentVO(db.Model):
    __tablename__ = "appointmentmaster"
    appointmentId = db.Column('appointmentId', db.Integer, primary_key=True, autoincrement=True)
    appointmentType = db.Column('appointmentType', db.String(100), nullable=False)
    appointmentDate = db.Column('appointmentDate', db.String(100), nullable=False)
    appointmentStatus = db.Column('appointmentStatus', db.String(100), nullable=False)
    appointment_CityId = db.Column('appointment_CityId', db.Integer, db.ForeignKey(CityVO.cityId))
    appointment_AreaId = db.Column('appointment_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    appointment_BloodBankId = db.Column('appointment_BloodBankId', db.Integer, db.ForeignKey(BloodBankVO.bloodBankId))
    appointment_BloodGroupId = db.Column('appointment_BloodGroupId', db.Integer,
                                         db.ForeignKey(BloodGroupVO.bloodGroupId))
    appointment_TimeSlotId = db.Column('appointment_TimeSlotId', db.Integer, db.ForeignKey(TimeSlotVO.timeSlotId))
    appointment_LoginId = db.Column('appointment_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'appointmentId': self.appointmentId,
            'appointmentType': self.appointmentType,
            'appointmentDate': self.appointmentDate,
            'appointmentStatus': self.appointmentStatus,
            'appointment_CityId': self.appointment_CityId,
            'appointment_AreaId': self.appointment_AreaId,
            'appointment_BloodBankId': self.appointment_BloodBankId,
            'appointment_BloodGroupId': self.appointment_BloodGroupId,
            'appointment_TimeSlotId': self.appointment_TimeSlotId,
            'appointment_LoginId': self.appointment_LoginId
        }


db.create_all()
