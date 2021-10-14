from sqlalchemy import func

from project import db
from project.com.vo.AppointmentVO import AppointmentVO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BloodBankVO import BloodBankVO
from project.com.vo.BloodGroupVO import BloodGroupVO
from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.TimeSlotVO import TimeSlotVO


class AppointmentDAO:
    def insertAppointment(self, appointmentVO):
        db.session.add(appointmentVO)

        db.session.commit()

    def viewAppointmentByUser(self, appointmentVO):
        appointmentVOList = db.session.query(AppointmentVO, LoginVO, CityVO, AreaVO, BloodBankVO, BloodGroupVO,
                                             TimeSlotVO).join(
            BloodBankVO,
            AppointmentVO.appointment_BloodBankId == BloodBankVO.bloodBankId) \
            .join(AreaVO, AppointmentVO.appointment_AreaId == AreaVO.areaId) \
            .join(CityVO, AppointmentVO.appointment_CityId == CityVO.cityId) \
            .join(BloodGroupVO, AppointmentVO.appointment_BloodGroupId == BloodGroupVO.bloodGroupId) \
            .join(TimeSlotVO, AppointmentVO.appointment_TimeSlotId == TimeSlotVO.timeSlotId) \
            .join(LoginVO, AppointmentVO.appointment_LoginId == LoginVO.loginId) \
            .filter(AppointmentVO.appointment_LoginId == appointmentVO.appointment_LoginId).all()

        return appointmentVOList

    def viewAppointmentByAdmin(self):
        appointmentVOList = db.session.query(AppointmentVO, LoginVO, CityVO, AreaVO, BloodBankVO, BloodGroupVO,
                                             TimeSlotVO).join(
            BloodBankVO,
            AppointmentVO.appointment_BloodBankId == BloodBankVO.bloodBankId).join(
            AreaVO, AppointmentVO.appointment_AreaId == AreaVO.areaId).join(CityVO,
                                                                            AppointmentVO.appointment_CityId == CityVO.cityId).join(
            BloodGroupVO, AppointmentVO.appointment_BloodGroupId == BloodGroupVO.bloodGroupId).join(
            TimeSlotVO, AppointmentVO.appointment_TimeSlotId == TimeSlotVO.timeSlotId).join(
            LoginVO, AppointmentVO.appointment_LoginId == LoginVO.loginId).all()

        return appointmentVOList

    def viewAppointmentByBloodBank(self, appointmentVO):
        appointmentVOList = db.session.query(AppointmentVO, LoginVO, CityVO, AreaVO, BloodBankVO, BloodGroupVO,
                                             TimeSlotVO).join(
            BloodBankVO,
            AppointmentVO.appointment_BloodBankId == BloodBankVO.bloodBankId).join(
            AreaVO, AppointmentVO.appointment_AreaId == AreaVO.areaId).join(CityVO,
                                                                            AppointmentVO.appointment_CityId == CityVO.cityId).join(
            BloodGroupVO, AppointmentVO.appointment_BloodGroupId == BloodGroupVO.bloodGroupId).join(
            TimeSlotVO, AppointmentVO.appointment_TimeSlotId == TimeSlotVO.timeSlotId).join(
            LoginVO, AppointmentVO.appointment_LoginId == LoginVO.loginId).filter(
            AppointmentVO.appointment_BloodBankId == appointmentVO.appointment_BloodBankId).all()

        return appointmentVOList

    def updateAppointment(self, appointmentVO):
        db.session.merge(appointmentVO)

        db.session.commit()

    def getAppointmentDetailsByLoginId(self, appointmentVO):
        appointmentVOList = db.session.query(AppointmentVO.appointmentType, func.count(AppointmentVO.appointmentType)) \
            .filter_by(appointment_LoginId=appointmentVO.appointment_LoginId) \
            .group_by(AppointmentVO.appointmentType).all()
        return appointmentVOList

    def getAppointmentDetailsByBloodBankId(self, appointmentVO):
        appointmentVOList = db.session.query(AppointmentVO.appointmentType, func.count(AppointmentVO.appointmentType)) \
            .filter_by(appointment_BloodBankId=appointmentVO.appointment_BloodBankId) \
            .group_by(AppointmentVO.appointmentType).all()
        return appointmentVOList

    def ajaxGetGraphData(self, appointmentVO):
        appointmentVOList = db.session.query(AppointmentVO.appointmentType, func.count(AppointmentVO.appointmentType)) \
            .filter_by(appointment_BloodBankId=appointmentVO.appointment_BloodBankId) \
            .group_by(AppointmentVO.appointmentType).all()
        return appointmentVOList
