import pandas as pd
from ydata_profiling import ProfileReport

data = pd.read_csv("C:/Users/tam/Documents/data/titanic/train.csv")
profile = ProfileReport(data, title="Report", explorative=True)
profile.to_file("train.html")