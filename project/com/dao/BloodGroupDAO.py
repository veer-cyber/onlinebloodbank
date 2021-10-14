from project import db
from project.com.vo.BloodGroupVO import BloodGroupVO


class BloodGroupDAO:
    def insertBloodGroup(self, bloodGroupVO):
        db.session.add(bloodGroupVO)

        db.session.commit()

    def viewBloodGroup(self):
        bloodGroupList = BloodGroupVO.query.all()

        return bloodGroupList

    def deleteBloodGroup(self, bloodGroupVO):
        bloodGroupList = BloodGroupVO.query.get(bloodGroupVO.bloodGroupId)

        db.session.delete(bloodGroupList)

        db.session.commit()

    def editBloodGroup(self, bloodGroupVO):
        bloodGroupList = BloodGroupVO.query.filter_by(bloodGroupId=bloodGroupVO.bloodGroupId).all()

        return bloodGroupList

    def updateBloodgroup(self, bloodGroupVO):
        db.session.merge(bloodGroupVO)

        db.session.commit()

    def getBloodGroupName(self, emergencyRequest_BloodGroupId):
        bloodGroupList = BloodGroupVO.query.get(emergencyRequest_BloodGroupId)
        return bloodGroupList
