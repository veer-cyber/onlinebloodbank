from project import db
from project.com.vo.BloodBankVO import BloodBankVO
from project.com.vo.TimeSlotVO import TimeSlotVO


class TimeSlotDAO:
    def insertTimeSlot(self, timeSlotVO):
        db.session.add(timeSlotVO)
        db.session.commit()

    def viewTimeSlot(self):
        timeSlotVOList = db.session.query(TimeSlotVO, BloodBankVO).join(BloodBankVO,
                                                                        TimeSlotVO.timeSlot_BloodBankId == BloodBankVO.bloodBankId).all()

        return timeSlotVOList

    def viewBloodBankTimeSlot(self,timeSlot_BloodBankId):
        timeSlotVOList = TimeSlotVO.query.filter_by(timeSlot_BloodBankId=timeSlot_BloodBankId).all()

        return timeSlotVOList

    def deleteTimeSlot(self, timeSlotId):
        timeSlotList = TimeSlotVO.query.get(timeSlotId)

        db.session.delete(timeSlotList)

        db.session.commit()

    # def editTimeSlot(self, timeSlotVO):
    #     timeSlotList = TimeSlotVO.query.filter_by(timeSlotId=timeSlotVO.timeSlotId).all()
    #
    #     return timeSlotList
    #
    # def updateTimeSlot(self, timeSlotVO):
    #     db.session.merge(timeSlotVO)
    #
    #     db.session.commit()

    def searchBloodBank(self, loginId):
        bloodBankVOList = BloodBankVO.query.filter_by(bloodBank_LoginId=loginId).all()

        return bloodBankVOList

    def ajaxTimeSlotAppointment(self, timeSlotVO):
        timeSlotList = TimeSlotVO.query.filter_by(timeSlot_BloodBankId=timeSlotVO.timeSlot_BloodBankId).all()
        return timeSlotList
