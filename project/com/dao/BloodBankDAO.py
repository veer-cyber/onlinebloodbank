from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BloodBankVO import BloodBankVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO


class BloodBankDAO:
    def insertBloodBank(self, bloodBankVO):
        db.session.add(bloodBankVO)

        db.session.commit()

    def viewAdminBloodBank(self):
        bloodBankList = db.session.query(BloodBankVO, LoginVO, CityVO, AreaVO) \
            .join(LoginVO, BloodBankVO.bloodBank_LoginId == LoginVO.loginId) \
            .join(CityVO, BloodBankVO.bloodBank_CityId == CityVO.cityId) \
            .join(AreaVO, BloodBankVO.bloodBank_AreaId == AreaVO.areaId).all()

        return bloodBankList

    def getBloodbankData(self, loginId):
        bloodBankList = LoginVO.query.filter_by(loginId=loginId).all()
        return bloodBankList

    def getBloodBank(self, loginId):
        bloodBankList = BloodBankVO.query.filter_by(bloodBank_LoginId=loginId).all()
        return bloodBankList

    def manageBloodbank(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def editProfile(self, bloodBankVO):
        db.session.merge(bloodBankVO)

        db.session.commit()

    def ajaxBloodBankAppointment(self, bloodBankVO):
        bloodBankList = BloodBankVO.query.filter_by(bloodBank_AreaId=bloodBankVO.bloodBank_AreaId).all()
        return bloodBankList
