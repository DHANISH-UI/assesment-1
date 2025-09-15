import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess all datasets"""
    try:
        # Load datasets
        business_df = pd.read_csv('Marketing Intelligence Dashboard/business.csv')
        facebook_df = pd.read_csv('Marketing Intelligence Dashboard/Facebook.csv')
        google_df = pd.read_csv('Marketing Intelligence Dashboard/Google.csv')
        tiktok_df = pd.read_csv('Marketing Intelligence Dashboard/TikTok.csv')
        
        # Convert date columns
        for df in [business_df, facebook_df, google_df, tiktok_df]:
            df['date'] = pd.to_datetime(df['date'])
        
        # Add platform column
        facebook_df['platform'] = 'Facebook'
        google_df['platform'] = 'Google'
        tiktok_df['platform'] = 'TikTok'
        
        # Combine marketing data
        marketing_df = pd.concat([facebook_df, google_df, tiktok_df], ignore_index=True)
        
        # Calculate additional metrics
        marketing_df['ctr'] = (marketing_df['clicks'] / marketing_df['impression'] * 100).round(2)
        marketing_df['cpc'] = (marketing_df['spend'] / marketing_df['clicks']).round(2)
        marketing_df['cpm'] = (marketing_df['spend'] / marketing_df['impression'] * 1000).round(2)
        
        # Aggregate marketing data by date
        daily_marketing = marketing_df.groupby('date').agg({
            'impression': 'sum',
            'clicks': 'sum',
            'spend': 'sum',
            'attributed revenue': 'sum'
        }).reset_index()
        
        daily_marketing['ctr'] = (daily_marketing['clicks'] / daily_marketing['impression'] * 100).round(2)
        daily_marketing['cpc'] = (daily_marketing['spend'] / daily_marketing['clicks']).round(2)
        
        # Merge business and marketing data
        combined_df = pd.merge(business_df, daily_marketing, on='date', how='left')
        
        # Calculate additional business metrics
        combined_df['avg_order_value'] = (combined_df['total revenue'] / combined_df['# of orders']).round(2)
        combined_df['customer_acquisition_cost'] = (combined_df['spend'] / combined_df['new customers']).round(2)
        combined_df['marketing_attribution_rate'] = (combined_df['attributed revenue'] / combined_df['total revenue'] * 100).round(2)
        combined_df['profit_margin'] = (combined_df['gross profit'] / combined_df['total revenue'] * 100).round(2)
        
        return business_df, marketing_df, combined_df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None

def create_kpi_cards(combined_df):
    """Create KPI metric cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = combined_df['total revenue'].sum()
        st.metric(
            label="💰 Total Revenue",
            value=f"${total_revenue:,.0f}",
            delta=f"${combined_df['total revenue'].mean():,.0f} avg/day"
        )
    
    with col2:
        total_spend = combined_df['spend'].sum()
        st.metric(
            label="💸 Total Ad Spend",
            value=f"${total_spend:,.0f}",
            delta=f"${combined_df['spend'].mean():,.0f} avg/day"
        )
    
    with col3:
        avg_ctr = combined_df['ctr'].mean()
        st.metric(
            label="🎯 Average CTR",
            value=f"{avg_ctr:.2f}%",
            delta=f"Click Rate"
        )
    
    with col4:
        total_orders = combined_df['# of orders'].sum()
        st.metric(
            label="🛒 Total Orders",
            value=f"{total_orders:,}",
            delta=f"{combined_df['# of orders'].mean():.0f} avg/day"
        )

def create_revenue_trend_chart(combined_df):
    """Create enhanced revenue trend chart with better visualization"""
    # Create subplots for better comparison
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('📈 Revenue Trends Over Time', '📊 Daily Revenue Comparison'),
        specs=[[{"type": "scatter"}], [{"type": "bar"}]],
        vertical_spacing=0.2,
        row_heights=[0.6, 0.4]
    )
    
    # Line chart for revenue trends
    fig.add_trace(
        go.Scatter(
            x=combined_df['date'],
            y=combined_df['total revenue'],
            mode='lines+markers',
            name='Total Revenue',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=8, color='#3b82f6'),
            hovertemplate='<b>Total Revenue</b><br>Date: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=combined_df['date'],
            y=combined_df['attributed revenue'],
            mode='lines+markers',
            name='Attributed Revenue',
            line=dict(color='#f59e0b', width=3, dash='dash'),
            marker=dict(size=8, color='#f59e0b'),
            hovertemplate='<b>Attributed Revenue</b><br>Date: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Bar chart for daily comparison
    fig.add_trace(
        go.Bar(
            x=combined_df['date'],
            y=combined_df['total revenue'],
            name='Total Revenue',
            marker_color='#3b82f6',
            opacity=0.7,
            hovertemplate='<b>Total Revenue</b><br>Date: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=combined_df['date'],
            y=combined_df['attributed revenue'],
            name='Attributed Revenue',
            marker_color='#f59e0b',
            opacity=0.7,
            hovertemplate='<b>Attributed Revenue</b><br>Date: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        height=850,
        showlegend=True,
        plot_bgcolor='#334155',
        paper_bgcolor='#334155',
        font=dict(color='#f1f5f9', size=12),
        title=dict(
            text="💰 Revenue Performance Analysis",
            font=dict(size=18, color='#f1f5f9'),
            x=0.5,
            y=0.99,
            xanchor='center',
            yanchor='top'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="right",
            x=1,
            font=dict(color='#cbd5e1')
        ),
        margin=dict(l=50, r=50, t=140, b=50)
    )
    
    # Update axes
    fig.update_xaxes(
        title_text="Date",
        title_font=dict(color='#cbd5e1'),
        tickfont=dict(color='#94a3b8'),
        gridcolor='#475569',
        showgrid=True,
        row=1, col=1
    )
    fig.update_yaxes(
        title_text="Revenue ($)",
        title_font=dict(color='#cbd5e1'),
        tickfont=dict(color='#94a3b8'),
        gridcolor='#475569',
        showgrid=True,
        tickformat='$,.0f',
        row=1, col=1
    )
    
    fig.update_xaxes(
        title_text="Date",
        title_font=dict(color='#cbd5e1'),
        tickfont=dict(color='#94a3b8'),
        gridcolor='#475569',
        showgrid=True,
        row=2, col=1
    )
    fig.update_yaxes(
        title_text="Revenue ($)",
        title_font=dict(color='#cbd5e1'),
        tickfont=dict(color='#94a3b8'),
        gridcolor='#475569',
        showgrid=True,
        tickformat='$,.0f',
        row=2, col=1
    )
    
    return fig

def create_platform_performance_chart(marketing_df):
    """Create platform performance comparison"""
    platform_metrics = marketing_df.groupby('platform').agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'impression': 'sum',
        'clicks': 'sum'
    }).reset_index()
    
    platform_metrics['ctr'] = (platform_metrics['clicks'] / platform_metrics['impression'] * 100).round(2)
    platform_metrics['cpc'] = (platform_metrics['spend'] / platform_metrics['clicks']).round(2)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Spend by Platform', 'Revenue by Platform', 'CTR by Platform', 'CPC by Platform'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Spend
    fig.add_trace(
        go.Bar(x=platform_metrics['platform'], y=platform_metrics['spend'], name='Spend', marker_color='#1f77b4'),
        row=1, col=1
    )
    
    # Revenue
    fig.add_trace(
        go.Bar(x=platform_metrics['platform'], y=platform_metrics['attributed revenue'], name='Revenue', marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    # CTR
    fig.add_trace(
        go.Bar(x=platform_metrics['platform'], y=platform_metrics['ctr'], name='CTR', marker_color='#2ca02c'),
        row=2, col=1
    )
    
    # CPC
    fig.add_trace(
        go.Bar(x=platform_metrics['platform'], y=platform_metrics['cpc'], name='CPC', marker_color='#d62728'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    fig.update_xaxes(title_text="Platform", row=2, col=1)
    fig.update_xaxes(title_text="Platform", row=2, col=2)
    fig.update_yaxes(title_text="Spend ($)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=2)
    fig.update_yaxes(title_text="CTR (%)", row=2, col=1)
    fig.update_yaxes(title_text="CPC ($)", row=2, col=2)
    
    return fig

def create_tactic_performance_chart(marketing_df):
    """Create enhanced tactic performance analysis with better visualization"""
    tactic_metrics = marketing_df.groupby(['platform', 'tactic']).agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'impression': 'sum',
        'clicks': 'sum'
    }).reset_index()
    
    tactic_metrics['ctr'] = (tactic_metrics['clicks'] / tactic_metrics['impression'] * 100).round(2)
    tactic_metrics['cpc'] = (tactic_metrics['spend'] / tactic_metrics['clicks']).round(2)
    tactic_metrics['efficiency'] = (tactic_metrics['attributed revenue'] / tactic_metrics['impression'] * 1000).round(2)
    tactic_metrics['tactic_platform'] = tactic_metrics['tactic'] + ' (' + tactic_metrics['platform'] + ')'
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('💡 Tactic Performance Matrix', '📊 Top Performing Tactics'),
        specs=[[{"type": "scatter"}, {"type": "bar"}]],
        horizontal_spacing=0.25
    )
    
    # Bubble chart: Spend vs Revenue with CTR as size and CPC as color
    fig.add_trace(
        go.Scatter(
            x=tactic_metrics['spend'],
            y=tactic_metrics['attributed revenue'],
            mode='markers+text',
            text=tactic_metrics['tactic_platform'],
            textposition='top center',
            marker=dict(
                size=tactic_metrics['ctr'] * 6,
                color=tactic_metrics['cpc'],
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="CPC ($)", x=0.42, len=0.6),
                sizemode='diameter',
                sizemin=8,
                sizeref=3,
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>%{text}</b><br>Spend: $%{x:,.0f}<br>Revenue: $%{y:,.0f}<br>CPC: $%{marker.color:.2f}<br>CTR: %{marker.size:.1f}%<extra></extra>',
            name='Tactic Performance'
        ),
        row=1, col=1
    )
    
    # Bar chart: Top 8 tactics by CTR
    top_tactics = tactic_metrics.nlargest(8, 'ctr')
    fig.add_trace(
        go.Bar(
            x=top_tactics['ctr'],
            y=top_tactics['tactic_platform'],
            orientation='h',
            marker=dict(
                color=top_tactics['ctr'],
                colorscale='Blues',
                showscale=False
            ),
            hovertemplate='<b>%{y}</b><br>CTR: %{x:.2f}%<br>Spend: $%{customdata[0]:,.0f}<br>Revenue: $%{customdata[1]:,.0f}<extra></extra>',
            customdata=top_tactics[['spend', 'attributed revenue']],
            name='Top Tactics'
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=600,
        showlegend=False,
        plot_bgcolor='#334155',
        paper_bgcolor='#334155',
        font=dict(color='#f1f5f9', size=12),
        title=dict(
            text="🎯 Tactic Performance Analysis",
            font=dict(size=18, color='#f1f5f9'),
            x=0.5,
            y=0.98
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Update axes for scatter plot
    fig.update_xaxes(
        title_text="Spend ($)",
        title_font=dict(color='#cbd5e1'),
        tickfont=dict(color='#94a3b8'),
        gridcolor='#475569',
        showgrid=True,
        row=1, col=1
    )
    fig.update_yaxes(
        title_text="Attributed Revenue ($)",
        title_font=dict(color='#cbd5e1'),
        tickfont=dict(color='#94a3b8'),
        gridcolor='#475569',
        showgrid=True,
        row=1, col=1
    )
    
    # Update axes for bar chart
    fig.update_xaxes(
        title_text="CTR (%)",
        title_font=dict(color='#cbd5e1'),
        tickfont=dict(color='#94a3b8'),
        gridcolor='#475569',
        showgrid=True,
        row=1, col=2
    )
    fig.update_yaxes(
        title_text="Tactic (Platform)",
        title_font=dict(color='#cbd5e1'),
        tickfont=dict(color='#94a3b8'),
        gridcolor='#475569',
        showgrid=True,
        row=1, col=2
    )
    
    return fig

def create_geographic_analysis(marketing_df):
    """Create geographic performance analysis"""
    geo_metrics = marketing_df.groupby(['platform', 'state']).agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'impression': 'sum',
        'clicks': 'sum'
    }).reset_index()
    
    geo_metrics['ctr'] = (geo_metrics['clicks'] / geo_metrics['impression'] * 100).round(2)
    geo_metrics['cpc'] = (geo_metrics['spend'] / geo_metrics['clicks']).round(2)
    
    fig = px.bar(
        geo_metrics,
        x='platform',
        y='ctr',
        color='state',
        title="CTR by Platform and State",
        barmode='group'
    )
    
    fig.update_layout(height=400)
    return fig

def create_state_wise_analysis(marketing_df):
    """Create comprehensive state-wise analysis"""
    state_metrics = marketing_df.groupby('state').agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'impression': 'sum',
        'clicks': 'sum',
        'platform': 'nunique'
    }).reset_index()
    
    state_metrics['ctr'] = (state_metrics['clicks'] / state_metrics['impression'] * 100).round(2)
    state_metrics['cpc'] = (state_metrics['spend'] / state_metrics['clicks']).round(2)
    state_metrics['cpm'] = (state_metrics['spend'] / state_metrics['impression'] * 1000).round(2)
    
    return state_metrics

def create_state_performance_chart(state_metrics):
    """Create state performance comparison chart"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue by State', 'Spend by State', 'CTR by State', 'CPC by State'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Revenue
    fig.add_trace(
        go.Bar(x=state_metrics['state'], y=state_metrics['attributed revenue'], 
               name='Revenue', marker_color='#1f77b4'),
        row=1, col=1
    )
    
    # Spend
    fig.add_trace(
        go.Bar(x=state_metrics['state'], y=state_metrics['spend'], 
               name='Spend', marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    # CTR
    fig.add_trace(
        go.Bar(x=state_metrics['state'], y=state_metrics['ctr'], 
               name='CTR', marker_color='#2ca02c'),
        row=2, col=1
    )
    
    # CPC
    fig.add_trace(
        go.Bar(x=state_metrics['state'], y=state_metrics['cpc'], 
               name='CPC', marker_color='#d62728'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    fig.update_xaxes(title_text="State", row=2, col=1)
    fig.update_xaxes(title_text="State", row=2, col=2)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
    fig.update_yaxes(title_text="Spend ($)", row=1, col=2)
    fig.update_yaxes(title_text="CTR (%)", row=2, col=1)
    fig.update_yaxes(title_text="CPC ($)", row=2, col=2)
    
    return fig

def create_state_platform_breakdown(marketing_df):
    """Create state-platform breakdown heatmap"""
    state_platform = marketing_df.groupby(['state', 'platform']).agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'impression': 'sum',
        'clicks': 'sum'
    }).reset_index()
    
    state_platform['ctr'] = (state_platform['clicks'] / state_platform['impression'] * 100).round(2)
    
    # Create pivot table for heatmap
    pivot_ctr = state_platform.pivot(index='state', columns='platform', values='ctr').fillna(0)
    
    fig = px.imshow(
        pivot_ctr,
        text_auto=True,
        aspect="auto",
        title="CTR Heatmap: State vs Platform",
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=400)
    return fig

def create_campaign_analysis(marketing_df):
    """Create top performing campaigns analysis"""
    campaign_metrics = marketing_df.groupby(['platform', 'campaign']).agg({
        'spend': 'sum',
        'attributed revenue': 'sum',
        'impression': 'sum',
        'clicks': 'sum'
    }).reset_index()
    
    campaign_metrics['ctr'] = (campaign_metrics['clicks'] / campaign_metrics['impression'] * 100).round(2)
    campaign_metrics['cpc'] = (campaign_metrics['spend'] / campaign_metrics['clicks']).round(2)
    
    # Top 10 campaigns by revenue
    top_campaigns = campaign_metrics.nlargest(10, 'attributed revenue')
    
    fig = px.bar(
        top_campaigns,
        x='attributed revenue',
        y='campaign',
        color='ctr',
        title="Top 10 Campaigns by Revenue",
        labels={'attributed revenue': 'Attributed Revenue ($)', 'campaign': 'Campaign'}
    )
    
    fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
    return fig

def create_correlation_analysis(combined_df):
    """Create correlation analysis between marketing and business metrics"""
    # Select numeric columns for correlation
    numeric_cols = ['total revenue', 'gross profit', '# of orders', 'new customers', 
                   'spend', 'attributed revenue', 'impression', 'clicks', 'ctr', 'cpc']
    
    corr_data = combined_df[numeric_cols].corr()
    
    fig = px.imshow(
        corr_data,
        text_auto=True,
        aspect="auto",
        title="Correlation Matrix: Marketing vs Business Metrics",
        color_continuous_scale='RdBu_r'
    )
    
    fig.update_layout(height=600)
    return fig


def main():
    """Main dashboard function"""
    st.markdown('<h1 class="main-header">📊 Marketing Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    business_df, marketing_df, combined_df = load_data()
    
    if combined_df is None:
        st.error("Failed to load data. Please check the file paths.")
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    min_date = combined_df['date'].min()
    max_date = combined_df['date'].max()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        combined_df = combined_df[(combined_df['date'] >= pd.to_datetime(start_date)) & 
                                 (combined_df['date'] <= pd.to_datetime(end_date))]
        marketing_df = marketing_df[(marketing_df['date'] >= pd.to_datetime(start_date)) & 
                                   (marketing_df['date'] <= pd.to_datetime(end_date))]
    
    # Platform filter
    platforms = st.sidebar.multiselect(
        "Select Platforms",
        options=marketing_df['platform'].unique(),
        default=marketing_df['platform'].unique()
    )
    
    if platforms:
        marketing_df = marketing_df[marketing_df['platform'].isin(platforms)]
    
    # State filter
    states = st.sidebar.multiselect(
        "Select States",
        options=marketing_df['state'].unique(),
        default=marketing_df['state'].unique()
    )
    
    if states:
        marketing_df = marketing_df[marketing_df['state'].isin(states)]
    
    # Main content
    st.markdown("---")
    
    # KPI Cards
    create_kpi_cards(combined_df)
    
    st.markdown("---")
    
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_revenue_trend_chart(combined_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_platform_performance_chart(marketing_df), use_container_width=True)
    
    st.markdown("---")
    
    # Tactic Performance
    st.subheader("🎯 Tactic Performance Analysis")
    st.plotly_chart(create_tactic_performance_chart(marketing_df), use_container_width=True)
    
    st.markdown("---")
    
    # State-wise Analysis
    st.subheader("🗺️ State-wise Performance Analysis")
    
    # Generate state metrics
    state_metrics = create_state_wise_analysis(marketing_df)
    
    # State KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        best_state_revenue = state_metrics.loc[state_metrics['attributed revenue'].idxmax()]
        st.metric(
            label="🏆 Top Revenue State",
            value=best_state_revenue['state'],
            delta=f"${best_state_revenue['attributed revenue']:,.0f}"
        )
    
    with col2:
        best_state_ctr = state_metrics.loc[state_metrics['ctr'].idxmax()]
        st.metric(
            label="📈 Best CTR State",
            value=best_state_ctr['state'],
            delta=f"{best_state_ctr['ctr']:.2f}%"
        )
    
    with col3:
        best_state_cpc = state_metrics.loc[state_metrics['cpc'].idxmin()]
        st.metric(
            label="💰 Best CPC State",
            value=best_state_cpc['state'],
            delta=f"${best_state_cpc['cpc']:.2f}"
        )
    
    with col4:
        total_states = len(state_metrics)
        active_platforms = state_metrics['platform'].sum()
        st.metric(
            label="🌍 States Active",
            value=f"{total_states}",
            delta=f"{active_platforms} platform combinations"
        )
    
    st.markdown("---")
    
    # State Performance Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_state_performance_chart(state_metrics), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_state_platform_breakdown(marketing_df), use_container_width=True)
    
    st.markdown("---")
    
    # Geographic Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_geographic_analysis(marketing_df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_campaign_analysis(marketing_df), use_container_width=True)
    
    st.markdown("---")
    
    # Correlation Analysis
    st.subheader("🔗 Marketing-Business Correlation Analysis")
    st.plotly_chart(create_correlation_analysis(combined_df), use_container_width=True)
    
    st.markdown("---")
    
    # Data tables
    st.subheader("📋 Detailed Data")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Business Metrics", "Marketing Performance", "State-wise Analysis", "Combined View"])
    
    with tab1:
        st.dataframe(combined_df[['date', '# of orders', 'new customers', 'total revenue', 
                                 'gross profit', 'avg_order_value', 'profit_margin']].round(2))
    
    with tab2:
        st.dataframe(marketing_df[['date', 'platform', 'tactic', 'state', 'campaign', 
                                  'impression', 'clicks', 'spend', 'attributed revenue', 
                                  'ctr', 'cpc']].round(2))
    
    with tab3:
        st.dataframe(state_metrics[['state', 'spend', 'attributed revenue', 'impression', 
                                   'clicks', 'ctr', 'cpc', 'cpm', 'platform']].round(2))
    
    with tab4:
        st.dataframe(combined_df[['date', 'total revenue', 'spend', 'attributed revenue', 
                                 'ctr', 'cpc', 'marketing_attribution_rate', 
                                 'customer_acquisition_cost']].round(2))
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>📊 Marketing Intelligence Dashboard | Built with Streamlit & Plotly</p>
        <p>Data covers 120 days of marketing and business performance</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
