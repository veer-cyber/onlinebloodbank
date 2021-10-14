import warnings

from sklearn.externals import joblib
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings('ignore')


class BloodQuantityPrediction:
    def prediction(self, df):
        model_dump = joblib.load(r'project/static/adminResources/Blood_Model.sav')

        X = df
        print(X)

        self.dataPreprocessing(X,'BloodGroup')
        self.dataPreprocessing(X,'City')
        self.dataPreprocessing(X,'Area')
        self.dataPreprocessing(X,'Month')
        self.dataPreprocessing(X,'For_What')

        X = X.as_matrix()
        print(X, type(X))

        prediction = model_dump.predict(X)

        print('predicted_y:::', prediction,type(prediction))

        return prediction

    def dataPreprocessing(self,df, columnName):
        print(columnName)

        le = LabelEncoder()

        le.fit(df[columnName])

        df[columnName] = le.transform(df[columnName])
