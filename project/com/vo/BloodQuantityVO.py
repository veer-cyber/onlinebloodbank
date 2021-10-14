from project import db
from project.com.vo.BloodGroupVO import BloodGroupVO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CityVO import CityVO
from project.com.vo.BloodBankVO import BloodBankVO


class BloodQuantityVO(db.Model):
    __tablename__ = "bloodquantitymaster"
    bloodQuantityId = db.Column('bloodQuantityId', db.Integer, primary_key=True, autoincrement=True)
    bloodQuantityYear = db.Column('bloodQuantityYear', db.Integer, nullable=False)
    bloodQuantityMonth = db.Column('bloodQuantityMonth', db.String(100), nullable=False)
    bloodQuantity = db.Column('bloodQuantity', db.Integer, nullable=False)
    bloodQuantityRequirement = db.Column('bloodQuantityRequirement', db.Integer, nullable=False)
    bloodQuantity_BloodGroupId = db.Column('bloodQuantity_BloodGroupId', db.Integer,
                                           db.ForeignKey(BloodGroupVO.bloodGroupId))
    bloodQuantity_AreaId = db.Column('bloodQuantity_AreaId', db.Integer,
                                           db.ForeignKey(AreaVO.areaId))
    bloodQuantity_CityId = db.Column('bloodQuantity_CityId', db.Integer,
                                           db.ForeignKey(CityVO.cityId))
    bloodQuantity_BloodBankId = db.Column('bloodQuantity_BloodBankId', db.Integer,
                                     db.ForeignKey(BloodBankVO.bloodBankId))
    bloodQuantityDate = db.Column('bloodQuantityDate', db.String(100), nullable=False)
    bloodQuantityStatus = db.Column('bloodQuantityStatus', db.String(100), nullable=False)

    def as_dict(self):
        return {
            'bloodQuantityId': self.bloodQuantityId,
            'bloodQuantityYear': self.bloodQuantityYear,
            'bloodQuantityMonth': self.bloodQuantityMonth,
            'bloodQuantity': self.bloodQuantity,
            'bloodQuantityRequirement': self.bloodQuantityRequirement,
            'bloodQuantity_BloodGroupId': self.bloodQuantity_BloodGroupId,
            'bloodQuantity_AreaId': self.bloodQuantity_AreaId,
            'bloodQuantity_CityId': self.bloodQuantity_CityId,
            'bloodQuantity_BloodBankId': self.bloodQuantity_BloodBankId,
            'bloodQuantityDate': self.bloodQuantityDate,
            'bloodQuantityStatus': self.bloodQuantityStatus
        }


db.create_all()
