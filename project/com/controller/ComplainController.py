import os

from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename

from project import app
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO

UPLOAD_FOLDER_BLOODBANK_COMPLAIN = 'project/static/adminResources/bloodbankcomplain/'
UPLOAD_FOLDER_BLOODBANK_REPLY = 'project/static/adminResources/bloodbankreply/'
UPLOAD_FOLDER_USER_COMPLAIN = 'project/static/adminResources/usercomplain/'
UPLOAD_FOLDER_USER_REPLY = 'project/static/adminResources/userreply/'

app.config['UPLOAD_FOLDER_BLOODBANK_COMPLAIN'] = UPLOAD_FOLDER_BLOODBANK_COMPLAIN
app.config['UPLOAD_FOLDER_BLOODBANK_REPLY'] = UPLOAD_FOLDER_BLOODBANK_REPLY
app.config['UPLOAD_FOLDER_USER_COMPLAIN'] = UPLOAD_FOLDER_USER_COMPLAIN
app.config['UPLOAD_FOLDER_USER_REPLY'] = UPLOAD_FOLDER_USER_REPLY

from datetime import datetime
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession


@app.route('/admin/viewComplain', methods=['GET'])
def adminViewComplain():
    try:
        if adminLoginSession() == "admin":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainStatus = "Pending"

            complainVO.complainStatus = complainStatus
            complainVOList = complainDAO.viewBloodbankComplain(complainVO)

            return render_template('admin/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply', methods=['GET'])
def adminLoadComplainReply():
    try:
        if adminLoginSession() == "admin":

            complainId = request.args.get('complainId')
            print(complainId)

            return render_template('admin/addComplainReply.html', complainId=complainId)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST', 'GET'])
def adminInsertComplainReply():
    try:
        if adminLoginSession() == "admin":

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.form['complainId']

            complainStatus = "Replied"

            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']

            file = request.files['file']

            replyFileName = secure_filename(file.filename)
            print(replyFileName)

            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER_BLOODBANK_REPLY'])
            print(replyFilePath)

            now = datetime.now()
            replyDate = now.strftime("%d/%m/%Y")
            replyTime = now.strftime("%H:%M:%S")
            file.save(os.path.join(replyFilePath, replyFileName))
            complainVO.complainId = complainId
            complainVO.complainStatus = complainStatus
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace("project", "..")
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainTo_LoginId = session['session_loginId']

            complainDAO.insertComplainReply(complainVO)
            return redirect(url_for('adminViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# ----------------------------------------------BLOODBANK------------------------------------------------------


@app.route('/bloodbank/loadComplain', methods=['GET'])
def bloodbankLoadComplaint():
    try:
        if adminLoginSession() == "bloodbank":
            return render_template('bloodbank/addComplain.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/insertComplain', methods=['POST', 'GET'])
def bloodbankInsertComplain():
    try:
        if adminLoginSession() == "bloodbank":

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']

            file = request.files['file']
            print(file)

            complainFileName = secure_filename(file.filename)
            print(complainFileName)

            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER_BLOODBANK_COMPLAIN'])
            print(complainFilePath)

            now = datetime.now()
            complainDate = now.strftime("%d/%m/%Y")
            complainTime = now.strftime("%H:%M:%S")

            file.save(os.path.join(complainFilePath, complainFileName))

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription

            complainVO.complainFileName = complainFileName

            complainVO.complainFilePath = complainFilePath.replace("project", "..")

            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime

            complainVO.complainStatus = 'Pending'

            complainVO.complainFrom_LoginId = session['session_loginId']

            complainDAO.insertComplain(complainVO)

            return redirect(url_for('bloodbankViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/viewComplain', methods=['GET'])
def bloodbankViewComplain():
    try:
        if adminLoginSession() == "bloodbank":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainVO.complainFrom_LoginId = session['session_loginId']

            complainVOList = complainDAO.viewComplain(complainVO)

            return render_template('bloodbank/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/viewComplainReply', methods=['GET'])
def bloodbankViewComplainReply():
    try:
        if adminLoginSession() == "bloodbank":

            complainDAO = ComplainDAO()

            complainVO = ComplainVO()

            complainId = request.args.get('complainId')

            complainVO.complainId = complainId

            complainVOList = complainDAO.viewComplainReply(complainVO)

            return render_template('bloodbank/viewComplainReply.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/deleteComplain', methods=['GET'])
def bloodbankDeleteComplain():
    try:
        if adminLoginSession() == "bloodbank":
            complainDAO = ComplainDAO()

            complainVO = ComplainVO()

            complainId = request.args.get('complainId')

            complainVO.complainId = complainId
            print(complainId)

            complainList = complainDAO.deleteComplain(complainVO)

            complainFileName = complainList.complainFileName
            complainFilePath = complainList.complainFilePath

            path = complainFilePath.replace("..", "project") + complainFileName
            os.remove(path)

            if complainList.complainStatus == 'Replied':
                replyFileName = complainList.replyFileName
                replyFilePath = complainList.replyFilePath

                path = replyFilePath.replace("..", "project") + replyFileName
                os.remove(path)

            return redirect(url_for('bloodbankViewComplain'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/viewUserComplain', methods=['GET'])
def bloodbankViewUserComplaint():
    try:
        if adminLoginSession() == "bloodbank":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainStatus = "Pending"

            complainVO.complainStatus = complainStatus
            complainVOList = complainDAO.viewUserComplain(complainVO)
            print(complainVOList)

            return render_template('bloodbank/viewUserComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/loadComplainReply', methods=['GET'])
def bloodbankLoadComplainReply():
    try:
        if adminLoginSession() == "bloodbank":

            complainId = request.args.get('complainId')
            print(complainId)

            return render_template('bloodbank/addComplainReply.html', complainId=complainId)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/insertComplainReply', methods=['POST', 'GET'])
def bloodbankInsertComplainReply():
    try:
        if adminLoginSession() == "bloodbank":

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.form['complainId']

            complainStatus = "Replied"

            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']

            file = request.files['file']

            replyFileName = secure_filename(file.filename)
            print(replyFileName)

            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER_USER_REPLY'])
            print(replyFilePath)

            now = datetime.now()
            replyDate = now.strftime("%d/%m/%Y")
            replyTime = now.strftime("%H:%M:%S")
            file.save(os.path.join(replyFilePath, replyFileName))
            complainVO.complainId = complainId
            complainVO.complainStatus = complainStatus
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace("project", "..")
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainTo_LoginId = session['session_loginId']

            complainDAO.insertComplainReply(complainVO)

            return redirect(url_for('bloodbankViewUserComplaint'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# ----------------------------------------------------USER--------------------------------------------------------------

@app.route('/user/loadComplain', methods=['GET'])
def userLoadComplaint():
    try:
        if adminLoginSession() == "user":
#_____________________________________________COMPLAIN_________________________________________________
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainVO.complainFrom_LoginId = session['session_loginId']

            complainVOList = complainDAO.viewComplain(complainVO)
#_____________________________________________COMPLAIN_REPLY____________________________________________


            return render_template('user/addComplain.html',complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST', 'GET'])
def userInsertComplain():
    try:
        if adminLoginSession() == "user":

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']

            file = request.files['file']
            print(file)

            complainFileName = secure_filename(file.filename)
            print(complainFileName)

            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER_USER_COMPLAIN'])
            print(complainFilePath)

            now = datetime.now()
            complainDate = now.strftime("%d/%m/%Y")
            complainTime = now.strftime("%H:%M:%S")

            file.save(os.path.join(complainFilePath, complainFileName))

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription

            complainVO.complainFileName = complainFileName

            complainVO.complainFilePath = complainFilePath.replace("project", "..")

            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime

            complainVO.complainStatus = 'Pending'

            complainVO.complainFrom_LoginId = session['session_loginId']

            complainDAO.insertComplain(complainVO)

            return redirect(url_for('userLoadComplaint'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# @app.route('/user/viewComplain', methods=['GET'])
# def userViewComplain():
#     try:
#         if adminLoginSession() == "user":
#             complainDAO = ComplainDAO()
#             complainVO = ComplainVO()
#
#             complainVO.complainFrom_LoginId = session['session_loginId']
#
#             complainVOList = complainDAO.viewComplain(complainVO)
#
#             return render_template('user/viewComplain.html', complainVOList=complainVOList)
#         else:
#             return adminLogoutSession()
#     except Exception as ex:
#         print(ex)
#
#
# @app.route('/user/viewComplainReply', methods=['GET'])
# def userViewComplainReply():
#     try:
#         if adminLoginSession() == "user":
#
#             complainDAO = ComplainDAO()
#
#             complainVO = ComplainVO()
#
#             complainId = request.args.get('complainId')
#
#             complainVO.complainId = complainId
#
#             complainVOList = complainDAO.viewComplainReply(complainVO)
#
#             return render_template('user/viewComplainReply.html', complainVOList=complainVOList)
#         else:
#             return adminLogoutSession()
#     except Exception as ex:
#         print(ex)


@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == "user":
            complainDAO = ComplainDAO()

            complainVO = ComplainVO()
            print("HEROHEROHEROHEROHEROHEROHEROHEROHEROHEROHEROHEROHEROHEROHERO")

            complainId = request.args.get('complainId')
            print(complainId)

            complainVO.complainId = complainId
            print(complainId)

            complainList = complainDAO.deleteComplain(complainVO)

            complainFileName = complainList.complainFileName
            complainFilePath = complainList.complainFilePath

            path = complainFilePath.replace("..", "project") + complainFileName
            os.remove(path)

            if complainList.complainStatus == 'Replied':
                replyFileName = complainList.replyFileName
                replyFilePath = complainList.replyFilePath

                path = replyFilePath.replace("..", "project") + replyFileName
                os.remove(path)

            return redirect(url_for('userLoadComplaint'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
