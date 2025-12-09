import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, chi2_contingency, f_oneway

class HypothesisTester:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        # Clean / Prep Data
        cols_to_numeric = ['TotalPremium', 'TotalClaims']
        for col in cols_to_numeric:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)

        # Create Derived Metrics
        self.df['Margin'] = self.df['TotalPremium'] - self.df['TotalClaims']
        self.df['Claimed'] = (self.df['TotalClaims'] > 0).astype(int)

    def _log_result(self, test_name, p_value, decision, recommendation):
        """Internal helper to format the output professionally."""
        print(f"\n{'='*60}")
        print(f"TEST: {test_name}")
        print(f"{'-'*60}")
        print(f"P-Value:      {p_value:.5f}")
        print(f"Threshold:    0.05")
        print(f"Decision:     {decision}")
        print(f"ACTION:       {recommendation}")
        print(f"{'='*60}\n")

    def test_province_risk(self):
        """
        Hypothesis 1: No risk differences across provinces.
        Metric: TotalClaims (Severity)
        Test: ANOVA
        """
        # Filter for valid provinces
        valid_provinces = self.df['Province'].dropna().unique()
        groups = [self.df[self.df['Province'] == p]['TotalClaims'] for p in valid_provinces]
        
        stat, p_val = f_oneway(*groups)
        
        decision = "REJECT Null Hypothesis" if p_val < 0.05 else "FAIL TO REJECT Null Hypothesis"
        rec = "Implement Territorial Rating. Apply a risk loading factor (e.g., 1.2x) to high-claim provinces like Gauteng." if p_val < 0.05 else "Maintain uniform national pricing."
        
        self._log_result("H0: No Risk Difference Across Provinces", p_val, decision, rec)

    def test_zip_risk(self):
        """
        Hypothesis 2: No risk differences between Zip Codes.
        Metric: TotalClaims (Severity)
        Test: T-Test (Top 2 Zips for A/B simulation)
        """
        # Select Top 2 Zip Codes by volume
        top_zips = self.df['PostalCode'].value_counts().head(2).index.tolist()
        group_a = self.df[self.df['PostalCode'] == top_zips[0]]['TotalClaims']
        group_b = self.df[self.df['PostalCode'] == top_zips[1]]['TotalClaims']
        
        stat, p_val = ttest_ind(group_a, group_b, equal_var=False)
        
        decision = "REJECT Null Hypothesis" if p_val < 0.05 else "FAIL TO REJECT Null Hypothesis"
        rec = f"Geographic risk is granular. Implement geo-fencing pricing models distinguishing Zip {top_zips[0]} from {top_zips[1]}." if p_val < 0.05 else "Zip-level granularity provides no additional lift over Province-level rating."
        
        self._log_result(f"H0: No Risk Difference Between Zip {top_zips[0]} & {top_zips[1]}", p_val, decision, rec)

    def test_zip_margin(self):
        """
        Hypothesis 3: No margin (profit) difference between Zip Codes.
        Metric: Margin (Premium - Claims)
        Test: T-Test
        """
        top_zips = self.df['PostalCode'].value_counts().head(2).index.tolist()
        group_a = self.df[self.df['PostalCode'] == top_zips[0]]['Margin']
        group_b = self.df[self.df['PostalCode'] == top_zips[1]]['Margin']
        
        stat, p_val = ttest_ind(group_a, group_b, equal_var=False)
        
        decision = "REJECT Null Hypothesis" if p_val < 0.05 else "FAIL TO REJECT Null Hypothesis"
        rec = "Pricing inefficiency detected. One zip code is significantly more profitable; consider lowering premiums there to capture market share." if p_val < 0.05 else "Current pricing model effectively neutralizes risk differences, maintaining consistent margins."
        
        self._log_result(f"H0: No Margin Difference Between Zip {top_zips[0]} & {top_zips[1]}", p_val, decision, rec)

    def test_gender_risk(self):
        """
        Hypothesis 4: No risk difference between Women and Men.
        Metric: Claim Frequency (Claimed?)
        Test: Chi-Squared
        Control: Passenger Vehicles Only
        """
        # Control Step
        segment = self.df[(self.df['VehicleType'].astype(str).str.contains('Passenger')) & 
                          (self.df['Gender'].isin(['Male', 'Female', 'M', 'F']))]
        
        contingency = pd.crosstab(segment['Gender'], segment['Claimed'])
        chi2, p_val, _, _ = chi2_contingency(contingency)
        
        decision = "REJECT Null Hypothesis" if p_val < 0.05 else "FAIL TO REJECT Null Hypothesis"
        rec = "Launch 'HerDrive' product line. Statistically significant lower frequency justifies a 5% 'Safe Driver' discount for the lower-risk gender." if p_val < 0.05 else "Gender is not a predictive rating factor. Do not include in pricing model."
        
        self._log_result("H0: No Risk Difference Between Genders", p_val, decision, rec)

    def get_data(self):
        return self.df