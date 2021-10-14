from project import db
from project.com.vo.LoginVO import LoginVO


class LoginDAO:
    def insertLogin(self, loginVO):
        db.session.add(loginVO)

        db.session.commit()

    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername, loginPassword=loginVO.loginPassword)

        return loginList

    def findUser(self, loginUsername):
        loginList = LoginVO.query.filter_by(loginUsername=loginUsername)

        return loginList

    def forgotPassword(self,loginVO):
        db.session.merge(loginVO)

        db.session.commit()

    def resetPassword(self,loginVO):
        db.session.merge(loginVO)

        db.session.commit()

    def faceValidateLogin(self,name):
        loginList = LoginVO.query.filter_by(loginFileName=name)

        return loginList

    def addNameForFr(self,loginVO):
        db.session.merge(loginVO)

        db.session.commit()