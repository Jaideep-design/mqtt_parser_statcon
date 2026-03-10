def parse_packet(data_string, df):

    df = df.dropna(subset=['Index', 'Total Upto'])
    data_string = data_string.ljust(int(df['Total Upto'].max()) + 5)

    decoded_results = []

    for _, row in df.iterrows():
        try:
            short_name = str(row['Short name'])

            start = int(row['Index']) - 1
            end = int(row['Total Upto'])

            raw_segment = data_string[start:end]

            # Check if the field contains only spaces
            if raw_segment.strip() == "":
                decoded_results.append({
                    "Short name": short_name,
                    "Value": "N/A",
                    "Units": ""
                })
                continue

            data_format = str(row['Data format']).strip()
            scaling = float(row['Scaling Factor']) if pd.notnull(row['Scaling Factor']) else 1.0
            offset = float(row['Offset']) if pd.notnull(row['Offset']) else 0.0
            units = str(row['Units']) if pd.notnull(row['Units']) else ""

            if data_format == 'ASCII':
                final_val = raw_segment.strip()
            else:
                try:
                    numeric_val = float(raw_segment.strip())
                except ValueError:
                    numeric_val = int(raw_segment.strip(), 16)

                final_val = (numeric_val * scaling) + offset

                if final_val == int(final_val):
                    final_val = int(final_val)
                else:
                    final_val = round(final_val, 4)

            decoded_results.append({
                "Short name": short_name,
                "Value": final_val,
                "Units": units
            })

        except Exception as e:
            print("Parser error:", e, "Row:", row)
            continue

    return decoded_results
