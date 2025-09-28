import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from io import StringIO

# Page configuration
st.set_page_config(
    page_title="US Companies Revenue Scraper",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def scrape_companies_data():
    """Scrape the largest US companies data from Wikipedia"""
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
        
        # Make request with headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main table (usually the second table on the page)
        tables = soup.find_all('table', class_='wikitable sortable')
        if not tables:
            st.error("Could not find the data table on Wikipedia")
            return None
            
        table = tables[0]  # First wikitable sortable is usually the main one
        
        # Extract headers
        headers = []
        header_row = table.find('tr')
        for th in header_row.find_all('th'):
            header_text = th.get_text(strip=True)
            # Clean up header text
            header_text = re.sub(r'\s+', ' ', header_text)
            header_text = header_text.replace('(USD millions)', '(USD millions)')
            headers.append(header_text)
        
        # Extract data rows
        rows = []
        for tr in table.find_all('tr')[1:]:  # Skip header row
            row = []
            for td in tr.find_all(['td', 'th']):
                cell_text = td.get_text(strip=True)
                # Clean up cell text
                cell_text = re.sub(r'\s+', ' ', cell_text)
                # Remove citation markers like [1], [2], etc.
                cell_text = re.sub(r'\[\d+\]', '', cell_text)
                row.append(cell_text)
            
            if len(row) == len(headers):  # Only add complete rows
                rows.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers)
        
        # Clean up all columns - more robust cleaning
        for col in df.columns:
            if 'revenue' in col.lower() or 'usd' in col.lower():
                # Clean revenue column
                df[col] = df[col].astype(str)
                df[col] = df[col].str.replace(',', '')
                df[col] = df[col].str.replace('$', '')
                df[col] = df[col].str.replace(' ', '')
                # Extract only numbers (remove any text)
                df[col] = df[col].str.extract(r'(\d+\.?\d*)', expand=False)
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            elif 'employee' in col.lower():
                # Clean employees column
                df[col] = df[col].astype(str)
                df[col] = df[col].str.replace(',', '')
                df[col] = df[col].str.replace(' ', '')
                # Extract only numbers
                df[col] = df[col].str.extract(r'(\d+)', expand=False)
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
        
    except Exception as e:
        st.error(f"Error scraping data: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🏢 US Companies Revenue Scraper</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    This app scrapes real-time data of the **largest U.S. companies by revenue** from Wikipedia 
    and presents it in an interactive format. The data includes company rankings, revenue figures, 
    employee counts, and headquarters locations.
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Controls")
        
        if st.button("🔄 Refresh Data", type="primary"):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📋 Features")
        st.markdown("""
        - **Real-time data** from Wikipedia
        - **Interactive filtering** and sorting
        - **Data visualization** charts
        - **CSV export** functionality
        - **Responsive design** for all devices
        """)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        Data source: [Wikipedia - List of largest companies in the United States by revenue](https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue)
        
        Built with Python, Streamlit, BeautifulSoup, and Pandas.
        """)
    
    # Main content
    with st.spinner("🔍 Scraping latest data from Wikipedia..."):
        df = scrape_companies_data()
    
    if df is not None and not df.empty:
        st.success(f"✅ Successfully scraped data for {len(df)} companies!")
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Companies", len(df))
        
        with col2:
            if 'Revenue (USD millions)' in df.columns:
                total_revenue = df['Revenue (USD millions)'].sum()
                st.metric("Total Revenue", f"${total_revenue:,.0f}M")
        
        with col3:
            if 'Employees' in df.columns:
                total_employees = df['Employees'].sum()
                st.metric("Total Employees", f"{total_employees:,.0f}")
        
        with col4:
            if 'Industry' in df.columns:
                unique_industries = df['Industry'].nunique()
                st.metric("Industries", unique_industries)
        
        # Filters
        st.markdown("---")
        st.subheader("🔍 Filter Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Industry' in df.columns:
                industries = ['All'] + sorted(df['Industry'].dropna().unique().tolist())
                selected_industry = st.selectbox("Select Industry", industries)
        
        with col2:
            if 'Revenue (USD millions)' in df.columns:
                min_revenue = st.number_input(
                    "Minimum Revenue (USD millions)", 
                    min_value=0, 
                    value=0, 
                    step=1000
                )
        
        # Apply filters
        filtered_df = df.copy()
        
        if 'Industry' in df.columns and selected_industry != 'All':
            filtered_df = filtered_df[filtered_df['Industry'] == selected_industry]
        
        if 'Revenue (USD millions)' in df.columns:
            filtered_df = filtered_df[filtered_df['Revenue (USD millions)'] >= min_revenue]
        
        # Debug section (can be removed later)
        with st.expander("🔍 Debug Info - Data Structure"):
            st.write("**DataFrame Shape:**", filtered_df.shape)
            st.write("**Column Names:**", list(filtered_df.columns))
            st.write("**First few rows:**")
            st.dataframe(filtered_df.head(3))
            st.write("**Data Types:**")
            st.write(filtered_df.dtypes)
        
        # Display filtered data
        st.markdown("---")
        st.subheader("📈 Company Data")
        
        # Display dataframe with better formatting
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Revenue (USD millions)": st.column_config.NumberColumn(
                    "Revenue (USD millions)",
                    format="$%d M"
                ),
                "Employees": st.column_config.NumberColumn(
                    "Employees",
                    format="%d"
                )
            }
        )
        
        # Charts
        if len(filtered_df) > 0:
            st.markdown("---")
            st.subheader("📊 Data Visualizations")
            
            tab1, tab2, tab3 = st.tabs(["Top Companies by Revenue", "Industry Distribution", "Employee Count"])
            
            with tab1:
                # Find revenue and name columns
                revenue_col = None
                name_col = None
                
                # Find revenue column
                for col in filtered_df.columns:
                    if 'revenue' in col.lower() or 'usd' in col.lower():
                        revenue_col = col
                        break
                
                # Find name column
                for col in filtered_df.columns:
                    if 'name' in col.lower() or 'company' in col.lower():
                        name_col = col
                        break
                
                # Debug information
                st.write(f"**Found columns:** Revenue: `{revenue_col}`, Name: `{name_col}`")
                
                if revenue_col and name_col:
                    # Show sample data before processing
                    st.write("**Sample revenue data:**")
                    st.write(filtered_df[revenue_col].head(5).tolist())
                    
                    try:
                        # Check how many valid numeric values we have
                        valid_revenue_count = filtered_df[revenue_col].notna().sum()
                        st.write(f"**Valid revenue entries:** {valid_revenue_count} out of {len(filtered_df)}")
                        
                        if valid_revenue_count > 0:
                            # Get top 10 companies with valid revenue data
                            top_10 = filtered_df.dropna(subset=[revenue_col]).nlargest(10, revenue_col)
                            
                            st.write(f"**Top 10 companies found:** {len(top_10)}")
                            
                            if len(top_10) > 0:
                                # Show the data we're trying to chart
                                st.write("**Data for chart:**")
                                chart_data = top_10[[name_col, revenue_col]].set_index(name_col)[revenue_col]
                                st.write(chart_data)
                                
                                # Create the chart
                                st.bar_chart(chart_data, height=400)
                            else:
                                st.warning("No companies found after filtering")
                        else:
                            st.warning("No valid numeric revenue data found")
                            st.write("**Raw revenue column sample:**")
                            st.write(filtered_df[revenue_col].head(10))
                            
                    except Exception as e:
                        st.error(f"Error creating chart: {str(e)}")
                        st.write("**Error details:**")
                        st.write(f"Revenue column type: {filtered_df[revenue_col].dtype}")
                        st.write(f"Sample values: {filtered_df[revenue_col].head(5).tolist()}")
                else:
                    st.warning("Could not find required columns")
                    st.write("**Available columns:**", list(filtered_df.columns))
                    
                    # Try to find any column that might contain revenue data
                    st.write("**Column content preview:**")
                    for col in filtered_df.columns:
                        st.write(f"**{col}:** {filtered_df[col].iloc[0] if len(filtered_df) > 0 else 'No data'}")
            
            with tab2:
                # Find industry column
                industry_col = None
                for col in filtered_df.columns:
                    if 'industry' in col.lower() or 'sector' in col.lower():
                        industry_col = col
                        break
                
                if industry_col:
                    try:
                        industry_counts = filtered_df[industry_col].value_counts()
                        if len(industry_counts) > 0:
                            st.bar_chart(industry_counts, height=400)
                        else:
                            st.warning("No industry data found")
                    except Exception as e:
                        st.error(f"Error creating industry chart: {str(e)}")
                else:
                    st.warning("Could not find industry column")
                    st.write("Available columns:", list(filtered_df.columns))
            
            with tab3:
                # Find employees column
                employees_col = None
                name_col = None
                
                for col in filtered_df.columns:
                    if 'employee' in col.lower():
                        employees_col = col
                        break
                
                for col in filtered_df.columns:
                    if 'name' in col.lower() or 'company' in col.lower():
                        name_col = col
                        break
                
                if employees_col and name_col:
                    try:
                        # Ensure employees column is numeric
                        filtered_df[employees_col] = pd.to_numeric(filtered_df[employees_col], errors='coerce')
                        
                        # Get top 10 employers
                        top_employers = filtered_df.nlargest(10, employees_col).dropna(subset=[employees_col])
                        
                        if len(top_employers) > 0:
                            chart_data = top_employers.set_index(name_col)[employees_col]
                            st.bar_chart(chart_data, height=400)
                        else:
                            st.warning("No valid employee data found")
                    except Exception as e:
                        st.error(f"Error creating employees chart: {str(e)}")
                else:
                    st.warning("Could not find employees or name column")
                    st.write("Available columns:", list(filtered_df.columns))
        
        # Download section
        st.markdown("---")
        st.subheader("💾 Download Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"us_companies_revenue_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                type="primary"
            )
        
        with col2:
            st.info(f"📊 Dataset contains {len(filtered_df)} companies")
    
    else:
        st.error("❌ Failed to scrape data. Please try refreshing the page.")
        st.markdown("""
        **Possible reasons:**
        - Wikipedia page structure has changed
        - Network connectivity issues
        - Rate limiting from Wikipedia
        
        Please try again in a few moments.
        """)

if __name__ == "__main__":
    main()
