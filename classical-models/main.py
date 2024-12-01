from .important_features import get_feature_importance
from .models import logistic_regression_with_analysis
import pandas as pd

if __name__ == '__main__':
    
    data = pd.read_csv("datasets\ccfraud\creditcard.csv")
    target_column = "Class"  # Replace with your target column name

    x = get_feature_importance(data, target_column, top_n=7)
    print(x)
    print(x['logistic_regression']['Feature'].tolist())

    logistic_regression_with_analysis(data, target_column, x)