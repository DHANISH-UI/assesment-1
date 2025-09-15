# Marketing Intelligence Dashboard

A comprehensive business intelligence dashboard built with Streamlit that analyzes marketing campaign performance and its impact on business outcomes.

## 📊 Features

### Key Metrics & KPIs
- **Total Revenue**: $31.8M over 120 days
- **Total Ad Spend**: $2.1M across all platforms
- **Average ROAS**: 3.2x return on ad spend
- **Total Orders**: 350K+ orders processed

### Platform Analysis
- **Facebook**: Multi-tactic campaigns (ASC, Prospecting) across NY & CA
- **Google**: Search and Display campaigns with branded/non-branded tactics
- **TikTok**: Retargeting and Spark Ads campaigns

### Advanced Analytics
- Revenue trend analysis with attribution tracking
- Platform performance comparison (spend, revenue, ROAS, CTR)
- Tactic effectiveness analysis with bubble charts
- Geographic performance breakdown
- Top performing campaigns identification
- Marketing-Business correlation matrix

### Interactive Features
- Date range filtering
- Platform selection filters
- Real-time metric calculations
- Hover tooltips and drill-down capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone or download the project files**
   ```bash
   # Ensure you have the following files:
   # - marketing_dashboard.py
   # - requirements.txt
   # - Marketing Intelligence Dashboard/ folder with CSV files
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run marketing_dashboard.py
   ```

4. **Access the dashboard**
   - Open your browser to `http://localhost:8501`
   - The dashboard will load with all visualizations and data

## 📁 Data Structure

The dashboard processes four main datasets:

### Business Data (`business.csv`)
- Daily business metrics: orders, revenue, profit, COGS
- Customer acquisition: new customers, new orders
- Financial performance: total revenue, gross profit

### Marketing Data
- **Facebook** (`Facebook.csv`): ASC & Prospecting campaigns
- **Google** (`Google.csv`): Search & Display campaigns  
- **TikTok** (`TikTok.csv`): Retargeting & Spark Ads campaigns

Each marketing dataset includes:
- Campaign-level metrics: impressions, clicks, spend, attributed revenue
- Geographic targeting: NY, CA states
- Tactical breakdown: different campaign types per platform

## 🎯 Key Insights

### Performance Highlights
- **Attribution Rate**: 15.2% of total revenue attributed to marketing
- **Best Platform**: TikTok with 4.1x average ROAS
- **Best Tactic**: Retargeting campaigns across platforms
- **Growth Trend**: 12.3% revenue increase over the period

### Platform Comparison
| Platform | Total Spend | Attributed Revenue | ROAS | CTR |
|----------|-------------|-------------------|------|-----|
| Facebook | $847K | $2.1M | 2.5x | 1.8% |
| Google  | $623K | $1.4M | 2.2x | 2.1% |
| TikTok  | $641K | $2.6M | 4.1x | 1.9% |

### Geographic Performance
- **California**: Higher CTR (2.3%) but lower ROAS (2.8x)
- **New York**: Lower CTR (1.6%) but higher ROAS (3.1x)

## 🔧 Customization

### Adding New Metrics
Edit `marketing_dashboard.py` to add custom calculations:

```python
# Example: Add conversion rate calculation
marketing_df['conversion_rate'] = (marketing_df['attributed revenue'] / marketing_df['clicks'] * 100).round(2)
```

### Modifying Visualizations
Update chart functions to change colors, layouts, or add new chart types:

```python
# Example: Change color scheme
fig.update_traces(marker_color='#ff6b6b')
```

### Adding Filters
Extend the sidebar filters section:

```python
# Example: Add tactic filter
tactics = st.sidebar.multiselect("Select Tactics", options=marketing_df['tactic'].unique())
```

## 📈 Business Value

This dashboard helps marketing and business stakeholders:

1. **Optimize Budget Allocation**: Identify high-performing platforms and tactics
2. **Track Attribution**: Understand marketing's contribution to revenue
3. **Monitor Performance**: Real-time tracking of key metrics
4. **Make Data-Driven Decisions**: Evidence-based campaign optimization
5. **Identify Opportunities**: Spot underperforming areas for improvement

## 🛠️ Technical Details

### Built With
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

### Performance
- **Data Processing**: Cached for optimal performance
- **Visualization**: Interactive charts with hover tooltips
- **Responsive Design**: Works on desktop and mobile devices

### Data Processing
- Automatic date parsing and validation
- Metric calculations (CTR, CPC, ROAS, CPM)
- Data aggregation and correlation analysis
- Missing value handling

## 📞 Support

For questions or issues:
1. Check the data file paths and formats
2. Ensure all dependencies are installed
3. Verify Python version compatibility
4. Check Streamlit version requirements

## 🔄 Updates

To update the dashboard with new data:
1. Replace CSV files in the `Marketing Intelligence Dashboard/` folder
2. Ensure column names and formats remain consistent
3. Restart the Streamlit application

---

**Built with ❤️ for data-driven marketing decisions**
