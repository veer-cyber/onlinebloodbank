from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CityVO import CityVO


class AreaDAO:
    def insertArea(self, areaVO):
        db.session.add(areaVO)

        db.session.commit()

    def viewArea(self):
        areaList = db.session.query(AreaVO, CityVO).join(CityVO, AreaVO.area_CityId == CityVO.cityId).all()

        return areaList

    def deleteArea(self, areaId):
        areaList = AreaVO.query.get(areaId)

        db.session.delete(areaList)

        db.session.commit()

    def editArea(self, areaVO):
        areaList = AreaVO.query.filter_by(areaId=areaVO.areaId)

        return areaList

    def updateArea(self, areaVO):
        db.session.merge(areaVO)

        db.session.commit()

    # def ajaxAreaUser(self, areaVO):
    #     areaList = AreaVO.query.filter_by(area_CityId = areaVO.area_CityId).all()
    #
    #     return areaList

    def ajaxArea(self, areaVO):
        areaList = AreaVO.query.filter_by(area_CityId=areaVO.area_CityId).all()

        return areaList
