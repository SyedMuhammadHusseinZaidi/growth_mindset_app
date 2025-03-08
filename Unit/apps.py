import streamlit as st
import math
import datetime

# ----------------------------
# Conversion Functions Section
# ----------------------------

def convert_length(value, conversion):
    if conversion == "Kilometers to Miles":
        return value * 0.621371
    elif conversion == "Miles to Kilometers":
        return value / 0.621371
    elif conversion == "Meters to Feet":
        return value * 3.28084
    elif conversion == "Feet to Meters":
        return value / 3.28084
    elif conversion == "Centimeters to Inches":
        return value * 0.393701
    elif conversion == "Inches to Centimeters":
        return value / 0.393701
    elif conversion == "Millimeters to Inches":
        return value * 0.0393701
    elif conversion == "Inches to Millimeters":
        return value / 0.0393701

def convert_temperature(value, conversion):
    if conversion == "Celsius to Fahrenheit":
        return (value * 9/5) + 32
    elif conversion == "Fahrenheit to Celsius":
        return (value - 32) * 5/9
    elif conversion == "Celsius to Kelvin":
        return value + 273.15
    elif conversion == "Kelvin to Celsius":
        return value - 273.15
    elif conversion == "Fahrenheit to Kelvin":
        return (value - 32) * 5/9 + 273.15
    elif conversion == "Kelvin to Fahrenheit":
        return (value - 273.15) * 9/5 + 32

def convert_weight(value, conversion):
    if conversion == "Kilograms to Pounds":
        return value * 2.20462
    elif conversion == "Pounds to Kilograms":
        return value / 2.20462
    elif conversion == "Grams to Ounces":
        return value * 0.035274
    elif conversion == "Ounces to Grams":
        return value / 0.035274

def convert_volume(value, conversion):
    if conversion == "Liters to Gallons":
        return value * 0.264172
    elif conversion == "Gallons to Liters":
        return value / 0.264172
    elif conversion == "Milliliters to Fluid Ounces":
        return value * 0.033814
    elif conversion == "Fluid Ounces to Milliliters":
        return value / 0.033814

def convert_time(value, conversion):
    if conversion == "Seconds to Minutes":
        return value / 60.0
    elif conversion == "Minutes to Seconds":
        return value * 60.0
    elif conversion == "Minutes to Hours":
        return value / 60.0
    elif conversion == "Hours to Minutes":
        return value * 60.0
    elif conversion == "Hours to Days":
        return value / 24.0
    elif conversion == "Days to Hours":
        return value * 24.0

def convert_speed(value, conversion):
    if conversion == "km/h to mph":
        return value * 0.621371
    elif conversion == "mph to km/h":
        return value / 0.621371
    elif conversion == "m/s to km/h":
        return value * 3.6
    elif conversion == "km/h to m/s":
        return value / 3.6

def convert_angle(value, conversion):
    if conversion == "Degrees to Radians":
        return math.radians(value)
    elif conversion == "Radians to Degrees":
        return math.degrees(value)

def convert_currency(value, conversion):
    # Using static exchange rates
    # Example rates: 1 USD = 0.85 EUR, 1 EUR = 1.18 USD, 1 USD = 82 INR, 1 INR = 0.0122 USD
    if conversion == "USD to EUR":
        return value * 0.85
    elif conversion == "EUR to USD":
        return value * 1.18
    elif conversion == "USD to INR":
        return value * 82.0
    elif conversion == "INR to USD":
        return value * 0.0122

# ----------------------------
# Conversion History Setup
# ----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

def add_history(category, conversion_type, input_value, result):
    st.session_state.history.append({
        "Category": category,
        "Conversion": conversion_type,
        "Input": input_value,
        "Result": result,
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# ----------------------------
# Streamlit App UI Section
# ----------------------------
st.title("Advanced Unit Converter")
st.write("This enhanced converter supports multiple conversion types and keeps a history of your conversions.")

# Sidebar: Choose conversion category
category = st.sidebar.selectbox("Select Conversion Category", [
    "Length", "Temperature", "Weight", "Volume", "Time", "Speed", "Angle", "Currency"
])

value = st.number_input("Enter the value to convert", value=0.0)

# Process based on selected category
if category == "Length":
    conversion_type = st.selectbox("Select Length Conversion", [
        "Kilometers to Miles", "Miles to Kilometers",
        "Meters to Feet", "Feet to Meters",
        "Centimeters to Inches", "Inches to Centimeters",
        "Millimeters to Inches", "Inches to Millimeters"
    ])
    if st.button("Convert", key="length"):
        result = convert_length(value, conversion_type)
        st.success(f"Converted Value: {result}")
        add_history(category, conversion_type, value, result)

elif category == "Temperature":
    conversion_type = st.selectbox("Select Temperature Conversion", [
        "Celsius to Fahrenheit", "Fahrenheit to Celsius",
        "Celsius to Kelvin", "Kelvin to Celsius",
        "Fahrenheit to Kelvin", "Kelvin to Fahrenheit"
    ])
    if st.button("Convert", key="temperature"):
        result = convert_temperature(value, conversion_type)
        st.success(f"Converted Temperature: {result}")
        add_history(category, conversion_type, value, result)

elif category == "Weight":
    conversion_type = st.selectbox("Select Weight Conversion", [
        "Kilograms to Pounds", "Pounds to Kilograms",
        "Grams to Ounces", "Ounces to Grams"
    ])
    if st.button("Convert", key="weight"):
        result = convert_weight(value, conversion_type)
        st.success(f"Converted Weight: {result}")
        add_history(category, conversion_type, value, result)

elif category == "Volume":
    conversion_type = st.selectbox("Select Volume Conversion", [
        "Liters to Gallons", "Gallons to Liters",
        "Milliliters to Fluid Ounces", "Fluid Ounces to Milliliters"
    ])
    if st.button("Convert", key="volume"):
        result = convert_volume(value, conversion_type)
        st.success(f"Converted Volume: {result}")
        add_history(category, conversion_type, value, result)

elif category == "Time":
    conversion_type = st.selectbox("Select Time Conversion", [
        "Seconds to Minutes", "Minutes to Seconds",
        "Minutes to Hours", "Hours to Minutes",
        "Hours to Days", "Days to Hours"
    ])
    if st.button("Convert", key="time"):
        result = convert_time(value, conversion_type)
        st.success(f"Converted Time: {result}")
        add_history(category, conversion_type, value, result)

elif category == "Speed":
    conversion_type = st.selectbox("Select Speed Conversion", [
        "km/h to mph", "mph to km/h",
        "m/s to km/h", "km/h to m/s"
    ])
    if st.button("Convert", key="speed"):
        result = convert_speed(value, conversion_type)
        st.success(f"Converted Speed: {result}")
        add_history(category, conversion_type, value, result)

elif category == "Angle":
    conversion_type = st.selectbox("Select Angle Conversion", [
        "Degrees to Radians", "Radians to Degrees"
    ])
    if st.button("Convert", key="angle"):
        result = convert_angle(value, conversion_type)
        st.success(f"Converted Angle: {result}")
        add_history(category, conversion_type, value, result)

elif category == "Currency":
    conversion_type = st.selectbox("Select Currency Conversion", [
        "USD to EUR", "EUR to USD",
        "USD to INR", "INR to USD"
    ])
    if st.button("Convert", key="currency"):
        result = convert_currency(value, conversion_type)
        st.success(f"Converted Currency: {result}")
        add_history(category, conversion_type, value, result)

# ----------------------------
# Display Conversion History
# ----------------------------
st.markdown("---")
st.subheader("Conversion History")
if st.session_state.history:
    st.table(st.session_state.history)
    if st.button("Clear History"):
        st.session_state.history = []
else:
    st.write("No conversions yet.")
    