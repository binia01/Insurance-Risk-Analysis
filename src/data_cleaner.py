import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    
    def clean_for_models(self):
        # Main method to run the full pipeline
        self.optimize_types()
        self.handle_financial_anomalies()
        self.feature_engineering()       
        self.handle_missing_values()      
        return self.df
    
    def optimize_types(self):
        # Coneverts columns to appropriate types

        # Date Converison
        if 'TransactionMonth' in self.df.columns:
            self.df['TransactionMonth'] = pd.to_datetime(self.df['TransactionMonth'], errors='coerce')

        # ENsure Numerical columns are numeric
        cols_to_numeric = ['TotalPremium', 'TotalClaims', 'CalculatedPremiumPerTerm', 'RegistrationYear']

        for cols in cols_to_numeric:
            if cols in self.df.columns:
                self.df[cols] = pd.to_numeric(self.df[cols], errors='coerce')
        
        return self.df


    def handle_financial_anomalies(self):
        # Remove data errors (negatives) that might confuse models

        # Remove rows where Premium or Claims are negative (Accounting errors/Reversals)
        if 'TotalPremium' in self.df.columns:
            self.df = self.df[self.df['TotalPremium'] > 0]
        if 'TotalClaims' in self.df.columns:
            self.df = self.df[self.df['TotalClaims'] > 0]

        return self.df
    

    def feature_engineering(self):
        """
        Task 4 Requirement: Create new features (VehicleAge).
        """
        if 'RegistrationYear' in self.df.columns and 'TransactionMonth' in self.df.columns:
            # Calculate Transaction Year
            self.df['TransactionYear'] = self.df['TransactionMonth'].dt.year
            
            # Calculate Vehicle Age (Transaction Year - Registration Year)
            self.df['VehicleAge'] = self.df['TransactionYear'] - self.df['RegistrationYear']
            
            # Fix anomalies: Cars can't be negative years old, or > 50 years (likely typos)
            self.df.loc[(self.df['VehicleAge'] < 0) | (self.df['VehicleAge'] > 50), 'VehicleAge'] = 0
            
            # Drop the raw dates now that we have Age (optional, but helps models)
            # self.df = self.df.drop(columns=['TransactionMonth', 'RegistrationYear'])
            
        return self.df

    def handle_missing_values(self):
        """Strategies for missing values"""
        # Drop columns with >50% missing data
        threshold = len(self.df) * 0.5
        self.df = self.df.dropna(thresh=threshold, axis=1)
        
        # Fill categorical missing with 'Unknown'
        cat_cols = self.df.select_dtypes(include=['object']).columns
        self.df[cat_cols] = self.df[cat_cols].fillna('Unknown')
        
        # Fill numerical missing with median
        num_cols = self.df.select_dtypes(include=['number']).columns
        # Important: Calculate median only on valid numbers
        for col in num_cols:
            median_val = self.df[col].median()
            self.df[col] = self.df[col].fillna(median_val)
        
        return self.df

    def get_missing_stats(self):
        """Returns % of missing values per column."""
        missing = self.df.isnull().sum()
        total = len(self.df)
        return (missing / total) * 100