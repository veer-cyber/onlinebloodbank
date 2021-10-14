from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.BloodGroupDAO import BloodGroupDAO
from project.com.vo.BloodGroupVO import BloodGroupVO


@app.route('/admin/loadBloodGroup', methods=['GET'])
def adminLoadBloodGroup():
    try:
        if adminLoginSession() == "admin":
            return render_template('admin/addBloodGroup.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertBloodGroup', methods=['POST', 'GET'])
def adminInsertBloodGroup():
    try:
        if adminLoginSession() == "admin":
            bloodGroupName = request.form['bloodGroupName']

            bloodGroupVO = BloodGroupVO()
            bloodGroupDAO = BloodGroupDAO()

            bloodGroupVO.bloodGroupName = bloodGroupName

            bloodGroupDAO.insertBloodGroup(bloodGroupVO)

            return redirect(url_for('adminViewBloodGroup'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewBloodGroup', methods=['GET'])
def adminViewBloodGroup():
    try:
        if adminLoginSession() == "admin":
            bloodGroupDAO = BloodGroupDAO()
            bloodGroupVOList = bloodGroupDAO.viewBloodGroup()
            print("-------------", bloodGroupVOList)
            return render_template('admin/viewBloodGroup.html', bloodGroupVOList=bloodGroupVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteBloodGroup', methods=['GET'])
def adminDeleteBloodGroup():
    try:
        if adminLoginSession() == "admin":
            bloodGroupVO = BloodGroupVO()
            bloodGroupDAO = BloodGroupDAO()

            bloodGroupId = request.args.get('bloodGroupId')

            bloodGroupVO.bloodGroupId = bloodGroupId
            bloodGroupDAO.deleteBloodGroup(bloodGroupVO)
            return redirect(url_for('adminViewBloodGroup'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editBloodGroup', methods=['GET'])
def adminEditBloodGroup():
    try:
        if adminLoginSession() == "admin":
            bloodGroupVO = BloodGroupVO()

            bloodGroupDAO = BloodGroupDAO()

            bloodGroupId = request.args.get('bloodGroupId')
            print(bloodGroupId)

            bloodGroupVO.bloodGroupId = bloodGroupId

            bloodGroupVOList = bloodGroupDAO.editBloodGroup(bloodGroupVO)

            print("=======categoryVOList=======", bloodGroupVOList)

            print("=======type of categoryVOList=======", type(bloodGroupVOList))

            return render_template('admin/editBloodGroup.html', bloodGroupVOList=bloodGroupVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateBloodGroup', methods=['POST', 'GET'])
def adminUpdateBloodGroup():
    try:
        if adminLoginSession() == "admin":
            bloodGroupId = request.form['bloodGroupId']
            bloodGroupName = request.form['bloodGroupName']

            bloodGroupVO = BloodGroupVO()
            bloodGroupDAO = BloodGroupDAO()

            bloodGroupVO.bloodGroupId = bloodGroupId
            bloodGroupVO.bloodGroupName = bloodGroupName

            bloodGroupDAO.updateBloodgroup(bloodGroupVO)

            return redirect(url_for('adminViewBloodGroup'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
