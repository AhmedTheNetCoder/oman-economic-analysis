"""
Data Processing Module for Oman Economic Analysis

This module provides functions to clean, transform, and prepare
economic data for analysis and visualization.
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict
import os


class DataProcessor:
    """
    Processes and transforms economic data for analysis.

    Handles:
    - Data cleaning and missing value handling
    - Pivot transformations
    - Growth rate calculations
    - Aggregations and comparisons
    """

    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data processor.

        Args:
            data_dir: Base directory for data files
        """
        self.data_dir = data_dir
        self.raw_dir = os.path.join(data_dir, "raw")
        self.processed_dir = os.path.join(data_dir, "processed")
        os.makedirs(self.processed_dir, exist_ok=True)

    def load_data(self, filename: str = "gcc_economic_data.csv") -> pd.DataFrame:
        """
        Load economic data from CSV file.

        Args:
            filename: Name of the CSV file

        Returns:
            Loaded DataFrame
        """
        filepath = os.path.join(self.raw_dir, filename)
        if os.path.exists(filepath):
            return pd.read_csv(filepath)
        else:
            raise FileNotFoundError(f"Data file not found: {filepath}")

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the raw economic data.

        Args:
            df: Raw DataFrame

        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()

        # Convert year to integer
        df_clean['year'] = df_clean['year'].astype(int)

        # Sort by country, indicator, and year
        df_clean = df_clean.sort_values(['country_code', 'indicator_code', 'year'])

        # Remove completely empty rows
        df_clean = df_clean.dropna(subset=['country_code', 'indicator_code', 'year'])

        return df_clean

    def pivot_by_year(
        self,
        df: pd.DataFrame,
        indicator_code: str,
        country_codes: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Pivot data to have years as columns for a specific indicator.

        Args:
            df: Economic data DataFrame
            indicator_code: World Bank indicator code
            country_codes: Optional list of country codes to filter

        Returns:
            Pivoted DataFrame with years as columns
        """
        # Filter by indicator
        df_filtered = df[df['indicator_code'] == indicator_code].copy()

        # Filter by countries if specified
        if country_codes:
            df_filtered = df_filtered[df_filtered['country_code'].isin(country_codes)]

        # Pivot
        pivoted = df_filtered.pivot_table(
            index='country_name',
            columns='year',
            values='value',
            aggfunc='first'
        )

        return pivoted

    def pivot_by_indicator(
        self,
        df: pd.DataFrame,
        country_code: str,
        indicators: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Pivot data to have indicators as rows and years as columns for a country.

        Args:
            df: Economic data DataFrame
            country_code: Country code (e.g., 'OMN')
            indicators: Optional list of indicator codes to filter

        Returns:
            Pivoted DataFrame
        """
        # Filter by country
        df_filtered = df[df['country_code'] == country_code].copy()

        # Filter by indicators if specified
        if indicators:
            df_filtered = df_filtered[df_filtered['indicator_code'].isin(indicators)]

        # Pivot
        pivoted = df_filtered.pivot_table(
            index='indicator_name',
            columns='year',
            values='value',
            aggfunc='first'
        )

        return pivoted

    def calculate_growth_rate(
        self,
        df: pd.DataFrame,
        indicator_code: str,
        country_code: str = 'OMN'
    ) -> pd.DataFrame:
        """
        Calculate year-over-year growth rate for an indicator.

        Args:
            df: Economic data DataFrame
            indicator_code: Indicator to calculate growth for
            country_code: Country code

        Returns:
            DataFrame with growth rates
        """
        # Filter data
        df_filtered = df[
            (df['indicator_code'] == indicator_code) &
            (df['country_code'] == country_code)
        ].copy()

        df_filtered = df_filtered.sort_values('year')

        # Calculate growth rate
        df_filtered['growth_rate'] = df_filtered['value'].pct_change() * 100

        return df_filtered[['year', 'value', 'growth_rate']]

    def compare_countries(
        self,
        df: pd.DataFrame,
        indicator_code: str,
        year: int
    ) -> pd.DataFrame:
        """
        Compare all GCC countries for a specific indicator in a given year.

        Args:
            df: Economic data DataFrame
            indicator_code: Indicator to compare
            year: Year to compare

        Returns:
            DataFrame with country comparison
        """
        df_filtered = df[
            (df['indicator_code'] == indicator_code) &
            (df['year'] == year)
        ].copy()

        df_filtered = df_filtered.sort_values('value', ascending=False)

        # Add rank
        df_filtered['rank'] = range(1, len(df_filtered) + 1)

        return df_filtered[['rank', 'country_name', 'value', 'indicator_name']]

    def get_latest_values(
        self,
        df: pd.DataFrame,
        country_code: str = 'OMN'
    ) -> pd.DataFrame:
        """
        Get the most recent value for each indicator for a country.

        Args:
            df: Economic data DataFrame
            country_code: Country code

        Returns:
            DataFrame with latest values
        """
        df_filtered = df[df['country_code'] == country_code].copy()

        # Get the latest non-null value for each indicator
        latest = df_filtered.dropna(subset=['value']).sort_values('year', ascending=False)
        latest = latest.groupby('indicator_code').first().reset_index()

        return latest[['indicator_code', 'indicator_name', 'year', 'value']]

    def calculate_gcc_average(
        self,
        df: pd.DataFrame,
        indicator_code: str
    ) -> pd.DataFrame:
        """
        Calculate GCC average for an indicator over time.

        Args:
            df: Economic data DataFrame
            indicator_code: Indicator code

        Returns:
            DataFrame with yearly GCC averages
        """
        df_filtered = df[df['indicator_code'] == indicator_code].copy()

        gcc_avg = df_filtered.groupby('year').agg({
            'value': ['mean', 'std', 'min', 'max', 'count']
        }).reset_index()

        gcc_avg.columns = ['year', 'gcc_average', 'gcc_std', 'gcc_min', 'gcc_max', 'country_count']

        return gcc_avg

    def prepare_time_series(
        self,
        df: pd.DataFrame,
        indicator_code: str,
        country_code: str = 'OMN'
    ) -> pd.DataFrame:
        """
        Prepare time series data for a specific indicator and country.

        Args:
            df: Economic data DataFrame
            indicator_code: Indicator code
            country_code: Country code

        Returns:
            Time series DataFrame
        """
        df_filtered = df[
            (df['indicator_code'] == indicator_code) &
            (df['country_code'] == country_code)
        ].copy()

        df_filtered = df_filtered.sort_values('year')
        df_filtered = df_filtered[['year', 'value']].dropna()

        # Add moving averages
        if len(df_filtered) >= 3:
            df_filtered['ma_3'] = df_filtered['value'].rolling(window=3).mean()

        if len(df_filtered) >= 5:
            df_filtered['ma_5'] = df_filtered['value'].rolling(window=5).mean()

        return df_filtered

    def export_processed_data(
        self,
        df: pd.DataFrame,
        filename: str
    ) -> str:
        """
        Export processed data to CSV.

        Args:
            df: Processed DataFrame
            filename: Output filename

        Returns:
            Path to saved file
        """
        filepath = os.path.join(self.processed_dir, filename)
        df.to_csv(filepath, index=False)
        return filepath

    def create_summary_statistics(
        self,
        df: pd.DataFrame,
        country_code: str = 'OMN'
    ) -> pd.DataFrame:
        """
        Create summary statistics for all indicators for a country.

        Args:
            df: Economic data DataFrame
            country_code: Country code

        Returns:
            Summary statistics DataFrame
        """
        df_filtered = df[df['country_code'] == country_code].copy()

        summary = df_filtered.groupby(['indicator_code', 'indicator_name']).agg({
            'value': ['count', 'mean', 'std', 'min', 'max'],
            'year': ['min', 'max']
        }).reset_index()

        summary.columns = [
            'indicator_code', 'indicator_name',
            'data_points', 'mean', 'std', 'min_value', 'max_value',
            'first_year', 'last_year'
        ]

        return summary


def main():
    """Demonstrate data processing capabilities."""
    processor = DataProcessor()

    print("=" * 60)
    print("Oman Economic Data Processor")
    print("=" * 60)

    try:
        df = processor.load_data()
        df_clean = processor.clean_data(df)

        print(f"\nLoaded {len(df_clean)} records")

        # Get latest values for Oman
        print("\nLatest values for Oman:")
        latest = processor.get_latest_values(df_clean, 'OMN')
        print(latest.to_string(index=False))

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please run the data collector first to fetch data.")


if __name__ == "__main__":
    main()
