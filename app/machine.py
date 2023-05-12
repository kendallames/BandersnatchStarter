from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
import joblib
from datetime import datetime


class Machine:
    """ Created class to create a machine object and to build a model, call the model, save the model, open and return
    info on the model. """
    def __init__(self, df: DataFrame):
        """Constructor method that takes in a dataframe, creates a model with various hyperparameters, fits the model
         and returns the timestamp the model was created. """
        self.name = "Random Forest Classifier"
        self.model = RandomForestClassifier(
            bootstrap=True,
            n_estimators=400,
            random_state=42,
            n_jobs=-1,
            max_samples=0.5,
            max_depth=25
        )
        target = df["Rarity"]
        features = df[["Level", "Health", "Energy", "Sanity"]]
        self.model.fit(features,target)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __call__(self, feature_basis: DataFrame):
        """Call method takes in a dataframe, makes predictions and confidence in predictions from the random forest
        model. Returns confidence as a float value"""
        prediction, *_ = self.model.predict(feature_basis)
        confidence, *_ = self.model.predict_proba(feature_basis)
        return prediction, float(max(confidence))

    def save(self, filepath):
        """Save method uses the joblib dump function to save the self object at the filepath. Dump serializes the
        self object."""
        joblib.dump(self, "filepath")

    @staticmethod
    def open(filepath):
        """Open method uses the joblib load function to open the object from the filepath. Load deserializes the self
        object."""
        return joblib.load(filepath)

    def info(self):
        """Info method returns an f string with the name of the model, and the initialized at timestamp."""
        return f"Base Model:{self.name}, initialized {self.timestamp}"

