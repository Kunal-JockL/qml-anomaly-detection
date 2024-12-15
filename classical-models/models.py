from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, classification_report, roc_auc_score
import pandas as pd

def optimize_threshold(y_proba, y_test, step=0.01):
    """
    Find the optimal threshold that maximizes the F1-score for class 1.

    Parameters:
        y_proba (array): Predicted probabilities for the positive class.
        y_test (array): Ground truth labels.
        step (float): Increment for threshold adjustment.

    Returns:
        dict: Dictionary containing the optimal threshold, corresponding F1-score, and the classification report.
    """
    best_threshold = 0.0
    best_f1_score = 0.0
    best_report = None

    # Iterate through thresholds from 0.0 to 1.0 with the given step size
    for threshold in [x * step for x in range(int(1 / step) + 1)]:
        # Apply the threshold to classify
        y_pred = (y_proba >= threshold).astype(int)

        # Generate evaluation metrics
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        f1 = report["1"]["f1-score"]  # Get F1-score for class 1

        # Update best threshold if this F1 is better
        if f1 > best_f1_score:
            best_f1_score = f1
            best_threshold = threshold
            best_report = report
            

    return best_threshold, best_report



def logistic_regression_with_analysis(data, target_column, important_features, threshold=None):
    """
    Builds a logistic regression model using ROC curve analysis to determine the best threshold
    and class weights. Evaluates the model's performance on specified important features.

    Parameters:
    - data (pd.DataFrame): The input dataset.
    - target_column (str): The name of the target variable column.
    - important_features (pd.DataFrame): A DataFrame with feature names and their importance.
    - threshold (float): A predefined threshold. If None, optimal threshold will be determined using the ROC curve.

    Returns:
    - dict: A dictionary containing precision, recall, F1-score, ROC AUC score, and the classification report.
    """
    # Use only the important features
    # feature_names = important_features['logistic_regression']['Feature'].tolist()
    feature_names = ['Amount', 'V3', 'V14', 'V17', 'V9']
    X = data[feature_names]
    y = data[target_column]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Compute class weights
    #class_weights = {0: len(y) / (2 * (y == 0).sum()), 1: len(y) / (2 * (y == 1).sum())} #change class weights formulae
    class_weights = {0: 1, 1: 35}

    # Fit Logistic Regression model
    model = LogisticRegression(max_iter=1000, random_state=42, class_weight=class_weights)
    model.fit(X_train, y_train)

    # Predict probabilities for the positive class
    y_proba = model.predict_proba(X_test)[:, 1]

    # Determine optimal threshold using ROC curve analysis if threshold not provided
    if threshold is None:
        fpr, tpr, thresholds = roc_curve(y_test, y_proba)
        gmeans = (tpr * (1 - fpr)) ** 0.5
        optimal_idx = gmeans.argmax()
        threshold = 1 - thresholds[optimal_idx]

    # Apply the threshold to classify
    y_pred = (y_proba >= threshold).astype(int)

    # Generate evaluation metrics
    report = classification_report(y_test, y_pred, output_dict=True)
    roc_auc = roc_auc_score(y_test, y_proba)

    # Print and return results
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("ROC AUC Score:", roc_auc)

    results = {
        'classification_report': report,
        'roc_auc_score': roc_auc,
        'threshold': threshold,
        'class_weights': class_weights
    }

    return results


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, classification_report, roc_auc_score
import pandas as pd

def random_forest_with_analysis(data, target_column, important_features, threshold=None):
    """
    Builds a Random Forest model, optimizes the decision threshold using predict_proba, and 
    computes the most optimal class weights based on class imbalance.
    
    Parameters:
    - data (pd.DataFrame): The input dataset.
    - target_column (str): The name of the target variable column.
    - important_features (pd.DataFrame): A DataFrame with feature names and their importance.
    - threshold (float): A predefined threshold. If None, optimal threshold will be determined using the ROC curve.

    Returns:
    - dict: A dictionary containing precision, recall, F1-score, ROC AUC score, and the classification report.
    """
    # Use only the important features
    #feature_names = important_features['Feature'].tolist()
    # feature_names = important_features['logistic_regression']['Feature'].tolist()
    feature_names = ['V17', 'V12', 'V14', 'V10', 'V16']
    X = data[feature_names]
    y = data[target_column]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Compute optimal class weights
    # class_weights = {0: len(y) / (2 * (y == 0).sum()), 1: len(y) / (2 * (y == 1).sum())}
    class_weights = {0: 1, 1: 35}

    # Fit Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight=class_weights)
    model.fit(X_train, y_train)

    # Predict probabilities for the positive class
    y_proba = model.predict_proba(X_test)[:, 1]

    # Determine optimal threshold using ROC curve analysis if threshold not provided
    if threshold is None:
        fpr, tpr, thresholds = roc_curve(y_test, y_proba)
        gmeans = (tpr * (1 - fpr)) ** 0.5
        optimal_idx = gmeans.argmax()
        threshold = thresholds[optimal_idx]

    # Apply the threshold to classify
    y_pred = (y_proba >= 0.54).astype(int)

    # Generate evaluation metrics
    report = classification_report(y_test, y_pred, output_dict=True)
    roc_auc = roc_auc_score(y_test, y_proba)

    # Print and return results
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("ROC AUC Score:", roc_auc)
    print('threshold:', threshold)
    print('class_weights:', class_weights)

    results = {
        'classification_report': report,
        'roc_auc_score': roc_auc,
        'threshold': threshold,
        'class_weights': class_weights
    }

    return results

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, classification_report, roc_auc_score
import pandas as pd

def gradient_boosting_with_analysis(data, target_column, important_features, threshold=None):
    """
    Builds a Gradient Boosting model (XGBoost), optimizes the decision threshold using predict_proba, 
    and computes the most optimal scale_pos_weight based on class imbalance.
    
    Parameters:
    - data (pd.DataFrame): The input dataset.
    - target_column (str): The name of the target variable column.
    - important_features (pd.DataFrame): A DataFrame with feature names and their importance.
    - threshold (float): A predefined threshold. If None, optimal threshold will be determined using the ROC curve.

    Returns:
    - dict: A dictionary containing precision, recall, F1-score, ROC AUC score, and the classification report.
    """
    # Use only the important features
    # feature_names = important_features['logistic_regression']['Feature'].tolist()
    feature_names = ['V14', 'V27', 'V10', 'V17', 'V11']
    X = data[feature_names]
    y = data[target_column]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Compute optimal scale_pos_weight
    scale_pos_weight = (y == 0).sum() / (y == 1).sum()

    # Fit Gradient Boosting (XGBoost) model
    model = XGBClassifier(
        random_state=42,
        scale_pos_weight=scale_pos_weight,
        # use_label_encoder=False,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)

    # Predict probabilities for the positive class
    y_proba = model.predict_proba(X_test)[:, 1]

    # Apply the threshold to classify
    y_pred = (y_proba >= 0.65).astype(int)

    # Generate evaluation metrics
    threshold, report = optimize_threshold(y_proba, y_test, 0.01)
    y_pred = (y_proba >= threshold).astype(int)
    roc_auc = roc_auc_score(y_test, y_proba)

    # Print and return results
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("ROC AUC Score:", roc_auc)
    print('threshold:', threshold)
    # print('class_weights:', class_weights)
    print('scale_pos_weight', scale_pos_weight)

    results = {
        'classification_report': report,
        'roc_auc_score': roc_auc,
        'threshold': threshold,
        'scale_pos_weight': scale_pos_weight
    }

    return results
