from project import db
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.LoginVO import LoginVO


class FeedbackDAO:
    def insertFeedback(self, feedbackVO):
        db.session.add(feedbackVO)
        db.session.commit()

    def viewFeedback(self, feedbackVO):
        print(feedbackVO.feedbackFrom_LoginId)
        feedbackList = FeedbackVO.query.filter_by(feedbackFrom_LoginId=feedbackVO.feedbackFrom_LoginId).all()

        return feedbackList

    def viewBloodbankFeedback(self):
        feedbackList = db.session.query(FeedbackVO, LoginVO).join(LoginVO,
                                                                  FeedbackVO.feedbackFrom_LoginId == LoginVO.loginId).filter(
            LoginVO.loginRole == "bloodbank").all()

        return feedbackList

    def viewUserFeedback(self):
        feedbackList = db.session.query(FeedbackVO, LoginVO).join(LoginVO,
                                                                  FeedbackVO.feedbackFrom_LoginId == LoginVO.loginId).filter(
            LoginVO.loginRole == "user").all()

        print(feedbackList)
        return feedbackList

    def deleteFeedback(self, feedbackId):
        feedbackList = FeedbackVO.query.get(feedbackId)

        db.session.delete(feedbackList)

        db.session.commit()

    def viewAdminFeedbackReview(self, feedbackVO):
        db.session.merge(feedbackVO)

        db.session.commit()

    def viewBloodbankFeedbackReview(self, feedbackVO):
        db.session.merge(feedbackVO)

        db.session.commit()
