import pandas as pd
from glob import glob
from django.apps import AppConfig
class MyAppConfig(AppConfig):
    name = 'hello'
    verbose_name = "My Application"
    def ready(self):
        df = pd.DataFrame(columns=["Name", "Number", "Position", "Height", "Weight", "Age", "Exp", "College"])
        for thingythings in glob("hello/static/csv/*.csv"):
            df2 = pd.read_csv(thingythings)
            df2.columns = ["Name", "Number", "Position", "Height", "Weight", "Age", "Exp", "College"]
            df = df.append(df2)

        df.to_csv("hello/static/csv/all.csv", index=False)