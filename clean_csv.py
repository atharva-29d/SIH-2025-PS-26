import pandas as pd

input_filename = 'Copy of Book1(1).csv'
output_filename = 'namaste_codes_cleaned.csv'

try:
    print(f"Reading '{input_filename}'...")
    df = pd.read_csv(input_filename)

    # Check if the column exists before cleaning
    if 'NAMASTE_Code' in df.columns:
        # Clean the column: convert to string and strip whitespace
        df['NAMASTE_Code'] = df['NAMASTE_Code'].astype(str).str.strip()

        # Save the cleaned data to a new file
        df.to_csv(output_filename, index=False)
        print(f"✅ Successfully cleaned the data and saved it to '{output_filename}'")
    else:
        print(f"❌ ERROR: Column 'NAMASTE_Code' not found in the file.")

except FileNotFoundError:
    print(f"❌ ERROR: Could not find the file '{input_filename}'.")
except Exception as e:
    print(f"An error occurred: {e}")