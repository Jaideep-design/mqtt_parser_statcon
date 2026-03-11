import pandas as pd
import json

def excel_to_json(uploaded_file):

    # Read Excel
    df = pd.read_excel(uploaded_file)

    # Columns we want to keep
    required_columns = [
        "Sr. No.",
        "Parameter",
        "Short name",
        "Size [byte]",
        "Index",
        "Total Upto",
        "Scaling Factor",
        "Offset",
        "Data format",
        "Units"
    ]

    # Keep only required columns (ignore if some missing)
    df = df[[col for col in required_columns if col in df.columns]]

    # Convert to list of dictionaries
    registers = df.to_dict(orient="records")

    # Save JSON
    with open("output.json", "w") as f:
        json.dump(registers, f, indent=4)

    print("Excel successfully converted to JSON")

    return registers
