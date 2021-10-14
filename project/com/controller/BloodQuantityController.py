from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.BloodGroupDAO import BloodGroupDAO
from project.com.dao.BloodQuantityDAO import BloodQuantityDAO
from project.com.vo.BloodQuantityVO import BloodQuantityVO
from project.com.dao.BloodBankDAO import BloodBankDAO
from datetime import datetime

@app.route('/bloodbank/loadBloodQuantity', methods=['GET'])
def bloodbankLoadBloodQuantity():
    try:
        if adminLoginSession() == "bloodbank":
            bloodGroupDAO = BloodGroupDAO()
            bloodGroupVOList = bloodGroupDAO.viewBloodGroup()

            return render_template('bloodbank/addBloodQuantity.html', bloodGroupVOList=bloodGroupVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/insertBloodQuantity', methods=['POST', 'GET'])
def bloodbankInsertBloodQuantity():
    try:
        if adminLoginSession() == "bloodbank":
            bloodQuantity = request.form['bloodQuantity']

            bloodQuantity_BloodGroupId = request.form['bloodQuantity_BloodGroupId']
            bloodQuantityMonth = request.form['bloodQuantityMonth']
            bloodQuantityYear = request.form['bloodQuantityYear']
            bloodQuantityRequirement = request.form['bloodQuantityRequirement']

            bloodBankDAO = BloodBankDAO()
            loginId = session['session_loginId']
            bloodBankList = bloodBankDAO.getBloodBank(loginId)
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(bloodBankList)
            now = datetime.now()
            bloodQuantityDate = now.strftime("%d/%m/%Y")

            bloodQuantityVO = BloodQuantityVO()
            bloodQuantityDAO = BloodQuantityDAO()
            bloodQuantityStatus = "Pending"

            bloodQuantityVO.bloodQuantity = bloodQuantity

            bloodQuantityVO.bloodQuantity_BloodGroupId = bloodQuantity_BloodGroupId
            bloodQuantityVO.bloodQuantityMonth = bloodQuantityMonth
            bloodQuantityVO.bloodQuantityYear = bloodQuantityYear
            bloodQuantityVO.bloodQuantityDate = bloodQuantityDate
            bloodQuantityVO.bloodQuantity_AreaId = bloodBankList[0].bloodBank_AreaId
            bloodQuantityVO.bloodQuantity_CityId = bloodBankList[0].bloodBank_CityId
            bloodQuantityVO.bloodQuantity_BloodBankId = bloodBankList[0].bloodBankId
            bloodQuantityVO.bloodQuantityStatus = bloodQuantityStatus
            bloodQuantityVO.bloodQuantityRequirement = bloodQuantityRequirement

            bloodQuantityDAO.insertBloodQuantity(bloodQuantityVO)

            return redirect(url_for('bloodbankViewBloodQuantity'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/viewBloodQuantity', methods=['GET'])
def bloodbankViewBloodQuantity():
    try:
        if adminLoginSession() == "bloodbank":
            bloodQuantityDAO = BloodQuantityDAO()
            bloodQuantityVOList = bloodQuantityDAO.viewBloodQuantity()

            return render_template('bloodbank/viewBloodQuantity.html', bloodQuantityVOList=bloodQuantityVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/deleteBloodQuantity', methods=['GET'])
def bloodbankDeleteBloodQuantity():
    try:
        if adminLoginSession() == "bloodbank":

            bloodQuantityDAO = BloodQuantityDAO()

            bloodQuantityId = request.args.get('bloodQuantityId')

            bloodQuantityDAO.deleteBloodQuantity(bloodQuantityId)

            return redirect(url_for('bloodbankViewBloodQuantity'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/statusBloodQuantity', methods=['GET'])
def bloodbankStatusBloodQuantity():
    try:
        if adminLoginSession() == "bloodbank":

            bloodQuantityDAO = BloodQuantityDAO()
            bloodQuantityVO = BloodQuantityVO()

            bloodQuantityId = request.args.get('bloodQuantityId')
            bloodQuantityStatus = "Complete"

            bloodQuantityVO.bloodQuantityStatus = bloodQuantityStatus
            bloodQuantityVO.bloodQuantityId = bloodQuantityId
            bloodQuantityDAO.updateBloodQuantity(bloodQuantityVO)

            return redirect(url_for('bloodbankViewBloodQuantity'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/editBloodQuantity', methods=['GET'])
def bloodbankEditBloodQuantity():
    try:
        if adminLoginSession() == "bloodbank":
            bloodQuantityVO = BloodQuantityVO()

            bloodQuantityDAO = BloodQuantityDAO()

            bloodGroupDAO = BloodGroupDAO()

            bloodQuantityId = request.args.get('bloodQuantityId')

            bloodQuantityVO.bloodQuantityId = bloodQuantityId

            bloodQuantityVOList = bloodQuantityDAO.editBloodQuantity(bloodQuantityVO)

            bloodGroupVOList = bloodGroupDAO.viewBloodGroup()

            return render_template('bloodbank/editBloodQuantity.html', bloodGroupVOList=bloodGroupVOList,
                                   bloodQuantityVOList=bloodQuantityVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/updateBloodQuantity', methods=['POST', 'GET'])
def bloodbankUpdateBloodQuantity():
    try:
        if adminLoginSession() == "bloodbank":
            bloodQuantity = request.form['bloodQuantity']
            bloodQuantity_BloodGroupId = request.form['bloodQuantity_BloodGroupId']
            bloodQuantityId = request.form['bloodQuantityId']
            bloodQuantityMonth = request.form['bloodQuantityMonth']
            bloodQuantityYear = request.form['bloodQuantityYear']

            bloodQuantityVO = BloodQuantityVO()
            bloodQuantityDAO = BloodQuantityDAO()

            bloodQuantityVO.bloodQuantityId = bloodQuantityId
            bloodQuantityVO.bloodQuantity = bloodQuantity
            bloodQuantityVO.bloodQuantity_BloodGroupId = bloodQuantity_BloodGroupId
            bloodQuantityVO.bloodQuantityMonth = bloodQuantityMonth
            bloodQuantityVO.bloodQuantityYear = bloodQuantityYear

            bloodQuantityDAO.updateBloodQuantity(bloodQuantityVO)

            return redirect(url_for('bloodbankViewBloodQuantity'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
