"""
Visualization Module for Oman Economic Analysis

This module provides functions to create professional visualizations
of economic data for reports and presentations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Tuple, Dict
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


class EconomicVisualizer:
    """
    Creates professional visualizations for economic data analysis.

    Supports:
    - Time series plots
    - Country comparisons
    - Multi-indicator dashboards
    - Correlation analysis
    """

    # Color scheme for GCC countries
    COUNTRY_COLORS = {
        'Oman': '#E41A1C',           # Red
        'Saudi Arabia': '#377EB8',    # Blue
        'United Arab Emirates': '#4DAF4A',  # Green
        'Qatar': '#984EA3',           # Purple
        'Kuwait': '#FF7F00',          # Orange
        'Bahrain': '#A65628'          # Brown
    }

    def __init__(self, output_dir: str = "outputs/charts"):
        """
        Initialize the visualizer.

        Args:
            output_dir: Directory to save charts
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def plot_time_series(
        self,
        df: pd.DataFrame,
        title: str,
        ylabel: str,
        save_name: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 6),
        show_trend: bool = True
    ) -> plt.Figure:
        """
        Create a time series plot.

        Args:
            df: DataFrame with 'year' and 'value' columns
            title: Chart title
            ylabel: Y-axis label
            save_name: Filename to save (without extension)
            figsize: Figure size
            show_trend: Whether to show trend line

        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=figsize)

        # Main line
        ax.plot(df['year'], df['value'], marker='o', linewidth=2,
                markersize=6, color='#E41A1C', label='Actual')

        # Moving average if available
        if 'ma_3' in df.columns and show_trend:
            ax.plot(df['year'], df['ma_3'], '--', linewidth=1.5,
                    color='#377EB8', alpha=0.7, label='3-Year MA')

        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')

        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        # Format x-axis
        ax.set_xticks(df['year'].unique()[::2])  # Show every other year

        plt.tight_layout()

        if save_name:
            filepath = os.path.join(self.output_dir, f"{save_name}.png")
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"Saved: {filepath}")

        return fig

    def plot_country_comparison(
        self,
        df: pd.DataFrame,
        indicator_name: str,
        year: Optional[int] = None,
        save_name: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 6)
    ) -> plt.Figure:
        """
        Create a bar chart comparing GCC countries.

        Args:
            df: DataFrame with comparison data
            indicator_name: Name of the indicator
            year: Year for comparison (shown in title)
            save_name: Filename to save
            figsize: Figure size

        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=figsize)

        colors = [self.COUNTRY_COLORS.get(c, '#999999') for c in df['country_name']]

        bars = ax.barh(df['country_name'], df['value'], color=colors)

        ax.set_xlabel(indicator_name, fontsize=12)

        title = f"GCC Comparison: {indicator_name}"
        if year:
            title += f" ({year})"
        ax.set_title(title, fontsize=14, fontweight='bold')

        # Add value labels
        for bar, value in zip(bars, df['value']):
            if pd.notna(value):
                ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                        f' {value:,.1f}', va='center', fontsize=10)

        ax.grid(True, alpha=0.3, axis='x')

        plt.tight_layout()

        if save_name:
            filepath = os.path.join(self.output_dir, f"{save_name}.png")
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"Saved: {filepath}")

        return fig

    def plot_multi_country_trend(
        self,
        df: pd.DataFrame,
        indicator_code: str,
        indicator_name: str,
        save_name: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 6)
    ) -> plt.Figure:
        """
        Plot trends for multiple countries on the same chart.

        Args:
            df: Full economic data DataFrame
            indicator_code: Indicator to plot
            indicator_name: Display name for the indicator
            save_name: Filename to save
            figsize: Figure size

        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=figsize)

        df_filtered = df[df['indicator_code'] == indicator_code].copy()

        for country in df_filtered['country_name'].unique():
            country_data = df_filtered[df_filtered['country_name'] == country]
            country_data = country_data.sort_values('year')

            color = self.COUNTRY_COLORS.get(country, '#999999')
            linewidth = 3 if country == 'Oman' else 1.5
            alpha = 1.0 if country == 'Oman' else 0.7

            ax.plot(country_data['year'], country_data['value'],
                    marker='o', markersize=4, linewidth=linewidth,
                    color=color, alpha=alpha, label=country)

        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel(indicator_name, fontsize=12)
        ax.set_title(f"{indicator_name} - GCC Comparison", fontsize=14, fontweight='bold')

        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_name:
            filepath = os.path.join(self.output_dir, f"{save_name}.png")
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"Saved: {filepath}")

        return fig

    def plot_indicator_dashboard(
        self,
        df: pd.DataFrame,
        country_code: str,
        indicators: List[Dict],
        save_name: Optional[str] = None,
        figsize: Tuple[int, int] = (14, 10)
    ) -> plt.Figure:
        """
        Create a dashboard with multiple indicators.

        Args:
            df: Economic data DataFrame
            country_code: Country to display
            indicators: List of dicts with 'code', 'name', 'ylabel'
            save_name: Filename to save
            figsize: Figure size

        Returns:
            matplotlib Figure
        """
        n_indicators = len(indicators)
        n_cols = 2
        n_rows = (n_indicators + 1) // 2

        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.flatten()

        country_name = df[df['country_code'] == country_code]['country_name'].iloc[0]

        for idx, indicator in enumerate(indicators):
            ax = axes[idx]

            data = df[
                (df['indicator_code'] == indicator['code']) &
                (df['country_code'] == country_code)
            ].sort_values('year')

            if not data.empty:
                ax.plot(data['year'], data['value'], marker='o',
                        linewidth=2, markersize=4, color='#E41A1C')

                ax.fill_between(data['year'], data['value'],
                                alpha=0.3, color='#E41A1C')

            ax.set_title(indicator['name'], fontsize=11, fontweight='bold')
            ax.set_xlabel('Year', fontsize=9)
            ax.set_ylabel(indicator.get('ylabel', ''), fontsize=9)
            ax.grid(True, alpha=0.3)

            # Rotate x-axis labels
            ax.tick_params(axis='x', rotation=45)

        # Hide unused subplots
        for idx in range(len(indicators), len(axes)):
            axes[idx].set_visible(False)

        fig.suptitle(f"{country_name} Economic Dashboard",
                     fontsize=16, fontweight='bold', y=1.02)

        plt.tight_layout()

        if save_name:
            filepath = os.path.join(self.output_dir, f"{save_name}.png")
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"Saved: {filepath}")

        return fig

    def plot_growth_comparison(
        self,
        df: pd.DataFrame,
        indicator_code: str,
        save_name: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 8)
    ) -> plt.Figure:
        """
        Create a heatmap showing growth rates by country and year.

        Args:
            df: Economic data DataFrame
            indicator_code: Indicator code
            save_name: Filename to save
            figsize: Figure size

        Returns:
            matplotlib Figure
        """
        df_filtered = df[df['indicator_code'] == indicator_code].copy()

        # Pivot for heatmap
        pivot = df_filtered.pivot_table(
            index='country_name',
            columns='year',
            values='value'
        )

        # Calculate year-over-year growth
        growth = pivot.pct_change(axis=1) * 100

        fig, ax = plt.subplots(figsize=figsize)

        sns.heatmap(growth, annot=True, fmt='.1f', cmap='RdYlGn',
                    center=0, ax=ax, cbar_kws={'label': 'Growth Rate (%)'})

        indicator_name = df_filtered['indicator_name'].iloc[0]
        ax.set_title(f"Year-over-Year Growth: {indicator_name}",
                     fontsize=14, fontweight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Country', fontsize=12)

        plt.tight_layout()

        if save_name:
            filepath = os.path.join(self.output_dir, f"{save_name}.png")
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"Saved: {filepath}")

        return fig

    def plot_pie_chart(
        self,
        df: pd.DataFrame,
        title: str,
        value_col: str = 'value',
        label_col: str = 'country_name',
        save_name: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 8)
    ) -> plt.Figure:
        """
        Create a pie chart (e.g., for GDP share).

        Args:
            df: DataFrame with values
            title: Chart title
            value_col: Column name for values
            label_col: Column name for labels
            save_name: Filename to save
            figsize: Figure size

        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=figsize)

        colors = [self.COUNTRY_COLORS.get(c, '#999999') for c in df[label_col]]

        wedges, texts, autotexts = ax.pie(
            df[value_col],
            labels=df[label_col],
            autopct='%1.1f%%',
            colors=colors,
            explode=[0.05 if c == 'Oman' else 0 for c in df[label_col]],
            shadow=True
        )

        ax.set_title(title, fontsize=14, fontweight='bold')

        plt.tight_layout()

        if save_name:
            filepath = os.path.join(self.output_dir, f"{save_name}.png")
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            print(f"Saved: {filepath}")

        return fig


def main():
    """Demonstrate visualization capabilities."""
    print("=" * 60)
    print("Oman Economic Visualizer")
    print("=" * 60)
    print("\nThis module provides visualization functions.")
    print("Import and use with your data:")
    print("  from src.visualizations import EconomicVisualizer")
    print("  viz = EconomicVisualizer()")
    print("  viz.plot_time_series(df, 'GDP Growth', '%')")


if __name__ == "__main__":
    main()
