from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CityVO import CityVO
from project.com.vo.BloodGroupVO import BloodGroupVO
from project.com.vo.PredictionVO import PredictionVO


class PredictionDAO:
    def insertPrediction(self, predictionVO):
        db.session.add(predictionVO)

        db.session.commit()

    def viewPrediction(self):
        predictionList = db.session.query(PredictionVO, AreaVO, CityVO, BloodGroupVO).join(CityVO, PredictionVO.prediction_CityId == CityVO.cityId).join(AreaVO, PredictionVO.prediction_AreaId == AreaVO.areaId).join(BloodGroupVO, PredictionVO.prediction_BloodGroupId == BloodGroupVO.bloodGroupId).all()

        return predictionList

    def deletePrediction(self, predictionId):
        predictionList = PredictionVO.query.get(predictionId)

        db.session.delete(predictionList)

        db.session.commit()

    # def ajaxAreaUser(self, areaVO):
    #     areaList = AreaVO.query.filter_by(area_CityId = areaVO.area_CityId).all()
    #
    #     return areaList

    # def ajaxArea(self, areaVO):
    #     areaList = AreaVO.query.filter_by(area_CityId=areaVO.area_CityId).all()
    #
    #     return areaList
