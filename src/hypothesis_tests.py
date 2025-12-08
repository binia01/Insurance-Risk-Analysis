import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, chi2_contingency, f_oneway


class HypothesisTester:
    def __init__(self, df):
        self.df = df.copy()

        cols_to_fix = ['TotalPremium', 'TotalClaims']
        for col in cols_to_fix:
            # Force convert to numeric, turning errors (text) into NaN (0)
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)

        # Create a binary "CLaimed" column (1 if TotalClains > 0, else 0)
        self.df['Claimed'] = (self.df['TotalClaims'] > 0).astype(int)

        # Create Margin column (Premium - Claims)
        self.df['Margin'] = self.df['TotalPremium'] - self.df['TotalClaims']
    
    def get_data(self):
        """Returns the dataframe with the new calculated columns"""
        return self.df
    
    def test_risk_by_group(self, group_col, metric='TotalClaims'):
        """
        Generic function to test A/B groups.
        - If Metric is Categorical (e.g., Claimed/Not Claimed): Uses Chi-Squared.
        - If Metric is Numerical (e.g., Claim Amount): Uses T-Test (for 2 groups) or ANOVA (>2 groups).
        """
        print(f"--- Testing Hypothesis: Risk differences by {group_col} ---")
        if group_col not in self.df.columns:
            print(f"Error: Column '{group_col}' not found.")
            return

        # 2. Validation: Check if we have enough data (at least 2 groups)
        unique_groups = self.df[group_col].dropna().unique()
        if len(unique_groups) < 2:
            print(f"Error: Not enough categories in '{group_col}' to test. Found: {unique_groups}")
            return
        # A. Chi-Squared Test for Frequency (Risk Metric 1)
        print("\n1. Claim Frequency (Chi-Squared Test):")
        contingency_table = pd.crosstab(self.df[group_col], self.df['Claimed'])
        chi2, p_val_chi, _, _ = chi2_contingency(contingency_table)
        print(f"   P-Value: {p_val_chi:.5f}")
        self._interpret_p(p_val_chi)

        # B. T-Test/ANOVA for Severity/Margin (Risk Metric 2)
        print(f"\n2. {metric} Mean Difference (T-Test / ANOVA):")
        
        # Get groups
        groups = [group[metric].dropna() for name, group in self.df.groupby(group_col)]
        
        # Filter out groups with too few samples to avoid errors
        groups = [g for g in groups if len(g) > 30]

        if len(groups) < 2:
            print("   Error: Not enough valid groups for testing.")
            return

        if len(groups) == 2:
            stat, p_val_num = ttest_ind(groups[0], groups[1], equal_var=False)
            test_type = "T-Test"
        else:
            stat, p_val_num = f_oneway(*groups)
            test_type = "ANOVA"

        print(f"   Test Used: {test_type}")
        print(f"   P-Value: {p_val_num:.5f}")
        self._interpret_p(p_val_num)
        
        return p_val_chi, p_val_num

    def _interpret_p(self, p_value):
        if p_value < 0.05:
            print("   Result: REJECT Null Hypothesis (Significant Difference found).")
        else:
            print("   Result: FAIL TO REJECT Null Hypothesis (No significant difference).")