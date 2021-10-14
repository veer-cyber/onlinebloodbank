from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BloodGroupVO import BloodGroupVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO


class UserVO(db.Model):
    __tablename__ = 'usermaster'
    userId = db.Column('userId', db.Integer, primary_key=True, autoincrement=True)
    userFirstName = db.Column('userFirstName', db.String(100), nullable=False)
    userLastName = db.Column('userLastName', db.String(100), nullable=False)
    userBirthDate = db.Column('userBirthDate', db.String(100), nullable=False)
    user_BloodGroupId = db.Column('user_BloodGroupId', db.Integer, db.ForeignKey(BloodGroupVO.bloodGroupId))
    userGender = db.Column('userGender', db.String(100), nullable=False)
    userWeight = db.Column('userWeight', db.String(100), nullable=False)
    userHeight = db.Column('userHeight', db.String(100), nullable=False)
    userContact = db.Column('userContact', db.String(100), nullable=False)
    userFileName = db.Column('userFileName', db.String(100), nullable=False)
    userFilePath = db.Column('userFilePath', db.String(100), nullable=False)
    user_CityId = db.Column('user_CityId', db.Integer, db.ForeignKey(CityVO.cityId))
    user_AreaId = db.Column('user_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    userAddress = db.Column('userAddress', db.String(100), nullable=False)
    userDiseases = db.Column('userDiseases', db.String(100), nullable=False)
    user_LoginId = db.Column('user_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'userId': self.userId,
            'userFirstName': self.userFirstName,
            'userLastName': self.userLastName,
            'userName': self.userName,
            'userBloodGroup': self.userBloodGroup,
            'userGender': self.userGender,
            'userWeight': self.userWeight,
            'userHeight': self.userHeight,
            'userContact': self.userContact,
            'userFileName': self.userFileName,
            'userFilePath': self.userFilePath,
            'user_CityId': self.user_CityId,
            'user_AreaId': self.user_AreaId,
            'userAddress': self.userAddress,
            'userDiseases': self.userDiseases,
            'user_LoginId': self.user_LoginId
        }


db.create_all()
