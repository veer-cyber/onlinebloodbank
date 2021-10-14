import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, url_for, redirect, jsonify, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.BloodBankDAO import BloodBankDAO
from project.com.dao.CityDAO import CityDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BloodBankVO import BloodBankVO
from project.com.vo.LoginVO import LoginVO


@app.route('/bloodbank/loadBloodBank', methods=['GET'])
def bloodbankLoadBloodBank():
    try:
        cityDAO = CityDAO()
        cityVOList = cityDAO.viewCity()
        print(cityVOList)

        areaDAO = AreaDAO()
        areaVOList = areaDAO.viewArea()

        return render_template('bloodbank/register.html', areaVOList=areaVOList, cityVOList=cityVOList)
    except Exception as ex:
        print(ex)


@app.route('/bloodBank/ajaxAreaBloodBank')
def bloodbankAjaxAreaBloodBank():
    try:
        areaVO = AreaVO()

        areaDAO = AreaDAO()

        area_CityId = request.args.get('bloodbank_CityId')
        print('area_CityId::', area_CityId)

        areaVO.area_CityId = area_CityId

        ajaxBloodBankAreaList = areaDAO.ajaxArea(areaVO)

        ajaxBloodBankAreaJson = [i.as_dict() for i in ajaxBloodBankAreaList]

        return jsonify(ajaxBloodBankAreaJson)

    except Exception as ex:
        print(ex)


@app.route('/bloodbank/insertBloodBank', methods=['POST'])
def bloodbankInsertBloodBank():
    try:
        loginVO = LoginVO()
        loginDAO = LoginDAO()

        bloodBankVO = BloodBankVO()
        bloodBankDAO = BloodBankDAO()

        loginUsername = request.form['loginUsername']
        bloodBankName = request.form['bloodBankName']
        bloodBank_CityId = request.form['bloodBank_CityId']
        bloodBank_AreaId = request.form['bloodBank_AreaId']
        bloodBankAddress = request.form['bloodBankAddress']
        bloodBankContact = request.form['bloodBankContact']
        bloodBankLicense = request.form['bloodBankLicense']
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("loginPassword=" + loginPassword)

        sender = "onlinebloodbank2020@gmail.com"

        receiver = loginUsername

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "LOGIN PASSWORD"

        msg.attach(MIMEText('Your Password is:' + loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "Qwer123@")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = "bloodbank"
        loginVO.loginStatus = "active"
        loginVO.loginFileName = "None"
        print("###############################################")
        loginDAO.insertLogin(loginVO)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        bloodBankVO.bloodBankName = bloodBankName
        bloodBankVO.bloodBank_CityId = bloodBank_CityId
        bloodBankVO.bloodBank_AreaId = bloodBank_AreaId
        bloodBankVO.bloodBankAddress = bloodBankAddress
        bloodBankVO.bloodBankContact = bloodBankContact
        bloodBankVO.bloodBankLicense = bloodBankLicense
        bloodBankVO.bloodBank_LoginId = loginVO.loginId
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        bloodBankDAO.insertBloodBank(bloodBankVO)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        server.quit()

        return render_template("admin/takePicture.html", loginUsername=loginUsername)
    except Exception as ex:
        print(ex)


@app.route('/admin/viewBloodbank', methods=['GET'])
def adminViewBloodbank():
    try:
        if adminLoginSession() == "admin":
            bloodBankDAO = BloodBankDAO()

            bloodBankVOList = bloodBankDAO.viewAdminBloodBank()

            return render_template('admin/viewBloodbank.html', bloodBankVOList=bloodBankVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/manageBloodbank', methods=['GET'])
def adminManageBloodbank():
    try:
        if adminLoginSession() == "admin":

            loginVO = LoginVO()
            bloodBankDAO = BloodBankDAO()

            loginId = request.args.get('loginId')

            bloodBankList = bloodBankDAO.getBloodbankData(loginId)

            bloodBankDictList = [i.as_dict() for i in bloodBankList]

            if bloodBankDictList[0]['loginStatus'] == "inactive":

                loginStatus = "active"

                loginVO.loginId = loginId
                loginVO.loginStatus = loginStatus

                bloodBankDAO.manageBloodbank(loginVO)

            elif bloodBankDictList[0]['loginStatus'] == "active":

                loginStatus = "inactive"

                loginVO.loginId = loginId
                loginVO.loginStatus = loginStatus

                bloodBankDAO.manageBloodbank(loginVO)
            return redirect(url_for('adminViewBloodbank'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

#______________________________________________EDIT PROFILE______________________________________________________
@app.route('/bloodbank/editProfile', methods=['GET'])
def bloodBankEditProfile():
    try:
        if adminLoginSession() == "bloodbank":
            cityDAO = CityDAO()
            cityVOList = cityDAO.viewCity()
            print(cityVOList)

            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            loginId = session['session_loginId']

            bloodBankDAO = BloodBankDAO()

            bloodBankVOList=bloodBankDAO.getBloodbankData(loginId)
            bloodBankVOAllList=bloodBankDAO.getBloodBank(loginId)

            return render_template('bloodbank/editProfile.html', areaVOList=areaVOList, cityVOList=cityVOList, bloodBankVOList=bloodBankVOList, bloodBankVOAllList=bloodBankVOAllList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/bloodbank/updateBloodBankProfile', methods=['POST'])
def updateBloodBankProfile():
    try:
        if adminLoginSession() == "bloodbank":

            bloodBankDAO = BloodBankDAO()
            bloodBankVO = BloodBankVO()

            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            bloodBankName = request.form['bloodBankName']
            bloodBank_CityId = request.form['bloodBank_CityId']
            bloodBank_AreaId = request.form['bloodBank_AreaId']
            bloodBankAddress = request.form['bloodBankAddress']
            bloodBankContact = request.form['bloodBankContact']
            bloodBankLicense = request.form['bloodBankLicense']
            bloodBankId = request.form['bloodBankId']
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            bloodBankVO.bloodBankName = bloodBankName
            bloodBankVO.bloodBank_CityId = bloodBank_CityId
            bloodBankVO.bloodBank_AreaId = bloodBank_AreaId
            bloodBankVO.bloodBankAddress = bloodBankAddress
            bloodBankVO.bloodBankContact = bloodBankContact
            bloodBankVO.bloodBankLicense = bloodBankLicense
            bloodBankVO.bloodBankId = bloodBankId

            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(bloodBankId)
            bloodBankDAO.editProfile(bloodBankVO)
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            return render_template("bloodbank/index.html")
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)