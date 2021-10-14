from project import db
from project.com.vo.EmergencyRequestVO import EmergencyRequestVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.UserVO import UserVO


class AcceptEmergencyRequestVO(db.Model):
    __tablename__ = 'acceptemergencyrequest'
    acceptEmergencyRequestId = db.Column('acceptEmergencyRequestId', db.Integer, primary_key=True, autoincrement=True)
    acceptEmergencyRequest_UserId = db.Column('acceptEmergencyRequest_UserId', db.Integer, db.ForeignKey(UserVO.userId))
    acceptEmergencyRequest_LoginId = db.Column('acceptEmergencyRequest_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    acceptEmergencyRequestDate = db.Column('acceptEmergencyRequestDate', db.String(100), nullable=False)
    acceptEmergencyRequestTime = db.Column('acceptEmergencyRequestTime', db.String(100), nullable=False)
    acceptEmergencyRequestStatus = db.Column('acceptEmergencyRequestStatus', db.String(100), nullable=False)
    acceptEmergencyRequest_EmergencyRequestId = db.Column('acceptEmergencyRequest_EmergencyRequestId', db.Integer, db.ForeignKey(EmergencyRequestVO.emergencyRequestId))

    def as_dict(self):
        return {
            'acceptEmergencyRequestId': self.acceptEmergencyRequestId,
            'acceptEmergencyRequest_UserId': self.acceptEmergencyRequest_UserId,
            'acceptEmergencyRequest_LoginId': self.acceptEmergencyRequest_LoginId,
            'acceptEmergencyRequestDate': self.acceptEmergencyRequestDate,
            'acceptEmergencyRequestTime': self.acceptEmergencyRequestTime,
            'acceptEmergencyRequest_EmergencyRequestId': self.acceptEmergencyRequest_EmergencyRequestId
        }


db.create_all()
