"""
Data Collection Module for Oman Economic Analysis

This module fetches economic data from the World Bank API for Oman and GCC countries.
Uses the official World Bank API (https://data.worldbank.org/)
"""

import requests
import pandas as pd
from typing import Dict, List, Optional
import time
import os

class OmanDataCollector:
    """
    Collects economic data from World Bank API for Oman and GCC countries.

    The World Bank provides free access to global development data including:
    - GDP and economic growth
    - Trade statistics
    - Employment and labor
    - Inflation and prices
    - And many more indicators
    """

    BASE_URL = "https://api.worldbank.org/v2"

    # Country codes for Oman and GCC countries
    COUNTRIES = {
        'OMN': 'Oman',
        'SAU': 'Saudi Arabia',
        'ARE': 'United Arab Emirates',
        'QAT': 'Qatar',
        'KWT': 'Kuwait',
        'BHR': 'Bahrain'
    }

    # Key economic indicators with their World Bank codes
    INDICATORS = {
        # GDP and Growth
        'NY.GDP.MKTP.CD': 'GDP (current US$)',
        'NY.GDP.MKTP.KD.ZG': 'GDP growth (annual %)',
        'NY.GDP.PCAP.CD': 'GDP per capita (current US$)',
        'NY.GDP.PCAP.KD.ZG': 'GDP per capita growth (annual %)',

        # Trade
        'NE.EXP.GNFS.ZS': 'Exports of goods and services (% of GDP)',
        'NE.IMP.GNFS.ZS': 'Imports of goods and services (% of GDP)',
        'BN.CAB.XOKA.CD': 'Current account balance (BoP, current US$)',
        'TG.VAL.TOTL.GD.ZS': 'Merchandise trade (% of GDP)',

        # Employment
        'SL.UEM.TOTL.ZS': 'Unemployment, total (% of labor force)',
        'SL.TLF.TOTL.IN': 'Labor force, total',
        'SL.TLF.CACT.ZS': 'Labor force participation rate (% of population 15+)',

        # Inflation and Prices
        'FP.CPI.TOTL.ZG': 'Inflation, consumer prices (annual %)',
        'NY.GDP.DEFL.KD.ZG': 'Inflation, GDP deflator (annual %)',

        # Population
        'SP.POP.TOTL': 'Population, total',
        'SP.POP.GROW': 'Population growth (annual %)',

        # Oil and Energy (important for GCC)
        'NY.GDP.PETR.RT.ZS': 'Oil rents (% of GDP)',
        'EG.USE.PCAP.KG.OE': 'Energy use (kg of oil equivalent per capita)',

        # Government and Finance
        'GC.REV.XGRT.GD.ZS': 'Revenue, excluding grants (% of GDP)',
        'GC.XPN.TOTL.GD.ZS': 'Expense (% of GDP)',

        # Foreign Investment
        'BX.KLT.DINV.WD.GD.ZS': 'Foreign direct investment, net inflows (% of GDP)',

        # Tourism
        'ST.INT.ARVL': 'International tourism, number of arrivals',
        'ST.INT.RCPT.CD': 'International tourism, receipts (current US$)',
    }

    def __init__(self, cache_dir: str = "data/raw"):
        """
        Initialize the data collector.

        Args:
            cache_dir: Directory to cache downloaded data
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def fetch_indicator(
        self,
        indicator_code: str,
        countries: Optional[List[str]] = None,
        start_year: int = 2000,
        end_year: int = 2023
    ) -> pd.DataFrame:
        """
        Fetch a single indicator for specified countries.

        Args:
            indicator_code: World Bank indicator code
            countries: List of country codes (default: all GCC)
            start_year: Start year for data
            end_year: End year for data

        Returns:
            DataFrame with the indicator data
        """
        if countries is None:
            countries = list(self.COUNTRIES.keys())

        country_str = ';'.join(countries)

        url = f"{self.BASE_URL}/country/{country_str}/indicator/{indicator_code}"
        params = {
            'format': 'json',
            'date': f'{start_year}:{end_year}',
            'per_page': 1000
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if len(data) < 2 or data[1] is None:
                print(f"No data available for indicator: {indicator_code}")
                return pd.DataFrame()

            records = []
            for item in data[1]:
                records.append({
                    'country_code': item['country']['id'],
                    'country_name': item['country']['value'],
                    'indicator_code': item['indicator']['id'],
                    'indicator_name': item['indicator']['value'],
                    'year': int(item['date']),
                    'value': item['value']
                })

            df = pd.DataFrame(records)
            return df

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {indicator_code}: {e}")
            return pd.DataFrame()

    def fetch_all_indicators(
        self,
        countries: Optional[List[str]] = None,
        start_year: int = 2000,
        end_year: int = 2023,
        save: bool = True
    ) -> pd.DataFrame:
        """
        Fetch all defined indicators for specified countries.

        Args:
            countries: List of country codes (default: all GCC)
            start_year: Start year
            end_year: End year
            save: Whether to save to CSV

        Returns:
            Combined DataFrame with all indicators
        """
        all_data = []

        print(f"Fetching {len(self.INDICATORS)} indicators...")

        for i, (code, name) in enumerate(self.INDICATORS.items(), 1):
            print(f"  [{i}/{len(self.INDICATORS)}] {name}...")
            df = self.fetch_indicator(code, countries, start_year, end_year)

            if not df.empty:
                all_data.append(df)

            # Be nice to the API
            time.sleep(0.5)

        if not all_data:
            print("No data fetched!")
            return pd.DataFrame()

        combined_df = pd.concat(all_data, ignore_index=True)

        if save:
            filepath = os.path.join(self.cache_dir, 'gcc_economic_data.csv')
            combined_df.to_csv(filepath, index=False)
            print(f"\nData saved to: {filepath}")
            print(f"Total records: {len(combined_df)}")

        return combined_df

    def fetch_oman_data(
        self,
        start_year: int = 2000,
        end_year: int = 2023,
        save: bool = True
    ) -> pd.DataFrame:
        """
        Fetch all indicators for Oman only.

        Args:
            start_year: Start year
            end_year: End year
            save: Whether to save to CSV

        Returns:
            DataFrame with Oman economic data
        """
        df = self.fetch_all_indicators(
            countries=['OMN'],
            start_year=start_year,
            end_year=end_year,
            save=False
        )

        if save and not df.empty:
            filepath = os.path.join(self.cache_dir, 'oman_economic_data.csv')
            df.to_csv(filepath, index=False)
            print(f"Oman data saved to: {filepath}")

        return df

    def get_indicator_info(self, indicator_code: str) -> Dict:
        """
        Get metadata about a specific indicator.

        Args:
            indicator_code: World Bank indicator code

        Returns:
            Dictionary with indicator metadata
        """
        url = f"{self.BASE_URL}/indicator/{indicator_code}"
        params = {'format': 'json'}

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if len(data) >= 2 and data[1]:
                return data[1][0]
            return {}

        except requests.exceptions.RequestException as e:
            print(f"Error fetching indicator info: {e}")
            return {}

    def list_available_indicators(self) -> pd.DataFrame:
        """
        List all indicators defined in this collector.

        Returns:
            DataFrame with indicator codes and descriptions
        """
        return pd.DataFrame([
            {'code': code, 'description': desc}
            for code, desc in self.INDICATORS.items()
        ])


def main():
    """Main function to demonstrate data collection."""
    collector = OmanDataCollector()

    print("=" * 60)
    print("Oman Economic Data Collector")
    print("=" * 60)

    # Fetch all GCC data
    print("\nFetching GCC economic data (2000-2023)...")
    df = collector.fetch_all_indicators()

    if not df.empty:
        print("\nSample data:")
        print(df.head(10))

        print("\nData summary:")
        print(f"  Countries: {df['country_name'].nunique()}")
        print(f"  Indicators: {df['indicator_name'].nunique()}")
        print(f"  Year range: {df['year'].min()} - {df['year'].max()}")
        print(f"  Total records: {len(df)}")


if __name__ == "__main__":
    main()
