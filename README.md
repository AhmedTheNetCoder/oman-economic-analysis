# Oman Economic Data Analysis

A comprehensive economic analysis of Oman using World Bank data, with comparisons to other GCC countries. This project demonstrates Python data analysis skills with real-world economic data.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview

This project analyzes Oman's economic performance across multiple dimensions:
- GDP and economic growth trends
- Trade and export patterns
- Employment and labor market
- Inflation and price stability
- Regional comparison with GCC countries

### Why This Matters for GCC

Understanding Oman's economic position is crucial for:
- Business investment decisions
- Policy analysis
- Regional economic planning
- Career opportunities in data analytics

## Project Structure

```
oman-economic-analysis/
├── README.md
├── requirements.txt
├── LICENSE
├── data/
│   ├── raw/              # Downloaded World Bank data
│   └── processed/        # Cleaned and transformed data
├── notebooks/
│   ├── 01_data_collection.ipynb    # Data fetching from World Bank API
│   ├── 02_gdp_analysis.ipynb       # GDP and growth analysis
│   ├── 03_trade_analysis.ipynb     # Trade and exports
│   └── 04_gcc_comparison.ipynb     # Regional comparison
├── src/
│   ├── __init__.py
│   ├── data_collector.py    # World Bank API wrapper
│   ├── data_processor.py    # Data cleaning utilities
│   └── visualizations.py    # Chart generation
├── outputs/
│   └── charts/              # Generated visualizations
└── reports/
    └── key_findings.md      # Analysis summary
```

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/oman-economic-analysis.git
cd oman-economic-analysis
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the analysis

```bash
# Start with data collection
jupyter notebook notebooks/01_data_collection.ipynb
```

Or run the data collector directly:

```bash
python -m src.data_collector
```

## Key Findings

### Oman's Economic Profile

| Metric | Value | GCC Rank |
|--------|-------|----------|
| GDP | ~$85B | 6th |
| GDP per Capita | ~$19,000 | 4th-5th |
| GDP Growth (avg) | 3-4% | Variable |
| Oil Dependency | 25-40% of GDP | Moderate |

### Notable Insights

1. **Oil Dependency**: Oman's economy remains significantly tied to oil prices, though diversification efforts are ongoing through Vision 2040.

2. **GCC Position**: While Oman has the smallest economy in the GCC, it maintains competitive GDP per capita above Bahrain.

3. **Growth Volatility**: GDP growth shows strong correlation with global oil prices, with notable contractions in 2015-2016 and 2020.

4. **Diversification Progress**: Non-oil sectors including tourism, logistics, and manufacturing are growing.

## Data Sources

This project uses the **World Bank Open Data API**, which provides free access to:
- GDP and growth indicators
- Trade statistics
- Employment data
- Inflation metrics
- Population statistics

API Documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

## Countries Analyzed

| Country | Code | Region |
|---------|------|--------|
| Oman | OMN | GCC |
| Saudi Arabia | SAU | GCC |
| United Arab Emirates | ARE | GCC |
| Qatar | QAT | GCC |
| Kuwait | KWT | GCC |
| Bahrain | BHR | GCC |

## Economic Indicators

The analysis covers 20+ World Bank indicators:

### GDP & Growth
- `NY.GDP.MKTP.CD` - GDP (current US$)
- `NY.GDP.MKTP.KD.ZG` - GDP growth (annual %)
- `NY.GDP.PCAP.CD` - GDP per capita

### Trade
- `NE.EXP.GNFS.ZS` - Exports (% of GDP)
- `NE.IMP.GNFS.ZS` - Imports (% of GDP)
- `BN.CAB.XOKA.CD` - Current account balance

### Employment
- `SL.UEM.TOTL.ZS` - Unemployment rate
- `SL.TLF.TOTL.IN` - Labor force

### Other
- `FP.CPI.TOTL.ZG` - Inflation rate
- `NY.GDP.PETR.RT.ZS` - Oil rents (% of GDP)

## Sample Visualizations

The project generates various charts including:
- GDP trend analysis
- GCC comparison bar charts
- Trade balance over time
- Oil dependency trends
- Inflation heatmaps

## Technologies Used

- **Python 3.10+**
- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **matplotlib** - Static visualizations
- **seaborn** - Statistical plots
- **requests** - API calls
- **jupyter** - Interactive notebooks

## Usage Examples

### Fetch Oman Data

```python
from src.data_collector import OmanDataCollector

collector = OmanDataCollector()
df = collector.fetch_oman_data(start_year=2000, end_year=2023)
print(df.head())
```

### Create Visualizations

```python
from src.visualizations import EconomicVisualizer

viz = EconomicVisualizer()
viz.plot_time_series(gdp_data, title='Oman GDP Trend', ylabel='Billion USD')
```

### Process Data

```python
from src.data_processor import DataProcessor

processor = DataProcessor()
df = processor.load_data('gcc_economic_data.csv')
latest = processor.get_latest_values(df, 'OMN')
```

## Future Enhancements

- [ ] Add interactive Plotly dashboards
- [ ] Include more GCC-specific data sources
- [ ] Add forecasting models
- [ ] Create Streamlit web app
- [ ] Add sector-specific analysis (tourism, logistics)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created as part of a Data Analytics portfolio project focused on GCC economic analysis.

## Acknowledgments

- World Bank for providing open access to economic data
- Oman Vision 2040 documentation for strategic context
- GCC statistical agencies for regional data

---

**Star this repository** if you find it useful for understanding GCC economics!
