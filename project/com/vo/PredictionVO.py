from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.BloodGroupVO import BloodGroupVO
from project.com.vo.CityVO import CityVO


class PredictionVO(db.Model):
    __tablename__ = "predictionmaster"
    predictionId = db.Column('predictionId', db.Integer, primary_key=True, autoincrement=True)
    predictionForWhat = db.Column('predictionForWhat', db.String(100), nullable=False)
    predictionPersonCount = db.Column('predictionPersonCount', db.Integer, nullable=False)
    predictionMonth = db.Column('predictionMonth', db.String(100), nullable=False)
    predictionYear = db.Column('predictionYear', db.Integer, nullable=False)
    predictionBloodQuantity = db.Column('predictionBloodQuantity', db.Integer, nullable=False)
    predictionTotalBloodQuantity = db.Column('predictionTotalBloodQuantity', db.Integer, nullable=False)
    predictionDate = db.Column('predictionDate', db.String(100), nullable=False)
    predictionTime = db.Column('predictionTime', db.String(100), nullable=False)
    prediction_CityId = db.Column('prediction_CityId', db.Integer, db.ForeignKey(CityVO.cityId))
    prediction_AreaId = db.Column('prediction_areaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    prediction_BloodGroupId = db.Column('prediction_BloodGroupId', db.Integer, db.ForeignKey(BloodGroupVO.bloodGroupId))

    def as_dict(self):
        return {
            'predictionId': self.predictionId,
            'predictionForWhat': self.predictionForWhat,
            'predictionPersonCount': self.predictionPersonCount,
            'predictionMonth': self.predictionMonth,
            'predictionYear': self.predictionYear,
            'predictionBloodQuantity': self.predictionBloodQuantity,
            'predictionTotalBloodQuantity': self.predictionTotalBloodQuantity,
            'predictionDate': self.predictionDate,
            'predictionTime': self.predictionTime,
            'prediction_CityId': self.prediction_CityId,
            'prediction_AreaId': self.prediction_AreaId,
            'prediction_BloodGroupId': self.prediction_BloodGroupId
        }


db.create_all()
