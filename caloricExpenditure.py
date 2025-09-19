# To run this script, you will need to install the pandas and numpy libraries.
# You can do this by running the following command in your terminal:
# pip install pandas numpy

# The script now expects a single command-line argument:
# 1. Path to the CSV file with triaxial data

import pandas as pd
import numpy as np
import sys
import os

def get_user_data():
    """
    Prompts the user for personal information required for the calculation.
    Includes basic input validation to ensure correct data types.
    """
    print("Please provide your personal data for the calculation:")
    
    # Get and validate age
    while True:
        try:
            age = int(input("Enter your age (in years): "))
            if age <= 0:
                print("Age must be a positive number. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number for age.")

    # Get and validate height
    while True:
        try:
            height = float(input("Enter your height (in cm): "))
            if height <= 0:
                print("Height must be a positive number. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number for height.")

    # Get and validate weight
    while True:
        try:
            weight = float(input("Enter your weight (in kg): "))
            if weight <= 0:
                print("Weight must be a positive number. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number for weight.")

    # Get and validate gender
    while True:
        gender = input("Enter your gender (Male/Female): ").strip().lower()
        if gender in ["male", "female"]:
            break
        else:
            print("Invalid input. Please enter 'Male' or 'Female'.")
            
    return {'age': age, 'height': height, 'weight': weight, 'gender': gender}

def convert_to_triaxial_counts(df, x_col, y_col, z_col):
    """
    Converts raw triaxial accelerometer data to a series of "triaxial counts"
    by calculating the vector magnitude and summing the values over 15-second epochs.
    
    Args:
        df (pd.DataFrame): DataFrame containing the raw accelerometer data.
        x_col (str): Name of the column with the X-axis acceleration data.
        y_col (str): Name of the column with the Y-axis acceleration data.
        z_col (str): Name of the column with the Z-axis acceleration data.
                              
    Returns:
        list: A list of the calculated triaxial counts for each epoch.
    """
    # Calculate the vector magnitude for each data point
    df['vector_magnitude'] = np.sqrt(df[x_col]**2 + df[y_col]**2 + df[z_col]**2)
    
    # Resample the data into 15-second epochs and sum the vector magnitudes
    triaxial_counts = df['vector_magnitude'].resample('15S').sum().tolist()
    
    return triaxial_counts


def calculate_bmr(user_data):
    """
    Calculates the Basal Metabolic Rate (BMR) using the Harris-Benedict formula.
    
    Args:
        user_data (dict): A dictionary containing 'age', 'height', 'weight', and 'gender'.
        
    Returns:
        float: The calculated BMR in kcal/day.
    """
    age = user_data['age']
    height = user_data['height']
    weight = user_data['weight']
    gender = user_data['gender']
    
    if gender == 'male':
        # BMR for males: 88.362 + (13.397 x weight in kg) + (4.799 x height in cm) - (5.677 x age in years)
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == 'female':
        # BMR for females: 447.593 + (9.247 x weight in kg) + (3.098 x height in cm) - (4.330 x age in years)
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)


def calculate_triaxial_expenditure(triaxial_counts, user_data):
    """
    Calculates total caloric expenditure from a list of triaxial counts.
    
    This function applies the formulas from Table 3 of the article.
    
    Args:
        triaxial_counts (list): A list of triaxial counts for each epoch.
        user_data (dict): A dictionary containing 'age', 'height', 'weight', and 'gender'.
        
    Returns:
        float: The total calculated caloric expenditure in kilocalories (kcal).
    """
    
    # Initialize a list to store the energy expenditure for each data point
    expenditures = []
    
    # Extract user data for easier access
    age = user_data['age']
    weight = user_data['weight']
    gender = user_data['gender']

    # Iterate through each count in the list
    for count in triaxial_counts:
        ee_per_min = 0.0 # Energy Expenditure in kcal/min

        # Apply the appropriate triaxial formula based on gender
        if gender == 'male':
            # Formula for males: EE = -106.59251 + 0.40825(Age) + 0.35249(Weight) - 0.22485(Triaxial Counts)
            ee_per_min = -106.59251 + (0.40825 * age) + (0.35249 * weight) - (0.22485 * count)
        elif gender == 'female':
            # Formula for females: EE = -56.09672 + 0.38459(Age) + 0.16541(Weight) - 0.16912(Triaxial Counts)
            ee_per_min = -56.09672 + (0.38459 * age) + (0.16541 * weight) - (0.16912 * count)
        
        # The formulas can result in negative values, especially for low activity.
        # We will assume a minimum of 0 expenditure per minute.
        expenditures.append(max(0, ee_per_min))

    # Sum all the individual expenditures to get the total
    total_expenditure_min = sum(expenditures)
    
    # Since each epoch is 15 seconds, we divide the total by 4
    total_expenditure_kcal = total_expenditure_min / 4
    
    return total_expenditure_kcal


if __name__ == "__main__":
    # The script now expects a single command-line argument:
    # 1. Path to the CSV file with triaxial data

    if len(sys.argv) != 2:
        print("Usage: python caloric_expenditure_calculator.py <triaxial_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    user_info = get_user_data()

    try:
        # The file has 10 lines of metadata, so we skip them
        df = pd.read_csv(file_path, skiprows=10)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df = df.set_index('Timestamp')
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        sys.exit(1)
            
    print("\nPlease inspect your CSV file and find the columns for X, Y, and Z acceleration.")
    x_col_name = input(f"Enter the name of the X-axis column in '{os.path.basename(file_path)}': ")
    y_col_name = input(f"Enter the name of the Y-axis column in '{os.path.basename(file_path)}': ")
    z_col_name = input(f"Enter the name of the Z-axis column in '{os.path.basename(file_path)}': ")

    if not all(col in df.columns for col in [x_col_name, y_col_name, z_col_name]):
        print(f"Error: One or more of the specified columns were not found.")
        print("Available columns are:", list(df.columns))
        sys.exit(1)

    print("\nConverting raw triaxial data to accelerometer counts...")
    triaxial_counts = convert_to_triaxial_counts(df, x_col_name, y_col_name, z_col_name)
    
    # The total duration is the difference between the first and last timestamps
    total_duration_seconds = (df.index[-1] - df.index[0]).total_seconds()
    total_duration_hours = total_duration_seconds / 3600

    print("\nCalculating caloric expenditure using the ActiGraph triaxial formula...")
    
    # Calculate the BMR
    bmr_per_day = calculate_bmr(user_info)
    
    # Calculate BMR for the duration of the activity
    bmr_for_activity = (bmr_per_day / 24) * total_duration_hours
    
    # Calculate activity-based expenditure
    activity_expenditure = calculate_triaxial_expenditure(triaxial_counts, user_info)
    
    total_kcal = bmr_for_activity + activity_expenditure
    
    if total_kcal is not None:
        print(f"\nBased on the data and your information, the total estimated caloric expenditure is {total_kcal:.2f} kcal.")
    print("Calculation complete.")
