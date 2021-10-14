from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BloodGroupVO import BloodGroupVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.BloodBankVO import BloodBankVO


class EmergencyRequestVO(db.Model):
    __tablename__ = 'emergencyrequestmaster'
    emergencyRequestId = db.Column('emergencyRequestId', db.Integer, primary_key=True, autoincrement=True)
    emergencyRequestQuantity = db.Column('emergencyRequestQuantity', db.String(100), nullable=False)
    emergencyRequestDate = db.Column('emergencyRequestDate', db.String(100), nullable=False)
    emergencyRequestTime = db.Column('emergencyRequestTime', db.String(100), nullable=False)
    emergencyRequestStatus = db.Column('emergencyRequestStatus', db.String(100), nullable=False)
    emergencyRequestPersonRequire = db.Column('emergencyRequestPersonRequire', db.Integer, nullable=False)
    emergencyRequest_CityId = db.Column('emergencyRequest_CityId', db.Integer, db.ForeignKey(CityVO.cityId))
    emergencyRequest_AreaId = db.Column('emergencyRequest_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    emergencyRequest_BloodGroupId = db.Column('emergencyRequest_BloodGroupId', db.Integer, db.ForeignKey(BloodGroupVO.bloodGroupId))
    emergencyRequest_BloodBankId = db.Column('emergencyRequest_BloodBankId', db.Integer, db.ForeignKey(BloodBankVO.bloodBankId))
    emergencyRequest_LoginId = db.Column('emergencyRequest_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'emergencyRequestId': self.emergencyRequestId,
            'emergencyRequestQuantity': self.emergencyRequestQuantity,
            'emergencyRequestDate': self.emergencyRequestDate,
            'emergencyRequestTime': self.emergencyRequestTime,
            'emergencyRequestStatus': self.emergencyRequestStatus,
            'emergencyRequestPersonRequire': self.emergencyRequestPersonRequire,
            'emergencyRequest_CityId': self.emergencyRequest_CityId,
            'emergencyRequest_AreaId': self.emergencyRequest_AreaId,
            'emergencyRequest_BloodGroupId': self.emergencyRequest_BloodGroupId,
            'emergencyRequest_BloodBankId': self.emergencyRequest_BloodBankId,
            'emergencyRequest_LoginId': self.emergencyRequest_LoginId
        }


db.create_all()
