import random
import smtplib
import string
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.BloodGroupDAO import BloodGroupDAO
from project.com.dao.CityDAO import CityDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.UserDAO import UserDAO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.UserVO import UserVO

UPLOAD_FOLDER = 'project/static/adminResources/userBloodReport/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/user/loadUser', methods=['GET'])
def userLoadUser():
    try:
        areaDAO = AreaDAO()
        areaVOList = areaDAO.viewArea()
        print(areaVOList)

        cityDAO = CityDAO()
        cityVOList = cityDAO.viewCity()
        print(cityVOList)

        bloodGroupDAO = BloodGroupDAO()
        bloodGroupVOList = bloodGroupDAO.viewBloodGroup()
        print(bloodGroupVOList)

        return render_template('user/register.html', areaVOList=areaVOList, cityVOList=cityVOList,
                               bloodGroupVOList=bloodGroupVOList)
    except Exception as ex:
        print(ex)


@app.route('/user/ajaxAreaUser')
def userAjaxAreaUser():
    try:
        areaVO = AreaVO()

        areaDAO = AreaDAO()

        area_CityId = request.args.get('user_CityId')
        print('area_CityId::', area_CityId)

        areaVO.area_CityId = area_CityId

        ajaxUserAreaList = areaDAO.ajaxArea(areaVO)
        print('ajaxUserAreaList::', ajaxUserAreaList)

        ajaxUserAreaJson = [i.as_dict() for i in ajaxUserAreaList]
        print('ajaxUserAreaJson::', ajaxUserAreaJson)

        return jsonify(ajaxUserAreaJson)

    except Exception as ex:
        print(ex)


@app.route('/user/insertUser', methods=['POST'])
def userInsertUser():
    try:
        loginVO = LoginVO()
        loginDAO = LoginDAO()

        userVO = UserVO()
        userDAO = UserDAO()
        loginUsername = request.form['loginUsername']

        userFirstName = request.form['userFirstName']

        userLastName = request.form['userLastName']

        userBirthDate = request.form['userBirthDate']

        user_BloodGroupId = request.form['user_BloodGroupId']

        userGender = request.form['userGender']

        userWeight = request.form['userWeight']

        userHeight = request.form['userHeight']

        user_CityId = request.form['user_CityId']

        userDiseases = request.form['userDiseases']

        user_AreaId = request.form['user_AreaId']

        userAddress = request.form['userAddress']

        userContact = request.form['userContact']

        userFile = request.files['userFile']
        print(userFile)

        userFileName = secure_filename(userFile.filename)
        print(userFileName)

        userFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
        print(userFilePath)

        userFile.save(os.path.join(userFilePath, userFileName))

        userVO.userFileName = userFileName

        userVO.userFilePath = userFilePath.replace("project", "..")


        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

        print("loginPassword=" + loginPassword)

        #sender = "pythondemodonotreply@gmail.com"
        sender = "onlinebloodbank2020@gmail.com"

        receiver = loginUsername

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "LOGIN PASSWORD"

        msg.attach(MIMEText('Your Password is:' + loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        #server.login(sender, "qazwsxedcrfvtgb1234567890")
        server.login(sender, "Qwer123@")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = "user"
        loginVO.loginStatus = "active"
        loginVO.loginFileName = "None"

        loginDAO.insertLogin(loginVO)

        userVO.user_CityId = user_CityId
        userVO.user_BloodGroupId = user_BloodGroupId
        userVO.userFirstName = userFirstName
        userVO.userLastName = userLastName
        userVO.userBirthDate = userBirthDate
        userVO.userGender = userGender
        userVO.userWeight = userWeight
        userVO.userHeight = userHeight
        userVO.userDiseases = userDiseases
        userVO.user_AreaId = user_AreaId
        userVO.userAddress = userAddress
        userVO.userContact = userContact
        userVO.user_LoginId = loginVO.loginId
        userDAO.insertUser(userVO)

        server.quit()

        return render_template("admin/takePicture.html",loginUsername=loginUsername)
    except Exception as ex:
        print(ex)


@app.route('/admin/viewUser', methods=['GET'])
def adminViewUser():
    try:
        if adminLoginSession() == "admin":
            userDAO = UserDAO()

            userVOList = userDAO.viewAdminUser()

            return render_template('admin/viewUser.html', userVOList=userVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/manageUser', methods=['GET'])
def adminManageUser():
    try:
        if adminLoginSession() == "admin":

            loginVO = LoginVO()
            userDAO = UserDAO()

            loginId = request.args.get('loginId')
            userList = userDAO.getUserData(loginId)

            userDictList = [i.as_dict() for i in userList]

            if userDictList[0]['loginStatus'] == "inactive":

                loginStatus = "active"

                loginVO.loginId = loginId
                loginVO.loginStatus = loginStatus

                userDAO.manageUser(loginVO)

            elif userDictList[0]['loginStatus'] == "active":

                loginStatus = "inactive"

                loginVO.loginId = loginId
                loginVO.loginStatus = loginStatus

                userDAO.manageUser(loginVO)
            return redirect(url_for('adminViewUser'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


#--------------------------------------------------EDIT PROFILE-------------------------------------------------
@app.route('/user/editProfile', methods=['GET'])
def userEditProfile():
    try:
        if adminLoginSession() == "user":
            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()
            print(areaVOList)

            cityDAO = CityDAO()
            cityVOList = cityDAO.viewCity()
            print(cityVOList)

            bloodGroupDAO = BloodGroupDAO()
            bloodGroupVOList = bloodGroupDAO.viewBloodGroup()
            print(bloodGroupVOList)

            userDAO = UserDAO()
            loginId = session['session_loginId']

            userVOList = userDAO.getUserData(loginId)
            userVOAllList = userDAO.getUserAllData(loginId)
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(userVOList)

            return render_template('user/editProfile.html', userVOList=userVOList, userVOAllList=userVOAllList, areaVOList=areaVOList, cityVOList=cityVOList, bloodGroupVOList=bloodGroupVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/user/updateUserProfile', methods=['POST'])
def updateUserProfile():
    try:
        if adminLoginSession() == "user":

            userVO = UserVO()
            userDAO = UserDAO()
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            userFirstName = request.form['userFirstName']

            userLastName = request.form['userLastName']

            userBirthDate = request.form['userBirthDate']

            user_BloodGroupId = request.form['user_BloodGroupId']

            userGender = request.form['userGender']

            userWeight = request.form['userWeight']

            userHeight = request.form['userHeight']

            user_CityId = request.form['user_CityId']

            userDiseases = request.form['userDiseases']

            user_AreaId = request.form['user_AreaId']

            userAddress = request.form['userAddress']

            userContact = request.form['userContact']

            userId = request.form['userId']
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            userVO.user_CityId = user_CityId
            userVO.user_BloodGroupId = user_BloodGroupId
            userVO.userFirstName = userFirstName
            userVO.userLastName = userLastName
            userVO.userBirthDate = userBirthDate
            userVO.userGender = userGender
            userVO.userWeight = userWeight
            userVO.userHeight = userHeight
            userVO.userDiseases = userDiseases
            userVO.user_AreaId = user_AreaId
            userVO.userAddress = userAddress
            userVO.userContact = userContact
            userVO.userId = userId
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(userId)
            userDAO.editProfile(userVO)
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            return render_template("user/index.html")
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)