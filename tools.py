import os
from langchain.tools import tool
import requests
import math
# Calculator tool 
@tool
def Calculator(expression, allow_large_numbers=True, allow_division_by_zero=False, max_result=10**100):
    """ 
Evaluates a mathematical expression with enhanced error handling and safety checks.

Args:
    expression (str): The mathematical expression to evaluate. Examples:
        - Simple arithmetic: "2 + 3 * 4"
        - Advanced functions: "log(10)", "sin(30)", "factorial(5)"
    allow_large_numbers (bool, optional): If False, prevents results larger than `max_result`. Defaults to True.
    allow_division_by_zero (bool, optional): If False, raises an error for division by zero. Defaults to False.
    max_result (int, optional): The maximum allowable result for calculations if `allow_large_numbers` is False.
        Defaults to 10**100.

Returns:
    str: A string representation of the evaluated result or an error message in the following format:
        - If successful:
            "<calculated_value>"
        - If an error occurs:
            "Error: <error_message>"

    Example formatted responses:
        - Successful calculation: "120"
        - Large number error: "Error: Result exceeds the allowed limit for large numbers."
        - Division by zero error: "Error: Division by zero is not allowed."
        - Invalid expression: "Error: Expression contains invalid characters."

Raises:
    ValueError: If the expression is not a string or contains invalid characters.
    OverflowError: If the result exceeds the maximum allowed value and `allow_large_numbers` is False.
    ZeroDivisionError: If division by zero occurs and `allow_division_by_zero` is False.
"""
    try:
        allowed_funcs = {
            "log": math.log,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "factorial": math.factorial,
            "exp": math.exp,
            "pow": pow,
        }
        if not isinstance(expression, str):
            raise ValueError("Expression must be a string.")
        sanitized_expression = expression.replace(" ", "")
        allowed_chars = "0123456789+-*/().,!"
        if not all(char in allowed_chars or char.isalpha() for char in sanitized_expression):
            raise ValueError("Expression contains invalid characters.")
        if "!" in sanitized_expression:
            sanitized_expression = sanitized_expression.replace("!", ".factorial()")
        result = eval(sanitized_expression, {"__builtins__": None}, allowed_funcs)
        if not allow_large_numbers and isinstance(result, (int, float)) and abs(result) > max_result:
            raise OverflowError("Result exceeds the allowed limit for large numbers.")
        if not allow_division_by_zero and isinstance(result, float) and math.isinf(result):
            raise ZeroDivisionError("Division by zero is not allowed.")
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def Weather(city_name):
    """
    Fetches the current weather for a given city using the OpenWeather API.

    Args:
        city_name (str): The name of the city to fetch the weather for.

    Returns:
        str: A formatted string containing the weather details or an error message.
            The formatted response includes:
            - A title with the city name and a weather emoji for visual appeal.
            - Weather details listed in bullet points:
                - **Condition**: A brief description of the current weather (e.g., Clear, Smoke).
                - **Temperature**: The current temperature in Celsius.
                - **Humidity**: The humidity level in percentage.
                - **Wind Speed**: The speed of the wind in meters per second.
            Example of the formatted response:
                🌤️ **Weather Update for Lahore** 🌤️
                - **Condition**: Smoke
                - **Temperature**: 12.99°C
                - **Humidity**: 67%
                - **Wind Speed**: 0 m/s

    Raises:
        ValueError: If the API key is missing, invalid, or the city name is invalid.
        ConnectionError: If the weather data cannot be fetched due to network or server issues.
    """
    try:
        # Fetch API key from environment
        api_key = os.environ.get("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError("Missing OpenWeather API key.")

        # Validate city name
        if not isinstance(city_name, str) or not city_name.strip():
            raise ValueError("City name must be a non-empty string.")

        # OpenWeather API URL and parameters
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city_name, "appid": api_key, "units": "metric"}
        response = requests.get(base_url, params=params, timeout=10)

        # Handle HTTP errors
        if response.status_code == 401:
            raise ValueError("Invalid API key.")
        elif response.status_code == 404:
            raise ValueError(f"City '{city_name}' not found.")
        elif response.status_code != 200:
            raise ConnectionError(f"Failed to fetch weather data. HTTP status: {response.status_code}")

        # Parse weather data
        data = response.json()
        weather_info = {
            "city": data.get("name", city_name),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
        }

        # Format the response with each detail on a new line
        formatted_response = (
            f"Weather: {weather_info['description']}\n"
            f"Temperature: {weather_info['temperature']}°C\n"
            f"Humidity: {weather_info['humidity']}%\n"
            f"Wind Speed: {weather_info['wind_speed']} m/s\n"
            f"City: {weather_info['city']}"
        )
        return formatted_response

    except Exception as e:
        return f"Error: {str(e)}"





# Initialize tools and LLM
tools = [Calculator,Weather]
