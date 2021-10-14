import smtplib
import math

from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.EmergencyRequestDAO import EmergencyRequestDAO
from project.com.vo.EmergencyRequestVO import EmergencyRequestVO
from project.com.dao.BloodGroupDAO import BloodGroupDAO
from project.com.dao.BloodBankDAO import BloodBankDAO
from project.com.dao.UserDAO import UserDAO
from project.com.vo.UserVO import UserVO
from project.com.vo.AcceptEmergencyRequestVO import AcceptEmergencyRequestVO
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@app.route('/bloodbank/loadEmergencyRequest', methods=['GET'])
def bloodbankLoadEmergencyRequest():
    try:
        if adminLoginSession() == "bloodbank":

            bloodGroupDAO =BloodGroupDAO()
            bloodGroupVOList = bloodGroupDAO.viewBloodGroup()

            return render_template('bloodbank/addEmergencyRequest.html', bloodGroupVOList=bloodGroupVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/insertEmergencyRequest', methods=['POST', 'GET'])
def bloodbankInsertEmergencyRequest():
    try:
        if adminLoginSession() == "bloodbank":
            print("00000000000000000000000000000000000000000000000000000000000000000")
            emergencyRequestVO = EmergencyRequestVO()
            emergencyRequestDAO = EmergencyRequestDAO()

            userDAO = UserDAO()


            loginId = session["session_loginId"]
            bloodBankDAO = BloodBankDAO()

            bloodBankList = bloodBankDAO.getBloodBank(loginId)
            print(bloodBankList)
            emergencyRequestQuantity = request.form['emergencyRequestQuantity']
            emergencyRequest_BloodGroupId = request.form['emergencyRequest_BloodGroupId']
            print("1111111111111111111111111111111111111111111111")
            emergencyRequest_CityId = bloodBankList[0].bloodBank_CityId
            emergencyRequest_AreaId = bloodBankList[0].bloodBank_AreaId
            emergencyRequest_BloodBankId = bloodBankList[0].bloodBankId
            emergencyRequest_LoginId = bloodBankList[0].bloodBank_LoginId
            print("22222222222222222222222222222222222222222222222")

            bloodGroupDAO = BloodGroupDAO()
            bloodGroupList = bloodGroupDAO.getBloodGroupName(emergencyRequest_BloodGroupId)
            print(bloodGroupList)

            emergencyRequestDate = str(datetime.now().date())
            emergencyRequestTime = datetime.now().strftime("%H:%M:%S")
            emergencyRequestStatus = "Pending"
            print("333333333333333333333333333333333333333333333333333")

            emergencyRequestPersonRequire = int(emergencyRequestQuantity)*525/350
            emergencyRequestPersonRequire = math.ceil(emergencyRequestPersonRequire)
            print(emergencyRequestPersonRequire)

            emergencyRequestVO.emergencyRequest_AreaId = emergencyRequest_AreaId
            emergencyRequestVO.emergencyRequest_BloodBankId = emergencyRequest_BloodBankId
            emergencyRequestVO.emergencyRequest_CityId = emergencyRequest_CityId
            emergencyRequestVO.emergencyRequest_BloodGroupId = emergencyRequest_BloodGroupId
            emergencyRequestVO.emergencyRequest_LoginId = emergencyRequest_LoginId
            emergencyRequestVO.emergencyRequestQuantity = emergencyRequestQuantity
            emergencyRequestVO.emergencyRequestDate = emergencyRequestDate
            emergencyRequestVO.emergencyRequestTime = emergencyRequestTime
            emergencyRequestVO.emergencyRequestStatus = emergencyRequestStatus
            emergencyRequestVO.emergencyRequestPersonRequire = emergencyRequestPersonRequire

            userVOList = userDAO.getUserForEmergencyRequest(emergencyRequest_AreaId,emergencyRequest_BloodGroupId)

            print("############################################################3")
            userId = []
            for i in userVOList:
                userId.append(i[1].loginUsername)
            print(userId)
            #----------------------------------------------------MAIL SEND------------------------------------------------
            sender = "onlinebloodbank2020@gmail.com"

            receiver = userId

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = ",".join(receiver)

            msg['Subject'] = "EMERGENCY BLOOD REQUEST"

            msg.attach(MIMEText('Dear User,\nWe '+str(bloodBankList[0].bloodBankName)+' are in need of '+str(bloodGroupList.bloodGroupName)+".It would be very thankful of you if you come forward and donate."))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "Qwer123@")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)
            #----------------------------------------------------------------------------------------------------

            emergencyRequestDAO.insertEmergencyRequest(emergencyRequestVO)



            return redirect(url_for('bloodbankViewEmergencyRequest'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/viewEmergencyRequest', methods=['GET'])
def bloodbankViewEmergencyRequest():
    try:
        if adminLoginSession() == "bloodbank":
            emergencyRequestDAO = EmergencyRequestDAO()
            print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
            emergencyRequestList = emergencyRequestDAO.viewEmergencyRequest()
            print(emergencyRequestList)
            print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
            acceptEmergencyRequestList = emergencyRequestDAO.viewAcceptEmergencyRequest()
            print(acceptEmergencyRequestList)
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")

            list1=[]
            list2=[]
            for i in emergencyRequestList:
                count = 0
                for j in acceptEmergencyRequestList:
                    if i[0].emergencyRequestId == j.acceptEmergencyRequest_EmergencyRequestId:
                        count+=1
                list1.append(i[0].emergencyRequestId)
                list2.append(count)
            acceptPresonCount = list(zip(list1,list2))
            print(list1)
            print(list2)
            print(acceptPresonCount)


            return render_template('bloodbank/viewEmergencyRequest.html', emergencyRequestList=emergencyRequestList, acceptPresonCount=acceptPresonCount)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/bloodbank/completeEmergencyRequest', methods=['GET'])
def bloodbankCompleteEmergencyRequest():
    try:
        if adminLoginSession() == "bloodbank":
            userDAO = UserDAO()

            emergencyRequestDAO = EmergencyRequestDAO()
            emergencyRequestVO = EmergencyRequestVO()

            emergencyRequestId = request.args.get('emergencyRequestId')
            emergencyRequest_BloodGroupId = request.args.get('emergencyRequest_BloodGroupId')
            emergencyRequest_AreaId = request.args.get('emergencyRequest_AreaId')
            emergencyRequestStatus = "Complete"

            emergencyRequestVO.emergencyRequestId = emergencyRequestId
            emergencyRequestVO.emergencyRequestStatus = emergencyRequestStatus
#_______________________________________________MAIL___________________________________________________________________
            userVOList = userDAO.getUserForEmergencyRequest(emergencyRequest_AreaId, emergencyRequest_BloodGroupId)

            userId = []
            for i in userVOList:
                userId.append(i[1].loginUsername)
            print(userId)

            sender = "onlinebloodbank2020@gmail.com"

            receiver = userId

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = ",".join(receiver)

            msg['Subject'] = "EMERGENCY BLOOD REQUEST FULFILL"

            msg.attach(MIMEText('Dear User,\nAs of now,the requirement of the needed blood is fulfilled.We will keep you updated whenever the need arises.\n\nThank you'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "Qwer123@")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)
#_______________________________________________________________________________________________________________________
            emergencyRequestDAO.completeEmergencyRequest(emergencyRequestVO)

            return redirect(url_for('bloodbankViewEmergencyRequest'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/viewEmergencyRequest', methods=['GET'])
def userViewEmergencyRequest():
    try:
        if adminLoginSession() == "user":
            print("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
            emergencyRequestDAO = EmergencyRequestDAO()

            loginId = session["session_loginId"]
            loginUsername = session['session_loginUsername']

            userVO = UserVO()
            userDAO = UserDAO()

            userList = userDAO.getUserAllData(loginId)
            user_BloodGroupId = userList[0].user_BloodGroupId
            user_AreaId = userList[0].user_AreaId
            print("area:",user_AreaId)
            print("blood group:",user_BloodGroupId)

            status = "Pending"

            emergencyRequestList = emergencyRequestDAO.viewUserEmergencyRequest(user_BloodGroupId, user_AreaId, status)


#_____________________________________________________________________________________________________________________
            emergencyRequestAllList = emergencyRequestDAO.viewEmergencyRequest()
            acceptEmergencyRequestList = emergencyRequestDAO.viewAcceptEmergencyRequest()
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            list1 = []
            list2 = []
            for i in emergencyRequestAllList:
                count = 0
                for j in acceptEmergencyRequestList:
                    if i[0].emergencyRequestId == j.acceptEmergencyRequest_EmergencyRequestId and loginId == j.acceptEmergencyRequest_LoginId:
                        count += 1
                        print("Veer")
                list1.append(i[0].emergencyRequestId)
                list2.append(count)
            acceptCount = list(zip(list1, list2))
            print(list1)
            print(list2)
            print(acceptCount)

            print(emergencyRequestList)
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            return render_template('user/viewEmergencyRequest.html', emergencyRequestList=emergencyRequestList, acceptCount=acceptCount)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/acceptEmergencyRequest', methods=['GET'])
def userAcceptEmergencyRequest():
    try:
        if adminLoginSession() == "user":
            userDAO = UserDAO()

            acceptEmergencyRequestVO = AcceptEmergencyRequestVO()
            emergencyRequestDAO = EmergencyRequestDAO()
            emergencyRequestVO = EmergencyRequestVO()

            acceptEmergencyRequest_EmergencyRequestId = request.args.get('emergencyRequestId')
            print(acceptEmergencyRequest_EmergencyRequestId)

            acceptEmergencyRequest_LoginId = session["session_loginId"]

            userAllList = userDAO.getUserAllData(acceptEmergencyRequest_LoginId)
            acceptEmergencyRequest_UserId = userAllList[0].userId

            acceptEmergencyRequestDate = str(datetime.now().date())
            acceptEmergencyRequestTime = datetime.now().strftime("%H:%M:%S")

            acceptEmergencyRequestStatus = "Accepted"

            acceptEmergencyRequestVO.acceptEmergencyRequest_EmergencyRequestId = acceptEmergencyRequest_EmergencyRequestId
            acceptEmergencyRequestVO.acceptEmergencyRequest_LoginId = acceptEmergencyRequest_LoginId
            acceptEmergencyRequestVO.acceptEmergencyRequest_UserId = acceptEmergencyRequest_UserId
            acceptEmergencyRequestVO.acceptEmergencyRequestDate = acceptEmergencyRequestDate
            acceptEmergencyRequestVO.acceptEmergencyRequestTime = acceptEmergencyRequestTime
            acceptEmergencyRequestVO.acceptEmergencyRequestStatus =acceptEmergencyRequestStatus

            emergencyRequestDAO.insertAcceptEmergencyRequest(acceptEmergencyRequestVO)

            acceptEmergencyRequestPersonList = emergencyRequestDAO.findPersonCount(acceptEmergencyRequest_EmergencyRequestId)

            acceptEmergencyRequestPersonDictList = [i.as_dict() for i in acceptEmergencyRequestPersonList]

            print(acceptEmergencyRequestPersonDictList)

            lenAcceptEmergencyRequestPersonDictList = len(acceptEmergencyRequestPersonDictList)
            print("############################################################33333333333333333")
            print(lenAcceptEmergencyRequestPersonDictList)

            emergencyRequestPersonList = emergencyRequestDAO.findPersonCountFromEmergencyRequest(acceptEmergencyRequest_EmergencyRequestId)
            print(emergencyRequestPersonList)
            if emergencyRequestPersonList[0][0].emergencyRequestPersonRequire == lenAcceptEmergencyRequestPersonDictList:
                emergencyRequestVO.emergencyRequestId = acceptEmergencyRequest_EmergencyRequestId
                emergencyRequestVO.emergencyRequestStatus = "Complete"
                emergencyRequestDAO.completeEmergencyRequest(emergencyRequestVO)
#___________________________________________________MAIL________________________________________________________________
                emergencyRequest_BloodGroupId = request.args.get('emergencyRequest_BloodGroupId')
                emergencyRequest_AreaId = request.args.get('emergencyRequest_AreaId')
                userVOList = userDAO.getUserForEmergencyRequest(emergencyRequest_AreaId, emergencyRequest_BloodGroupId)

                print("############################################################3")
                userId = []
                for i in userVOList:
                    userId.append(i[1].loginUsername)
                print(userId)

                sender = "onlinebloodbank2020@gmail.com"

                receiver = userId

                msg = MIMEMultipart()

                msg['From'] = sender

                msg['To'] = ",".join(receiver)

                msg['Subject'] = "EMERGENCY BLOOD REQUEST FULFILL"

                msg.attach(MIMEText('Dear User,\nAs of now,the requirement of the needed blood is fulfilled.We will keep you updated whenever the need arises.\n\nThank you'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "Qwer123@")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)
#_______________________________________________________________________________________________________________________
            return redirect(url_for('userViewEmergencyRequest'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
