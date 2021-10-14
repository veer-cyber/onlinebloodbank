import glob
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib.request

import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# import urllib.request

import cv2
import face_recognition
import numpy as np
from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.dao.AppointmentDAO import AppointmentDAO
from project.com.dao.BloodBankDAO import BloodBankDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.AppointmentVO import AppointmentVO
from project.com.vo.LoginVO import LoginVO

UPLOAD_FOLDER = 'project/static/adminResources/face/'


@app.route('/', methods=['GET'])
def adminLoadLogin():
    try:
        session.clear()
        return render_template('user/login.html')
    except Exception as ex:
        print(ex)


@app.route("/admin/file", methods=['POST', 'GET'])
def adminFile():
    try:

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        print("JOKERJOKERJOKERJOKERJOKERJOKERJOKERJOKERJOKERJOKERJOKERJOKER")
        fileUrl = request.form['file']
        print(fileUrl)
        print("############################################################")
        loginUsername = request.form['loginUsername']
        print(loginUsername)
        nameOfFile = loginUsername+".jpg"
        nameOfFileForDatabase = loginUsername
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        print("))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))")
        loginList = loginDAO.findUser(loginUsername)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        loginId = loginList[0].loginId

        loginVO.loginId = loginId
        loginVO.loginFileName = nameOfFileForDatabase
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        loginDAO.addNameForFr(loginVO)
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        urllib.request.urlretrieve(fileUrl, "project/static/adminResources/face/"+nameOfFile)
        print("DONE")

        return redirect(url_for('adminLoadLogin'))
    except Exception as ex:
        print(ex)


@app.route("/admin/validateLogin", methods=['POST', 'GET'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        # loginVO.loginStatus = "active"

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = 'Username Or Password is Incorrect !'

            return render_template('user/login.html', error=msg)

        elif loginDictList[0]['loginStatus'] == "inactive":

            msg = "you are temporarily blocked by admin"

            return render_template('user/login.html', error=msg)

        else:

            for row1 in loginDictList:

                loginId = row1['loginId']

                loginUsername = row1['loginUsername']

                loginRole = row1['loginRole']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername

                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))

                elif loginRole == 'bloodbank':
                    return redirect(url_for('bloodbankLoadDashboard'))

                elif loginRole == 'user':
                    return redirect(url_for('userLoadDashboard'))

    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard', methods=['GET'])
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            bloodBankDAO = BloodBankDAO()
            bloodBankVOList = bloodBankDAO.viewAdminBloodBank()
            return render_template('admin/index.html', bloodBankVOList=bloodBankVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/loadDashboard', methods=['GET'])
def bloodbankLoadDashboard():
    try:
        if adminLoginSession() == 'bloodbank':
            bloodbankDAO = BloodBankDAO()
            loginId = session['session_loginId']
            bloodBankVOList = bloodbankDAO.getBloodBank(loginId)

            appointmentVO = AppointmentVO()
            appointmentDAO = AppointmentDAO()
            appointmentVO.appointment_BloodBankId = bloodBankVOList[0].bloodBankId
            appointmentVOList = appointmentDAO.getAppointmentDetailsByBloodBankId(appointmentVO)

            return render_template('bloodbank/index.html', appointmentVOList=appointmentVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/loadDashboard', methods=['GET'])
def userLoadDashboard():
    try:
        if adminLoginSession() == 'user':
            appointmentVO = AppointmentVO()
            appointmentDAO = AppointmentDAO()
            loginId = session['session_loginId']

            appointmentVO.appointment_LoginId = loginId

            appointmentVOList = appointmentDAO.getAppointmentDetailsByLoginId(appointmentVO)
            print('appointmentVOList>>>>>', appointmentVOList)

            return render_template('user/index.html', appointmentVOList=appointmentVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:

            if session['session_loginRole'] == 'admin':

                return 'admin'

            elif session['session_loginRole'] == 'bloodbank':

                return 'bloodbank'

            elif session['session_loginRole'] == 'user':

                return 'user'

            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")

        else:

            print("<<<<<<<<<<<<<<<<False>>>>>>>>>>>>>>>>>>>>")

            return False
    except Exception as ex:
        print(ex)


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    try:
        session.clear()
        return redirect('/')
    except Exception as ex:
        print(ex)


# __________________________________________________forgot password____________________________________________________

@app.route('/admin/forgotPassword', methods=['GET'])
def adminLoadForgotPassword():
    try:
        return render_template('user/forgotPassword.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/sendOTP', methods=['POST'])
def adminSendOTP():
    try:
        loginDAO = LoginDAO()
        loginVO = LoginVO()

        loginUsername = request.form["loginUsername"]
        loginVOList = loginDAO.findUser(loginUsername)
        print(loginVOList)
        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)
        lenLoginDictList = len(loginDictList)
        if lenLoginDictList == 0:
            msg = "Username not found"

            return render_template('user/forgotPassword.html', error=msg)
        else:

            otp = ''.join((random.choice(string.digits)) for x in range(4))
            print(otp)

            sender = "onlinebloodbank2020@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "OTP"

            msg.attach(MIMEText('Your OTP is:' + otp, 'plain'))

            session['session_OTP'] = otp
            session['session_loginUsername'] = loginUsername
            session['session_loginId'] = loginDictList[0]['loginId']

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "Qwer123@")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            return render_template('user/otp.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/sendPassword', methods=['POST'])
def adminSendForgotPassword():
    try:
        loginDAO = LoginDAO()
        loginVO = LoginVO()

        OTP = request.form["otp"]

        if session['session_OTP'] != OTP:
            msg = "OTP IS NOT MATCHED"

            return render_template('user/otp.html', error=msg)
        else:
            loginId = session['session_loginId']

            password = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            print(password)

            sender = "onlinebloodbank2020@gmail.com"

            receiver = session['session_loginUsername']

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "YOUR PASSWORD"

            msg.attach(MIMEText('Your Password is:' + password, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "Qwer123@")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            loginVO.loginId = loginId
            loginVO.loginPassword = password

            loginDAO.forgotPassword(loginVO)

            return render_template('user/login.html')
    except Exception as ex:
        print(ex)


# ---------------------------------------------------------------RESET PASSWORD------------------------------------


@app.route('/admin/resetBloodBankPassword', methods=['GET'])
def adminResetBloodBankPassword():
    try:
        return render_template('bloodbank/resetPassword.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/resetUserPassword', methods=['GET'])
def adminLoadResetUserPassword():
    try:
        return render_template('user/resetPassword.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/changePassword', methods=['POST'])
def adminResetPassword():
    try:
        loginDAO = LoginDAO()
        loginVO = LoginVO()

        oldPassword = request.form["oldPassword"]
        newPassword = request.form["newPassword"]
        conformPassword = request.form["conformPassword"]

        loginUsername = session['session_loginUsername']

        loginVOList = loginDAO.findUser(loginUsername)
        print(loginVOList)
        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)

        if loginDictList[0]['loginPassword'] != oldPassword:
            msg = "PASSWORD IS NOT MATCHED"

            return render_template('bloodbank/resetPassword.html', error=msg)
        else:
            if newPassword == conformPassword:
                loginId = session['session_loginId']

                loginVO.loginId = loginId
                loginVO.loginPassword = newPassword

                loginDAO.forgotPassword(loginVO)

                if adminLoginSession() == 'bloodbank':

                    return render_template('bloodbank/index.html')

                elif adminLoginSession() == 'user':

                    return render_template('user/index.html')
            else:
                msg = "NEWPASSWORD AND CONFORMPASSWORD IS NOT MATCHED"

                return render_template('bloodbank/resetPassword.html', error=msg)
    except Exception as ex:
        print(ex)


# _______________________________________________________FR_____________________________________________________________

@app.route("/admin/faceValidateLogin", methods=['POST', 'GET'])
def adminFaceValidateLogin():
    try:
        loginVO = LoginVO()
        loginDAO = LoginDAO()

        # ____________________________________________FR_START___________________________________________________

        video_capture = cv2.VideoCapture(0)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        for filename in glob.glob(r"project\static\adminResources\face\*.jpg"):
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
            appointment = face_recognition.load_image_file(filename)
            print("########################################################")
            face_encoding = face_recognition.face_encodings(appointment)[0]

            known_face_encodings = []
            known_face_names = []
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            known_face_encodings.append(face_encoding)

            firstname = filename.replace(".jpg", "")
            firstname = firstname.replace(r"project\static\adminResources\face", "")
            firstname = firstname[1:]

            print("1:" + firstname)
            known_face_names.append(firstname)

            face_locations = []
            face_encodings = []
            face_names = []
            process_this_frame = True

            while True:
                name = "Unknown"
                ret, frame = video_capture.read()

                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                rgb_small_frame = small_frame[:, :, ::-1]

                if process_this_frame:
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    face_names = []
                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        name = "Unknown"

                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]

                        face_names.append(name)

                process_this_frame = not process_this_frame

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                cv2.imshow('Video', frame)

                if cv2.waitKey(1) and name == "Unknown":
                    break
                elif cv2.waitKey(1) and 0xFF == ord('q'):
                    break
                elif name != "Unknown":
                    break

            if name != "Unknown" or 0xFF == ord('q'):
                break
        print("NAME:" + name)
        video_capture.release()
        cv2.destroyAllWindows()

        # ____________________________________________FR_CLOSE___________________________________________________

        loginVOList = loginDAO.faceValidateLogin(name)

        # loginVO.loginUsername = loginVOList.loginUsername
        # loginVO.loginPassword = loginVOList.loginPassword
        # # loginVO.loginStatus = "active"
        #
        # loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = 'Face is Not matched'

            return render_template('user/login.html', error=msg)

        elif loginDictList[0]['loginStatus'] == "inactive":

            msg = "you are temporarily blocked by admin"

            return render_template('user/login.html', error=msg)

        else:

            for row1 in loginDictList:

                loginId = row1['loginId']

                loginUsername = row1['loginUsername']

                loginRole = row1['loginRole']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername

                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))

                elif loginRole == 'bloodbank':
                    return redirect(url_for('bloodbankLoadDashboard'))

                elif loginRole == 'user':
                    return redirect(url_for('userLoadDashboard'))

    except Exception as ex:
        print(ex)
