from project import db
from project.com.vo.EmergencyRequestVO import EmergencyRequestVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.BloodBankVO import BloodBankVO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CityVO import CityVO
from project.com.vo.BloodGroupVO import BloodGroupVO
from project.com.vo.AcceptEmergencyRequestVO import AcceptEmergencyRequestVO


class EmergencyRequestDAO:
    def insertEmergencyRequest(self, emergencyRequestVO):
        db.session.add(emergencyRequestVO)

        db.session.commit()

    def viewEmergencyRequest(self):
        emergencyRequestList = db.session.query(EmergencyRequestVO, AreaVO, CityVO, BloodGroupVO, LoginVO, BloodBankVO).join(CityVO, EmergencyRequestVO.emergencyRequest_CityId == CityVO.cityId).join(AreaVO, EmergencyRequestVO.emergencyRequest_AreaId == AreaVO.areaId).join(BloodGroupVO,EmergencyRequestVO.emergencyRequest_BloodGroupId == BloodGroupVO.bloodGroupId).join(LoginVO,EmergencyRequestVO.emergencyRequest_LoginId == LoginVO.loginId).join(BloodBankVO,EmergencyRequestVO.emergencyRequest_BloodBankId == BloodBankVO.bloodBankId).all()

        return emergencyRequestList

    def completeEmergencyRequest(self, emergencyRequestVO):

        db.session.merge(emergencyRequestVO)

        db.session.commit()

    def viewUserEmergencyRequest(self, user_BloodGroupId, user_AreaId, status):
        emergencyRequestList = db.session.query(EmergencyRequestVO, AreaVO, CityVO, BloodGroupVO, LoginVO,
                                                BloodBankVO).join(CityVO,
                                                                  EmergencyRequestVO.emergencyRequest_CityId == CityVO.cityId).join(
            AreaVO, EmergencyRequestVO.emergencyRequest_AreaId == AreaVO.areaId).join(BloodGroupVO,
                                                                                      EmergencyRequestVO.emergencyRequest_BloodGroupId == BloodGroupVO.bloodGroupId).join(
            LoginVO, EmergencyRequestVO.emergencyRequest_LoginId == LoginVO.loginId).join(BloodBankVO,
                                                                                          EmergencyRequestVO.emergencyRequest_BloodBankId == BloodBankVO.bloodBankId).filter(EmergencyRequestVO.emergencyRequestStatus==status, EmergencyRequestVO.emergencyRequest_AreaId==user_AreaId, EmergencyRequestVO.emergencyRequest_BloodGroupId==user_BloodGroupId).all()

        return emergencyRequestList

    def insertAcceptEmergencyRequest(self, acceptEmergencyRequestVO):
        db.session.add(acceptEmergencyRequestVO)

        db.session.commit()

    def viewAcceptEmergencyRequest(self):
        acceptEmergencyRequestList = AcceptEmergencyRequestVO.query.all()

        return acceptEmergencyRequestList

    def findPersonCount(self, emergencyRequestId):
        acceptEmergencyRequestPersonList = AcceptEmergencyRequestVO.query.filter_by(acceptEmergencyRequest_EmergencyRequestId=emergencyRequestId)

        return acceptEmergencyRequestPersonList

    def findPersonCountFromEmergencyRequest(self, emergencyRequestId):
        emergencyRequestPersonList = db.session.query(EmergencyRequestVO, AreaVO, CityVO, BloodGroupVO, LoginVO, BloodBankVO).join(CityVO,
                                                                                                      EmergencyRequestVO.emergencyRequest_CityId == CityVO.cityId).join(
            AreaVO, EmergencyRequestVO.emergencyRequest_AreaId == AreaVO.areaId).join(BloodGroupVO,
                                                                                      EmergencyRequestVO.emergencyRequest_BloodGroupId == BloodGroupVO.bloodGroupId).join(
            LoginVO, EmergencyRequestVO.emergencyRequest_LoginId == LoginVO.loginId).join(BloodBankVO,
                                                                                          EmergencyRequestVO.emergencyRequest_BloodBankId == BloodBankVO.bloodBankId).filter(EmergencyRequestVO.emergencyRequestId==emergencyRequestId).all()
        return emergencyRequestPersonList
    # def viewComplain(self, complainVO):
    #     complainList = ComplainVO.query.filter_by(complainFrom_LoginId=complainVO.complainFrom_LoginId).all()
    #
    #     return complainList
    #
    # def viewBloodbankComplain(self, complainVO):
    #     complainList = db.session.query(ComplainVO, LoginVO).join(LoginVO,
    #                                                               ComplainVO.complainFrom_LoginId == LoginVO.loginId).filter(
    #         ComplainVO.complainStatus == complainVO.complainStatus).all()
    #     return complainList
    #
    # def viewUserComplain(self, complainVO):
    #     complainList = db.session.query(ComplainVO, LoginVO).join(LoginVO,
    #                                                               ComplainVO.complainFrom_LoginId == LoginVO.loginId).filter(
    #         ComplainVO.complainStatus == complainVO.complainStatus).all()
    #     return complainList
    #
    # def insertComplainReply(self, complainVO):
    #     db.session.merge(complainVO)
    #
    #     db.session.commit()
    #
    # def viewComplainReply(self, complainVO):
    #     complainList = ComplainVO.query.filter_by(complainId=complainVO.complainId).all()
    #
    #     return complainList
    #
    # def deleteComplain(self, complainVO):
    #     complainList = ComplainVO.query.get(complainVO.complainId)
    #
    #     db.session.delete(complainList)
    #
    #     db.session.commit()
    #
    #     return complainList
