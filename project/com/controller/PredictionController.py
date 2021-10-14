from flask import request, render_template, redirect, url_for
import pandas as pd
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.CityDAO import CityDAO
from project.com.dao.PredictionDAO import PredictionDAO
from project.com.dao.BloodGroupDAO import BloodGroupDAO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BloodGroupVO import BloodGroupVO
from project.com.vo.CityVO import CityVO
from project.com.controller.BloodQuantityPrediction import BloodQuantityPrediction
from project.com.vo.PredictionVO import PredictionVO
from datetime import datetime

@app.route('/admin/loadPrediction', methods=['GET'])
def adminLoadPrediction():
    try:
        if adminLoginSession() == "admin":
            cityDAO = CityDAO()
            cityVOList = cityDAO.viewCity()

            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            bloodGroupDAO = BloodGroupDAO()
            bloodGroupVOList = bloodGroupDAO.viewBloodGroup()

            return render_template('admin/addPrediction.html', cityVOList=cityVOList, areaVOList=areaVOList, bloodGroupVOList=bloodGroupVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertPrediction', methods=['POST', 'GET'])
def adminInsertPrediction():
    try:
        if adminLoginSession() == "admin":
            areaVO = AreaVO()
            areaDAO = AreaDAO()
            cityVO = CityVO()
            cityDAO = CityDAO()
            bloodGroupVO = BloodGroupVO()
            bloodGroupDAO = BloodGroupDAO()
            predictionVO = PredictionVO()
            predictionDAO = PredictionDAO()

            prediction_CityId = request.form['prediction_CityId']
            prediction_AreaId = request.form['prediction_AreaId']
            prediction_BloodGroupId = request.form['prediction_BloodGroupId']
            predictionForWhat = request.form['predictionForWhat']
            predictionPersonCount = int(request.form['predictionPersonCount'])
            predictionYear = int(request.form['predictionYear'])
            predictionMonth = request.form['predictionMonth']

            cityVO.cityId = prediction_CityId
            cityVOList = cityDAO.editCity(cityVO)

            areaVO.areaId = prediction_AreaId
            areaVOList = areaDAO.editArea(areaVO)

            bloodGroupVO.bloodGroupId = prediction_BloodGroupId
            bloodGroupVOList = bloodGroupDAO.editBloodGroup(bloodGroupVO)

            cityName = cityVOList[0].cityName
            areaName = areaVOList[0].areaName
            bloodGroupName = bloodGroupVOList[0].bloodGroupName

            print(predictionForWhat, predictionPersonCount, predictionYear, predictionMonth)
            print(cityName,areaName,bloodGroupName)

            columnName = ['BloodGroup', 'City', 'Area', 'Month', 'Year', 'For_What', 'Person_Count']
            columnValue = [bloodGroupName,cityName,areaName,predictionMonth,predictionYear,predictionForWhat,predictionPersonCount]

            X = pd.DataFrame([columnValue],columns=columnName)

            bloodQuantityPrediction = BloodQuantityPrediction()

            predictedBloodQuantity = bloodQuantityPrediction.prediction(X)
            print('predictedBloodQuantity>>>>>>>>',predictedBloodQuantity)

            prediction=0

            for i in predictedBloodQuantity:
                if i < 0.99:
                    prediction = 0
                elif i <= 1.50:
                    prediction = 1
                elif i <= 2.50:
                    prediction = 2
                elif i <= 3.50:
                    prediction = 3
                elif i <= 4.50:
                    prediction = 4
                elif i > 4.40:
                    prediction = 5

            currentDate = str(datetime.now().date())
            currentTime = datetime.now().strftime("%H:%M:%S")

            predictionVO.predictionForWhat = predictionForWhat
            predictionVO.predictionPersonCount = predictionPersonCount
            predictionVO.predictionMonth = predictionMonth
            predictionVO.predictionYear = predictionYear
            predictionVO.predictionBloodQuantity = prediction
            predictionVO.predictionTotalBloodQuantity = predictionPersonCount*prediction
            predictionVO.predictionDate = currentDate
            predictionVO.predictionTime = currentTime
            predictionVO.prediction_CityId = prediction_CityId
            predictionVO.prediction_AreaId = prediction_AreaId
            predictionVO.prediction_BloodGroupId = prediction_BloodGroupId

            predictionDAO.insertPrediction(predictionVO)

            return redirect(url_for('adminViewPrediction'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewPrediction', methods=['GET'])
def adminViewPrediction():
    try:
        if adminLoginSession() == "admin":
            predictionDAO = PredictionDAO()
            predictionVOList = predictionDAO.viewPrediction()

            return render_template('admin/viewPrediction.html', predictionVOList=predictionVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/deletePrediction', methods=['GET'])
def adminDeletePrediction():
    try:
        if adminLoginSession() == "admin":
            predictionDAO = PredictionDAO()

            predictionId = request.args.get('predictionId')

            predictionDAO.deletePrediction(predictionId)
            return redirect(url_for('adminViewPrediction'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
#-----------------------------------------------------------BLOOD BANK--------------------------------------------------------

@app.route('/bloodbank/viewPrediction', methods=['GET'])
def bloodBankViewPrediction():
    try:
        if adminLoginSession() == "bloodbank":
            predictionDAO = PredictionDAO()
            predictionVOList = predictionDAO.viewPrediction()

            return render_template('bloodbank/viewPrediction.html', predictionVOList=predictionVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
