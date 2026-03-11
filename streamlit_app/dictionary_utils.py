import pandas as pd
import numpy as np
import json

def excel_to_json(uploaded_file):

    df = pd.read_excel(uploaded_file)

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

    df = df.loc[:, required_columns]

    # Convert NaN to None everywhere
    df = df.where(pd.notnull(df), None)

    registers = df.to_dict(orient="records")

    with open("output.json", "w") as f:
        json.dump(registers, f, indent=4)

    return registers
