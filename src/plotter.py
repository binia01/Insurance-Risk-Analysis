import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class EDAPlotter:
    def __init__(self, df):
        self.df = df
        # Create Loss Ratio if it doesn't exist
        # Loss Ratio = Claims / Premium. (Lower is better for company)
        if 'LossRatio' not in self.df.columns:
            self.df['LossRatio'] = self.df['TotalClaims'] / self.df['TotalPremium']
            # Fix infinite values from division by zero
            self.df['LossRatio'] = self.df['LossRatio'].fillna(0)

    def plot_univariate_dist(self, column):
        plt.figure(figsize=(10, 5))
        sns.histplot(self.df[column], kde=True, bins=30)
        plt.title(f'Distribution of {column}')
        plt.show()

    def plot_correlation(self):
        plt.figure(figsize=(12, 10))
        # Select only numeric columns
        numeric_df = self.df.select_dtypes(include=['float64', 'int64'])
        sns.heatmap(numeric_df.corr(), annot=False, cmap='coolwarm')
        plt.title('Feature Correlation Matrix')
        plt.show()

    def plot_premium_vs_claims(self):
        """Scatter plot to identify 'Low Risk' vs 'High Risk'"""
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='TotalPremium', y='TotalClaims', data=self.df, alpha=0.5)
        plt.title('Total Premium vs Total Claims')
        plt.xlabel('Premium (Revenue)')
        plt.ylabel('Claims (Cost)')
        # Add a break-even line
        plt.plot([0, self.df['TotalPremium'].max()], [0, self.df['TotalPremium'].max()], 'r--', label='Break-even')
        plt.legend()
        plt.show()

    def get_comprehensive_stats(self, columns=['TotalPremium', 'TotalClaims']):
        """
        Generates a detailed statistical summary for key financial variables.
        Returns a DataFrame with Mean, Median, Std Dev, Skewness, Kurtosis, etc.
        """
        stats_dict = {}
        
        for col in columns:
            if col in self.df.columns:
                series = self.df[col]
                stats_dict[col] = {
                    'Count': series.count(),
                    'Mean': series.mean(),
                    'Median': series.median(),
                    'Standard Deviation': series.std(),
                    'Variance': series.var(),
                    'Min': series.min(),
                    'Max': series.max(),
                    'Range': series.max() - series.min(),
                    'Skewness': series.skew(),   # Critical for Insurance (Right-skewed)
                    'Kurtosis': series.kurt(),   # Critical for "Fat Tails" (Extreme events)
                    'CV (Variability)': series.std() / series.mean() if series.mean() != 0 else 0
                }
        
        return pd.DataFrame(stats_dict)