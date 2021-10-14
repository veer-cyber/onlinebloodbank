from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BloodGroupVO import BloodGroupVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.UserVO import UserVO


class UserDAO:
    def insertUser(self, userVO):
        db.session.add(userVO)

        db.session.commit()

    def viewAdminUser(self):
        userList = db.session.query(UserVO, LoginVO, AreaVO, CityVO, BloodGroupVO).join(LoginVO,
                                                                                        UserVO.user_LoginId == LoginVO.loginId).join(
            AreaVO, UserVO.user_AreaId == AreaVO.areaId).join(CityVO, UserVO.user_CityId == CityVO.cityId).join(
            BloodGroupVO, UserVO.user_BloodGroupId == BloodGroupVO.bloodGroupId).all()

        return userList

    def getUserData(self, loginId):
        userList = LoginVO.query.filter_by(loginId=loginId).all()

        return userList

    def getUserAllData(self, loginId):
        userAllList = UserVO.query.filter_by(user_LoginId=loginId).all()

        return userAllList

    def manageUser(self, loginVO):
        db.session.merge(loginVO)

        db.session.commit()

    def editProfile(self, userVO):
        db.session.merge(userVO)

        db.session.commit()

    def getUserForEmergencyRequest(self, emergencyRequest_AreaId, emergencyRequest_BloodGroupId):

        userVOList = db.session.query(UserVO, LoginVO).join(LoginVO,UserVO.user_LoginId == LoginVO.loginId).filter(UserVO.user_AreaId == emergencyRequest_AreaId, UserVO.user_BloodGroupId == emergencyRequest_BloodGroupId).all()

        return userVOList
