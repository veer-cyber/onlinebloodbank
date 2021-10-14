from datetime import datetime

from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO


@app.route('/bloodbank/loadFeedback', methods=['GET'])
def bloodbankLoadFeedback():
    try:
        if adminLoginSession() == "bloodbank":
            return render_template('bloodbank/addFeedback.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/insertFeedback', methods=['POST', 'GET'])
def bloodbankInsertFeedback():
    try:
        if adminLoginSession() == "bloodbank":

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']

            now = datetime.now()
            feedbackDate = now.strftime("%d/%m/%Y")
            feedbackTime = now.strftime("%H:%M:%S")

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription

            feedbackVO.feedbackRating = feedbackRating

            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime

            feedbackVO.feedbackFrom_LoginId = session['session_loginId']

            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('bloodbankViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/viewFeedback', methods=['GET'])
def bloodbankViewFeedback():
    try:
        if adminLoginSession() == "bloodbank":

            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackFrom_LoginId = session['session_loginId']
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId
            print(feedbackFrom_LoginId)
            feedbackVOList = feedbackDAO.viewFeedback(feedbackVO)

            return render_template('bloodbank/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/deleteFeedback', methods=['GET'])
def bloodbankDeleteFeedback():
    try:
        if adminLoginSession() == "bloodbank":
            feedbackDAO = FeedbackDAO()

            feedbackId = request.args.get('feedbackId')

            feedbackDAO.deleteFeedback(feedbackId)

            return redirect(url_for('bloodbankViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# -------------------

@app.route('/bloodbank/viewUserFeedback', methods=['GET'])
def bloodbankViewUserFeedback():
    try:
        if adminLoginSession() == "bloodbank":
            feedbackDAO = FeedbackDAO()
            feedbackVOList = feedbackDAO.viewUserFeedback()
            print("####################################")
            print(feedbackVOList)

            return render_template('bloodbank/viewUserFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/bloodbank/viewFeedbackReview')
def ViewFeedbackReview():
    try:
        if adminLoginSession() == "bloodbank":
            feedbackId = request.args.get('feedbackId')
            feedbackTo_LoginId = session['session_loginId']

            print(feedbackId)

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()
            print("####################@@@@@@@@@@@@@@@@@@@@@@@@@")
            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId
            print("@@@@@@@@@@@@@@@@@@@@$$$$$$$$$$$$$$$$$$$$$$$$$")
            feedbackDAO.viewBloodbankFeedbackReview(feedbackVO)
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            return redirect(url_for('bloodbankViewUserFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# -----------------------------------------------ADMIN------------------------------------------------------------



@app.route('/admin/viewFeedback', methods=['GET'])
def adminViewFeedback():
    try:
        if adminLoginSession() == "admin":
            feedbackDAO = FeedbackDAO()
            feedbackVOList = feedbackDAO.viewBloodbankFeedback()

            return render_template('admin/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewFeedbackReview')
def adminViewFeedbackReview():
    try:
        if adminLoginSession() == "admin":
            feedbackId = request.args.get('feedbackId')
            feedbackTo_LoginId = session['session_loginId']

            print(feedbackId)

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId

            feedbackDAO.viewAdminFeedbackReview(feedbackVO)

            return redirect(url_for('adminViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# ---------------------------------------------------USER----------------------------------------------------------

@app.route('/user/loadFeedback', methods=['GET'])
def userLoadFeedback():
    try:
        if adminLoginSession() == "user":

            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackFrom_LoginId = session['session_loginId']
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId
            print(feedbackFrom_LoginId)
            feedbackVOList = feedbackDAO.viewFeedback(feedbackVO)

            return render_template('user/addFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['POST', 'GET'])
def userInsertFeedback():
    try:
        if adminLoginSession() == "user":

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']

            now = datetime.now()
            feedbackDate = now.strftime("%d/%m/%Y")
            feedbackTime = now.strftime("%H:%M:%S")

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription

            feedbackVO.feedbackRating = feedbackRating

            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime

            feedbackVO.feedbackFrom_LoginId = session['session_loginId']

            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('userLoadFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# @app.route('/user/viewFeedback', methods=['GET'])
# def userViewFeedback():
#     try:
#         if adminLoginSession() == "user":
#
#             feedbackDAO = FeedbackDAO()
#             feedbackVO = FeedbackVO()
#
#             feedbackFrom_LoginId = session['session_loginId']
#             feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId
#             print(feedbackFrom_LoginId)
#             feedbackVOList = feedbackDAO.viewFeedback(feedbackVO)
#
#             return render_template('user/viewFeedback.html', feedbackVOList=feedbackVOList)
#         else:
#             return adminLogoutSession()
#     except Exception as ex:
#         print(ex)


@app.route('/user/deleteFeedback', methods=['GET'])
def userDeleteFeedback():
    try:
        if adminLoginSession() == "user":
            feedbackDAO = FeedbackDAO()

            feedbackId = request.args.get('feedbackId')

            feedbackDAO.deleteFeedback(feedbackId)

            return redirect(url_for('userLoadFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
