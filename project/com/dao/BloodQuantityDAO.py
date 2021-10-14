from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CityVO import CityVO
from project.com.vo.BloodGroupVO import BloodGroupVO
from project.com.vo.BloodQuantityVO import BloodQuantityVO
from project.com.vo.BloodBankVO import BloodBankVO


class BloodQuantityDAO:
    def insertBloodQuantity(self, bloodQuantityVO):
        db.session.add(bloodQuantityVO)

        db.session.commit()

    def viewBloodQuantity(self):
        bloodQuantityList = db.session.query(BloodQuantityVO, BloodGroupVO, AreaVO, CityVO, BloodBankVO).join(BloodGroupVO,
                                                                                 BloodQuantityVO.bloodQuantity_BloodGroupId == BloodGroupVO.bloodGroupId).join(AreaVO,
                                                                                 BloodQuantityVO.bloodQuantity_AreaId == AreaVO.areaId).join(CityVO,
                                                                                 BloodQuantityVO.bloodQuantity_CityId == CityVO.cityId).join(BloodBankVO,
                                                                                 BloodQuantityVO.bloodQuantity_BloodBankId == BloodBankVO.bloodBankId).all()

        return bloodQuantityList

    def deleteBloodQuantity(self, bloodQuantityId):
        bloodQuantityList = BloodQuantityVO.query.get(bloodQuantityId)

        db.session.delete(bloodQuantityList)

        db.session.commit()

    def editBloodQuantity(self, bloodQuantityVO):
        bloodQuantityList = BloodQuantityVO.query.filter_by(bloodQuantityId=bloodQuantityVO.bloodQuantityId)

        return bloodQuantityList

    def updateBloodQuantity(self, bloodQuantityVO):
        db.session.merge(bloodQuantityVO)

        db.session.commit()
