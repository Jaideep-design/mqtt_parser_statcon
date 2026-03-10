def parse_packet(data_string, df):
    # Read the Excel data dictionary
    # df = pd.read_excel(excel_path)

    # Ensure we only process rows with valid indices
    df = df.dropna(subset=['Index', 'Total Upto'])

    decoded_results = []

    for _, row in df.iterrows():
        try:
            short_name = str(row['Short name'])
            # 'Index' in Excel is 1-based; Python is 0-based
            start = int(row['Index']) - 1
            # 'Total Upto' is used as the end of the slice
            end = int(row['Total Upto'])

            # Extract the raw string segment
            raw_segment = data_string[start:end].strip()

            # Skip if segment is empty
            if not raw_segment:
                decoded_results.append((short_name, "N/A", ""))
                continue

            data_format = str(row['Data format']).strip()
            scaling = float(row['Scaling Factor']) if pd.notnull(row['Scaling Factor']) else 1.0
            offset = float(row['Offset']) if pd.notnull(row['Offset']) else 0.0
            units = str(row['Units']) if pd.notnull(row['Units']) else ""

            if data_format == 'ASCII':
                # Literal text (like Lat/Long or RTC)
                final_val = raw_segment
            else:
                # Numeric text (e.g., "0123" represents the number 123)
                try:
                    # Attempt base-10 conversion for ASCII numeric data
                    numeric_val = float(raw_segment)
                    final_val = (numeric_val * scaling) + offset
                    # Clean up integers
                    if final_val == int(final_val):
                        final_val = int(final_val)
                    else:
                        final_val = round(final_val, 4)
                except ValueError:
                    # If it contains hex characters (like '3D'), parse as hex
                    try:
                        numeric_val = int(raw_segment, 16)
                        final_val = (numeric_val * scaling) + offset
                    except:
                        final_val = raw_segment  # Fallback to original string

            decoded_results.append({
                "Short name": short_name,
                "Value": final_val,
                "Units": units
            })

        except Exception:
            continue

    return decoded_results
