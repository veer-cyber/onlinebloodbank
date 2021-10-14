from flask import request, render_template, jsonify, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.AppointmentDAO import AppointmentDAO
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.BloodBankDAO import BloodBankDAO
from project.com.dao.BloodGroupDAO import BloodGroupDAO
from project.com.dao.CityDAO import CityDAO
from project.com.dao.TimeSlotDAO import TimeSlotDAO
from project.com.vo.AppointmentVO import AppointmentVO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BloodBankVO import BloodBankVO
from project.com.vo.TimeSlotVO import TimeSlotVO


@app.route('/user/ajaxAreaAppointment')
def userAjaxAreaAppointment():
    try:
        areaVO = AreaVO()
        areaDAO = AreaDAO()

        area_CityId = request.args.get('appointment_CityId')
        print('area_CityId::', area_CityId)

        areaVO.area_CityId = area_CityId

        ajaxBloodBankAreaList = areaDAO.ajaxArea(areaVO)

        ajaxBloodBankAreaJson = [i.as_dict() for i in ajaxBloodBankAreaList]

        return jsonify(ajaxBloodBankAreaJson)

    except Exception as ex:
        print(ex)


@app.route('/user/ajaxBloodBankAppointment')
def userAjaxBloodBankAppointment():
    try:
        bloodBankVO = BloodBankVO()

        bloodBankDAO = BloodBankDAO()

        bloodBank_AreaId = request.args.get('appointment_AreaId')
        print('bloodBank_AreaId::', bloodBank_AreaId)

        bloodBankVO.bloodBank_AreaId = bloodBank_AreaId

        ajaxAppointmentBloodBankList = bloodBankDAO.ajaxBloodBankAppointment(bloodBankVO)
        print("::", ajaxAppointmentBloodBankList)

        ajaxAppointmentBloodBankJson = [i.as_dict() for i in ajaxAppointmentBloodBankList]
        print('ajaxAppointmentBloodBankJson::', ajaxAppointmentBloodBankJson)

        return jsonify(ajaxAppointmentBloodBankJson)

    except Exception as ex:
        print(ex)


@app.route('/user/ajaxTimeSlotAppointment')
def userAjaxTimeSlotAppointment():
    try:
        timeSlotVO = TimeSlotVO()

        timeSlotDAO = TimeSlotDAO()

        timeSlot_BloodBankId = request.args.get('appointment_BloodBankId')
        print('timeSlot_BloodBankId::', timeSlot_BloodBankId)

        timeSlotVO.timeSlot_BloodBankId = timeSlot_BloodBankId

        ajaxAppointmentTimeSlotList = timeSlotDAO.ajaxTimeSlotAppointment(timeSlotVO)
        print("ajaxAppointmentTimeSlotList::", ajaxAppointmentTimeSlotList)

        ajaxAppointmentTimeSlotJson = [i.as_dict() for i in ajaxAppointmentTimeSlotList]

        return jsonify(ajaxAppointmentTimeSlotJson)

    except Exception as ex:
        print(ex)


# _____________________________________________________________________________________________________________________


@app.route('/user/loadAppointment', methods=['GET'])
def userLoadAppointment():
    try:
        if adminLoginSession() == "user":
            cityDAO = CityDAO()
            cityVOList = cityDAO.viewCity()

            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            bloodBankDAO = BloodBankDAO()
            bloodBankVOList = bloodBankDAO.viewAdminBloodBank()

            bloodGroupDAO = BloodGroupDAO()
            bloodGroupVOList = bloodGroupDAO.viewBloodGroup()

            timeSlotDAO = TimeSlotDAO()
            timeSlotVOList = timeSlotDAO.viewTimeSlot()

            return render_template('user/addAppointment.html', cityVOList=cityVOList, areaVOList=areaVOList,
                                   bloodBankVOList=bloodBankVOList, bloodGroupVOList=bloodGroupVOList,
                                   timeSlotVOList=timeSlotVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertAppointment', methods=['POST'])
def userInsertAppointment():
    try:
        if adminLoginSession() == "user":
            appointmentType = request.form['appointmentType']
            appointment_BloodGroupId = request.form['appointment_BloodGroupId']
            print("11111111")
            appointment_CityId = request.form['appointment_CityId']
            appointment_AreaId = request.form['appointment_AreaId']
            print("2222222222")
            appointment_BloodBankId = request.form['appointment_BloodBankId']
            appointment_TimeSlotId = request.form['appointment_TimeSlotId']
            appointmentDate = request.form['appointmentDate']
            appointmentStatus = 'Pending'
            print("3333333333333")

            appointmentVO = AppointmentVO()
            appointmentDAO = AppointmentDAO()
            print("44444444444444")

            appointmentVO.appointmentType = appointmentType
            appointmentVO.appointment_AreaId = appointment_AreaId
            print("55555555555")
            appointmentVO.appointment_BloodBankId = appointment_BloodBankId
            appointmentVO.appointment_BloodGroupId = appointment_BloodGroupId
            appointmentVO.appointment_CityId = appointment_CityId
            appointmentVO.appointment_TimeSlotId = appointment_TimeSlotId
            appointmentVO.appointmentDate = appointmentDate
            appointmentVO.appointmentStatus = appointmentStatus
            appointmentVO.appointment_LoginId = session['session_loginId']
            print("666666666666666666")

            appointmentDAO.insertAppointment(appointmentVO)
            print("7777777777777")

            return redirect(url_for('userViewAppointment'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewAppointment')
def userViewAppointment():
    try:
        if adminLoginSession() == "user":
            appointmentVO = AppointmentVO()
            appointmentDAO = AppointmentDAO()

            appointmentVO.appointment_LoginId = session['session_loginId']

            appointmentVOList = appointmentDAO.viewAppointmentByUser(appointmentVO)
            return render_template('user/viewAppointment.html', appointmentVOList=appointmentVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# --------------------------BLOOD BANK------------------------------------------

@app.route('/bloodbank/viewAppointment', methods=['GET'])
def bloodbankViewAppointment():
    try:
        if adminLoginSession() == "bloodbank":

            appointmentVO = AppointmentVO()
            appointmentDAO = AppointmentDAO()

            bloodBankDAO = BloodBankDAO()

            loginId = session['session_loginId']

            bloodBankVOList = bloodBankDAO.getBloodBank(loginId)

            bloodBankDictList = [i.as_dict() for i in bloodBankVOList]

            appointment_BloodBankId = bloodBankDictList[0]['bloodBankId']
            appointmentVO.appointment_BloodBankId = appointment_BloodBankId
            print(appointment_BloodBankId)

            appointmentVOList = appointmentDAO.viewAppointmentByBloodBank(appointmentVO)
            print("11111111111111:", appointmentVOList)
            return render_template('bloodbank/viewAppointment.html', appointmentVOList=appointmentVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/acceptAppointment', methods=['GET'])
def bloodbankAcceptAppointment():
    try:
        if adminLoginSession() == "bloodbank":
            appointmentVO = AppointmentVO()
            appointmentDAO = AppointmentDAO()

            appointmentId = request.args.get('appointmentId')
            appointmentStatus = 'Accepted'

            print("222222222222222222222:", appointmentId)
            appointmentVO.appointmentId = appointmentId
            appointmentVO.appointmentStatus = appointmentStatus

            appointmentDAO.updateAppointment(appointmentVO)

            return redirect(url_for('bloodbankViewAppointment'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/rejectAppointment', methods=['GET'])
def bloodbankRejectAppointment():
    try:
        if adminLoginSession() == "bloodbank":
            appointmentVO = AppointmentVO()
            appointmentDAO = AppointmentDAO()

            appointmentId = request.args.get('appointmentId')
            appointmentStatus = 'Rejected'

            print("222222222222222222222:", appointmentId)
            appointmentVO.appointmentId = appointmentId
            appointmentVO.appointmentStatus = appointmentStatus

            appointmentDAO.updateAppointment(appointmentVO)

            return redirect(url_for('bloodbankViewAppointment'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# --------------------------ADMIN------------------------------------------------

@app.route('/admin/viewDonationRequest', methods=['GET'])
def adminViewDonationRequest():
    try:
        if adminLoginSession() == "admin":
            appointmentDAO = AppointmentDAO()

            appointmentVOList = appointmentDAO.viewAppointmentByAdmin()
            return render_template('admin/viewAppointment.html', appointmentVOList=appointmentVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxGetGraphData')
def adminAjaxGetGraphData():
    appointmentVO = AppointmentVO()
    appointmentDAO = AppointmentDAO()

    index_BloodbankId = request.args.get('index_BloodbankId')

    appointmentVO.appointment_BloodBankId = index_BloodbankId
    ajaxGraphDataList = appointmentDAO.ajaxGetGraphData(appointmentVO)

    print("ajaxGraphDataList >>>>>>>>>>>>>>>>>> ", ajaxGraphDataList)

    graphDict = {}
    counter = False
    if len(ajaxGraphDataList) != 0:
        counter = True

        dict1 = {}
        for i in ajaxGraphDataList:
            dict1[i[0]] = i[1]

        graphDict.update(dict1)
    print('graphDict>>>', graphDict)
    if counter:
        response = {'responseKey': graphDict}
        print('response>>>>>>>>', response)

    else:
        response = {'responseKey': 'Error'}

    return jsonify(response)
