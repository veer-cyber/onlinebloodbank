from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO


class BloodBankVO(db.Model):
    __tablename__ = 'bloodbankmaster'
    bloodBankId = db.Column('bloodBankId', db.Integer, primary_key=True, autoincrement=True)
    bloodBankName = db.Column('bloodBankName', db.String(100), nullable=False)
    bloodBankAddress = db.Column('bloodBankAddress', db.String(100), nullable=False)
    bloodBankContact = db.Column('bloodBankContact', db.String(100), nullable=False)
    bloodBankLicense = db.Column('bloodBankLicense', db.String(100), nullable=False)
    bloodBank_CityId = db.Column('bloodBank_CityId', db.Integer, db.ForeignKey(CityVO.cityId))
    bloodBank_AreaId = db.Column('bloodBank_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    bloodBank_LoginId = db.Column('bloodBank_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'bloodBankId': self.bloodBankId,
            'bloodBankName': self.bloodBankName,
            'bloodBankAddress': self.bloodBankAddress,
            'bloodBankContact': self.bloodBankContact,
            'bloodBankLicense': self.bloodBankLicense,
            'bloodBank_CityId': self.bloodBank_CityId,
            'bloodBank_AreaId': self.bloodBank_AreaId,
            'bloodBank_LoginId': self.bloodBank_LoginId
        }


db.create_all()
