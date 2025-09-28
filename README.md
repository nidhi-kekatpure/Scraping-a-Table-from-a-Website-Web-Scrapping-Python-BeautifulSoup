# US Companies Revenue Scraper - Streamlit App

An interactive web application that scrapes real-time data of the largest U.S. companies by revenue from Wikipedia and presents it in a user-friendly dashboard.

## Live Demo
**Try the app now:** [https://us-companies-revenue-tracker.streamlit.app](https://us-companies-revenue-tracker.streamlit.app)

## Features

- **Real-time Data Scraping**: Fetches the latest company data from Wikipedia
- **Interactive Dashboard**: Filter and sort companies by industry and revenue
- **Data Visualizations**: Charts showing top companies, industry distribution, and employee counts
- **Export Functionality**: Download filtered data as CSV
- **Responsive Design**: Works on desktop and mobile devices
- **Caching**: Optimized performance with data caching

## Technologies Used

- **Streamlit**: Web app framework
- **Pandas**: Data manipulation and analysis
- **BeautifulSoup**: Web scraping
- **Requests**: HTTP requests
- **Python**: Core programming language

## Data Source

Data is scraped from: [Wikipedia - List of largest companies in the United States by revenue](https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue)

## Running Locally

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to `http://localhost:8501`


## Project Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README_streamlit.md    # This file
└── Scraping a Table from a Website.ipynb  # Original Jupyter notebook
```

## Configuration

The app includes several configurable features:

- **Caching**: Data is cached for 1 hour to improve performance
- **Error Handling**: Robust error handling for network issues
- **User Agent**: Proper headers to avoid being blocked
- **Data Cleaning**: Automatic cleaning of scraped data

## App Sections

1. **Header**: App title and description
2. **Sidebar**: Controls and information
3. **Metrics**: Key statistics (total companies, revenue, employees)
4. **Filters**: Industry and revenue filtering
5. **Data Table**: Interactive data display
6. **Visualizations**: Charts and graphs
7. **Download**: CSV export functionality

## Customization

You can customize the app by:

- Modifying the CSS in the `st.markdown()` sections
- Adding new chart types in the visualization tabs
- Implementing additional filters
- Changing the color scheme and layout

## Troubleshooting

**Common Issues:**

1. **Data not loading**: Check internet connection and Wikipedia availability
2. **Deployment errors**: Ensure all dependencies are in requirements.txt
3. **Slow performance**: Data is cached, but initial load may take time

**Solutions:**

- Use the "Refresh Data" button to reload
- Check Streamlit Cloud logs for deployment issues
- Clear cache if data seems outdated

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
