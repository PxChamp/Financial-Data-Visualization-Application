# Financial Data Visualization Application

This code is an application built using Dash, a Python framework for building analytical web applications. The application allows users to analyze financial data for a given stock symbol and visualize it using interactive charts and maps. The code fetches financial data from Yahoo Finance using the yfinance library, retrieves geolocation information using the [OpenCageData API](https://opencagedata.com/), and creates visualizations using Plotly and Dash Leaflet.

## Prerequisites
To run this code, you need to have the following libraries installed:

- dash
- dash_leaflet
- yfinance
- requests
- plotly

## Getting Started
1. Install the required libraries mentioned above.
2. Copy and paste the code into a Python file.
3. Run the Python file.

## Code Structure
The code is structured as follows:

1. **Library Imports**: The necessary libraries are imported.
2. **Constant Definitions**: Constants for colors are defined.
3. **Function Definitions**:
    * **get_coordinates**: Function to obtain geographical coordinates using the OpenCageData API.
    * **get_value_dictionnary**: Function to retrieve the value of a field in a dictionary formatted with a given number of decimal places.
    * **get_date**: Function to obtain a formatted date from a timestamp.
    * **get_currency_symbol**: Function to get the currency symbol based on the currency code.
4. **Dash Application Initialization**: The Dash application is initialized.
5. **User Interface Components**: HTML components are defined for the header, search section, graph section, map section, additional information section, and footer.
6. **Dash Layout**: The layout of the Dash application is defined using the HTML components.
7. **Callback Function**: The callback function is defined to update the user interface elements based on user inputs.
8. **Main Execution**: The Dash application is run.

## Usage
1. Enter the desired stock symbol in the search input field.
2. Select the desired date range using the date picker.
3. The application will fetch the financial data for the specified stock symbol and display it in the graph section.
4. Additional information about the stock and the company will be displayed in the additional information section.
5. The location of the company will be shown on the map.

## Contributing
Contributions to this code are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.
