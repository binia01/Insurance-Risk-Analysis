import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

class DataPreprocessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None

    def prepare_data(self, target_col='TotalClaims', problem_type='regression'):
        """
        Prepares data for modeling
        problem type: "regression" (predict amount) or "classification" (predict yes/no)
        """

        # Filter Data based on problem type
        data = self.df.copy()

        if problem_type == 'regression':
            # For severity, we only look at records where a claim happened
            data = data[data['TotalClaims'] > 0]
            y = data[target_col]
        elif problem_type == 'classification':
            # Create binary target: 1 if claim > 0, else 0
            data['ClaimClass'] = (data['TotalClaims'] > 0).astype(int)
            target_col = 'ClaimClass'
            y = data[target_col]

        # Feature Selection (Drop IDs and high-cardinality text)
        cols_to_drop = [
            'UnderwrittenCoverID', 'PolicyID', 'TransactionMonth', 'Mmcode', 
            'VehicleIntroDate', 'TotalPremium', 'TotalClaims', 'ClaimClass',
            'Margin', 'LossRatio', 'CalculatedPremiumPerTerm' 
        ]
        # Keep features that exist in the dataframe
        cols_to_drop = [c for c in cols_to_drop if c in data.columns]

        X = data.drop(columns=cols_to_drop)
        
        if target_col in X.columns:
            X = X.drop(columns=[target_col])

        # Define features types
        numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = X.select_dtypes(include=['object','category']).columns.tolist()

        # Create Transformers
        # Numeric: Impute missing with median, then scale
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        # Categorical: Impute missing with 'missing', then OneHotEncode
        # handle_unknown='ignore' is crucial for production models
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])

        # Combine into Preprocessor
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ],
            verbose_feature_names_out= False 
        )

        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X,y, test_size=0.2, random_state=42
        )

        # Fit and Transform
        # Note: We fit on Train, transform on Test to prevent data leakage
        self.X_train_processed = self.preprocessor.fit_transform(self.X_train)
        self.X_test_processed = self.preprocessor.transform(self.X_test)
        
        # Get feature names for SHAP later
        self.feature_names = self.preprocessor.get_feature_names_out()

        return self.X_train_processed, self.X_test_processed, self.y_train, self.y_test
