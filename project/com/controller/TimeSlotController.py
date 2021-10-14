from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.TimeSlotDAO import TimeSlotDAO
from project.com.vo.TimeSlotVO import TimeSlotVO


@app.route('/bloodbank/loadTimeSlot', methods=['GET'])
def bloodbankLoadTimeSlot():
    try:
        if adminLoginSession() == "bloodbank":

            return render_template('bloodbank/addTimeSlot.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/insertTimeSlot', methods=['POST', 'GET'])
def bloodbankInsertTimeSlot():
    try:
        if adminLoginSession() == "bloodbank":
            timeSlotName = request.form['timeSlotName']
            timeSlot = request.form['timeSlot']

            timeSlotVO = TimeSlotVO()
            timeSlotDAO = TimeSlotDAO()

            loginId = session['session_loginId']

            bloodBankVOList = timeSlotDAO.searchBloodBank(loginId)

            bloodbankDictList = [i.as_dict() for i in bloodBankVOList]

            timeSlot_BloodBankId = bloodbankDictList[0]["bloodBankId"]

            print(timeSlot_BloodBankId)

            timeSlotVO.timeSlotName = timeSlotName
            timeSlotVO.timeSlot = timeSlot
            timeSlotVO.timeSlot_BloodBankId = timeSlot_BloodBankId

            timeSlotDAO.insertTimeSlot(timeSlotVO)

            return redirect(url_for('bloodBankViewTimeSlot'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/viewTimeSlot', methods=['GET'])
def bloodBankViewTimeSlot():
    try:
        if adminLoginSession() == "bloodbank":
            timeSlotDAO = TimeSlotDAO()

            loginId = session['session_loginId']

            bloodBankVOList = timeSlotDAO.searchBloodBank(loginId)

            bloodbankDictList = [i.as_dict() for i in bloodBankVOList]

            timeSlot_BloodBankId = bloodbankDictList[0]["bloodBankId"]

            print(timeSlot_BloodBankId)
            timeSlotVOList = timeSlotDAO.viewBloodBankTimeSlot(timeSlot_BloodBankId)



            return render_template('bloodbank/viewTimeSlot.html', timeSlotVOList=timeSlotVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/deleteTimeSlot', methods=['GET'])
def bloodbankDeleteTimeSlot():
    try:
        if adminLoginSession() == "bloodbank":
            timeSlotDAO = TimeSlotDAO()

            timeSlotId = request.args.get('timeSlotId')

            timeSlotDAO.deleteTimeSlot(timeSlotId)

            return redirect(url_for('bloodBankViewTimeSlot'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
