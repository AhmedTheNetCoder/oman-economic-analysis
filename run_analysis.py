"""
Run Complete Oman Economic Analysis
This script executes all notebooks and generates outputs.
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_collector import OmanDataCollector
from src.data_processor import DataProcessor

# Settings
plt.style.use('seaborn-v0_8-whitegrid')
pd.set_option('display.float_format', '{:,.2f}'.format)

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs', 'charts')

# Color scheme for GCC countries
COLORS = {
    'Oman': '#E41A1C',
    'Saudi Arabia': '#377EB8',
    'United Arab Emirates': '#4DAF4A',
    'Qatar': '#984EA3',
    'Kuwait': '#FF7F00',
    'Bahrain': '#A65628'
}


def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def run_data_collection():
    """Notebook 01: Data Collection"""
    print_header("NOTEBOOK 01: DATA COLLECTION")

    collector = OmanDataCollector(cache_dir=os.path.join(DATA_DIR, 'raw'))

    print("\nFetching GCC economic data from World Bank API...")
    print("This may take 2-3 minutes...\n")

    df = collector.fetch_all_indicators(
        start_year=2000,
        end_year=2023,
        save=True
    )

    print("\n" + "-" * 40)
    print("DATA COLLECTION SUMMARY")
    print("-" * 40)
    print(f"Total records: {len(df):,}")
    print(f"Countries: {df['country_name'].nunique()}")
    print(f"Indicators: {df['indicator_name'].nunique()}")
    print(f"Year range: {df['year'].min()} - {df['year'].max()}")

    print("\nCountries included:")
    for country in sorted(df['country_name'].unique()):
        count = len(df[df['country_name'] == country])
        print(f"  - {country}: {count:,} records")

    return df


def run_gdp_analysis(df):
    """Notebook 02: GDP Analysis"""
    print_header("NOTEBOOK 02: GDP ANALYSIS")

    # GDP indicator
    gdp_ind = 'NY.GDP.MKTP.CD'
    growth_ind = 'NY.GDP.MKTP.KD.ZG'
    gdp_pc_ind = 'NY.GDP.PCAP.CD'

    # Oman GDP
    oman_gdp = df[(df['indicator_code'] == gdp_ind) &
                  (df['country_code'] == 'OM')].sort_values('year')

    if oman_gdp.empty:
        print("No GDP data available")
        return

    oman_gdp['gdp_billions'] = oman_gdp['value'] / 1e9

    print("\nOman GDP (Billion USD):")
    print("-" * 30)
    recent = oman_gdp[oman_gdp['year'] >= 2018]
    for _, row in recent.iterrows():
        if pd.notna(row['gdp_billions']):
            print(f"  {int(row['year'])}: ${row['gdp_billions']:.1f}B")

    # Plot 1: GDP Trend
    fig, ax = plt.subplots(figsize=(12, 6))
    valid_gdp = oman_gdp.dropna(subset=['gdp_billions'])
    ax.plot(valid_gdp['year'], valid_gdp['gdp_billions'],
            marker='o', linewidth=2, markersize=6, color='#E41A1C')
    ax.fill_between(valid_gdp['year'], valid_gdp['gdp_billions'], alpha=0.3, color='#E41A1C')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('GDP (Billion USD)', fontsize=12)
    ax.set_title('Oman GDP (2000-2023)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'oman_gdp_trend.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("\nSaved: oman_gdp_trend.png")

    # GDP Growth
    oman_growth = df[(df['indicator_code'] == growth_ind) &
                     (df['country_code'] == 'OM')].sort_values('year')
    oman_growth = oman_growth.dropna(subset=['value'])

    if not oman_growth.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = ['#2ca02c' if v >= 0 else '#d62728' for v in oman_growth['value']]
        ax.bar(oman_growth['year'], oman_growth['value'], color=colors, edgecolor='white')
        ax.axhline(y=0, color='black', linewidth=0.5)
        ax.axhline(y=oman_growth['value'].mean(), color='blue', linestyle='--',
                   label=f'Average: {oman_growth["value"].mean():.1f}%')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('GDP Growth Rate (%)', fontsize=12)
        ax.set_title('Oman GDP Growth Rate (Annual %)', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'oman_gdp_growth.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print("Saved: oman_gdp_growth.png")

    # GCC GDP Comparison
    gcc_gdp = df[df['indicator_code'] == gdp_ind].copy()
    gcc_gdp['gdp_billions'] = gcc_gdp['value'] / 1e9
    gcc_gdp = gcc_gdp.dropna(subset=['gdp_billions'])

    if not gcc_gdp.empty:
        latest_year = gcc_gdp['year'].max()
        gcc_latest = gcc_gdp[gcc_gdp['year'] == latest_year].sort_values('gdp_billions', ascending=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        bar_colors = [COLORS.get(c, '#999999') for c in gcc_latest['country_name']]
        bars = ax.barh(gcc_latest['country_name'], gcc_latest['gdp_billions'], color=bar_colors)
        ax.set_xlabel('GDP (Billion USD)', fontsize=12)
        ax.set_title(f'GCC GDP Comparison ({int(latest_year)})', fontsize=14, fontweight='bold')
        for bar, value in zip(bars, gcc_latest['gdp_billions']):
            ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                    f'${value:.0f}B', va='center', fontsize=10)
        ax.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'gcc_gdp_comparison.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print("Saved: gcc_gdp_comparison.png")

        # GCC GDP Trends
        fig, ax = plt.subplots(figsize=(14, 7))
        for country in gcc_gdp['country_name'].unique():
            country_data = gcc_gdp[gcc_gdp['country_name'] == country].sort_values('year')
            color = COLORS.get(country, '#999999')
            linewidth = 3 if country == 'Oman' else 1.5
            ax.plot(country_data['year'], country_data['gdp_billions'],
                    marker='o', markersize=3, linewidth=linewidth,
                    color=color, label=country)
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('GDP (Billion USD)', fontsize=12)
        ax.set_title('GCC GDP Trends (2000-2023)', fontsize=14, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'gcc_gdp_trends.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print("Saved: gcc_gdp_trends.png")

    # GDP per capita
    gcc_pc = df[df['indicator_code'] == gdp_pc_ind].copy()
    gcc_pc = gcc_pc.dropna(subset=['value'])

    if not gcc_pc.empty:
        latest_year = gcc_pc['year'].max()
        gcc_pc_latest = gcc_pc[gcc_pc['year'] == latest_year].sort_values('value', ascending=True)

        if not gcc_pc_latest.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            bar_colors = [COLORS.get(c, '#999999') for c in gcc_pc_latest['country_name']]
            bars = ax.barh(gcc_pc_latest['country_name'], gcc_pc_latest['value'], color=bar_colors)
            ax.set_xlabel('GDP per Capita (USD)', fontsize=12)
            ax.set_title(f'GCC GDP per Capita ({int(latest_year)})', fontsize=14, fontweight='bold')
            for bar, value in zip(bars, gcc_pc_latest['value']):
                if pd.notna(value):
                    ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
                            f'${value:,.0f}', va='center', fontsize=10)
            ax.grid(True, alpha=0.3, axis='x')
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, 'gcc_gdp_per_capita.png'), dpi=150, bbox_inches='tight')
            plt.close()
            print("Saved: gcc_gdp_per_capita.png")


def run_trade_analysis(df):
    """Notebook 03: Trade Analysis"""
    print_header("NOTEBOOK 03: TRADE ANALYSIS")

    export_ind = 'NE.EXP.GNFS.ZS'
    import_ind = 'NE.IMP.GNFS.ZS'
    oil_ind = 'NY.GDP.PETR.RT.ZS'

    # Exports vs Imports
    oman_exports = df[(df['indicator_code'] == export_ind) &
                      (df['country_code'] == 'OM')].sort_values('year')
    oman_imports = df[(df['indicator_code'] == import_ind) &
                      (df['country_code'] == 'OM')].sort_values('year')

    oman_exports = oman_exports.dropna(subset=['value'])
    oman_imports = oman_imports.dropna(subset=['value'])

    if not oman_exports.empty and not oman_imports.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(oman_exports['year'], oman_exports['value'],
                marker='o', linewidth=2, label='Exports (% of GDP)', color='#2ca02c')
        ax.plot(oman_imports['year'], oman_imports['value'],
                marker='s', linewidth=2, label='Imports (% of GDP)', color='#d62728')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('% of GDP', fontsize=12)
        ax.set_title('Oman Exports vs Imports (% of GDP)', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'oman_trade_trends.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print("\nSaved: oman_trade_trends.png")
    else:
        print("\nTrade data not available (API timeout)")

    # Oil dependency
    oman_oil = df[(df['indicator_code'] == oil_ind) &
                  (df['country_code'] == 'OM')].sort_values('year')
    oman_oil = oman_oil.dropna(subset=['value'])

    if not oman_oil.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(oman_oil['year'], oman_oil['value'], color='#1f77b4', edgecolor='white')
        ax.axhline(y=oman_oil['value'].mean(), color='red', linestyle='--',
                   label=f'Average: {oman_oil["value"].mean():.1f}%')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Oil Rents (% of GDP)', fontsize=12)
        ax.set_title('Oman Oil Dependency', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'oman_oil_dependency.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print("Saved: oman_oil_dependency.png")

        print(f"\nOil Dependency Stats:")
        print(f"  Average: {oman_oil['value'].mean():.1f}% of GDP")
        print(f"  Latest: {oman_oil['value'].iloc[-1]:.1f}% ({int(oman_oil['year'].iloc[-1])})")


def run_gcc_comparison(df):
    """Notebook 04: GCC Comparison"""
    print_header("NOTEBOOK 04: GCC COMPARISON")

    # Growth rate comparison
    growth_ind = 'NY.GDP.MKTP.KD.ZG'
    growth_data = df[df['indicator_code'] == growth_ind].copy()
    growth_data = growth_data.dropna(subset=['value'])

    if not growth_data.empty:
        fig, ax = plt.subplots(figsize=(14, 7))
        for country in growth_data['country_name'].unique():
            country_data = growth_data[growth_data['country_name'] == country].sort_values('year')
            color = COLORS.get(country, '#999999')
            linewidth = 3 if country == 'Oman' else 1.5
            alpha = 1.0 if country == 'Oman' else 0.7
            ax.plot(country_data['year'], country_data['value'],
                    marker='o', markersize=3, linewidth=linewidth,
                    color=color, alpha=alpha, label=country)
        ax.axhline(y=0, color='black', linewidth=0.5)
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('GDP Growth Rate (%)', fontsize=12)
        ax.set_title('GCC GDP Growth Rate Comparison', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'gcc_growth_comparison.png'), dpi=150, bbox_inches='tight')
        plt.close()
        print("\nSaved: gcc_growth_comparison.png")

    # Inflation heatmap
    inf_ind = 'FP.CPI.TOTL.ZG'
    inf_data = df[df['indicator_code'] == inf_ind].copy()

    if not inf_data.empty:
        pivot = inf_data.pivot_table(index='country_name', columns='year', values='value')

        if not pivot.empty:
            fig, ax = plt.subplots(figsize=(16, 6))
            sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn_r', center=0,
                        ax=ax, cbar_kws={'label': 'Inflation Rate (%)'})
            ax.set_title('GCC Inflation Rates (%)', fontsize=14, fontweight='bold')
            ax.set_xlabel('Year', fontsize=12)
            ax.set_ylabel('Country', fontsize=12)
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, 'gcc_inflation_heatmap.png'), dpi=150, bbox_inches='tight')
            plt.close()
            print("Saved: gcc_inflation_heatmap.png")

    # Unemployment comparison
    unemp_ind = 'SL.UEM.TOTL.ZS'
    unemp_data = df[df['indicator_code'] == unemp_ind].copy()
    unemp_data = unemp_data.dropna(subset=['value'])

    if not unemp_data.empty:
        latest_year = unemp_data['year'].max()
        unemp_latest = unemp_data[unemp_data['year'] == latest_year].sort_values('value', ascending=False)

        if not unemp_latest.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            bar_colors = [COLORS.get(c, '#999999') for c in unemp_latest['country_name']]
            bars = ax.barh(unemp_latest['country_name'], unemp_latest['value'], color=bar_colors)
            ax.set_xlabel('Unemployment Rate (%)', fontsize=12)
            ax.set_title(f'GCC Unemployment Rate ({int(latest_year)})', fontsize=14, fontweight='bold')
            for bar, value in zip(bars, unemp_latest['value']):
                if pd.notna(value):
                    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                            f'{value:.1f}%', va='center', fontsize=10)
            ax.grid(True, alpha=0.3, axis='x')
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, 'gcc_unemployment.png'), dpi=150, bbox_inches='tight')
            plt.close()
            print("Saved: gcc_unemployment.png")


def print_summary(df):
    """Print analysis summary"""
    print_header("ANALYSIS SUMMARY")

    # Oman key stats
    gdp_ind = 'NY.GDP.MKTP.CD'
    growth_ind = 'NY.GDP.MKTP.KD.ZG'

    oman_gdp = df[(df['indicator_code'] == gdp_ind) & (df['country_code'] == 'OM')]
    oman_gdp = oman_gdp.dropna(subset=['value'])

    oman_growth = df[(df['indicator_code'] == growth_ind) & (df['country_code'] == 'OM')]
    oman_growth = oman_growth.dropna(subset=['value'])

    print("\nOman Economic Highlights:")
    print("-" * 40)

    if not oman_gdp.empty:
        latest_gdp = oman_gdp.sort_values('year', ascending=False)['value'].iloc[0] / 1e9
        print(f"  GDP (latest): ${latest_gdp:.1f} Billion")

    if not oman_growth.empty:
        avg_growth = oman_growth['value'].mean()
        print(f"  Avg GDP Growth: {avg_growth:.1f}%")

    # Charts generated
    charts = [c for c in os.listdir(OUTPUT_DIR) if c.endswith('.png')]

    print(f"\nCharts Generated: {len(charts)}")
    for chart in sorted(charts):
        print(f"  - {chart}")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"\nData saved to: {os.path.join(DATA_DIR, 'raw')}")
    print(f"Charts saved to: {OUTPUT_DIR}")


def main():
    print("\n" + "=" * 60)
    print("    OMAN ECONOMIC ANALYSIS - FULL RUN")
    print("=" * 60)

    # Run all notebooks
    df = run_data_collection()

    if df is not None and not df.empty:
        run_gdp_analysis(df)
        run_trade_analysis(df)
        run_gcc_comparison(df)
        print_summary(df)
    else:
        print("\nError: No data collected. Check internet connection.")


if __name__ == "__main__":
    main()
