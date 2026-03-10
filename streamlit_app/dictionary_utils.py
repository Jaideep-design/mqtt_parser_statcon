import pandas as pd
import json

def excel_to_json(uploaded_file):

    # Read the Excel file
    df = pd.read_excel(uploaded_file)

    # Convert dataframe to list of dictionaries
    registers = df.to_dict(orient="records")

    # Save to JSON file
    with open("output.json", "w") as f:
        json.dump(registers, f, indent=4)

    print("Excel successfully converted to JSON")

    return registers
