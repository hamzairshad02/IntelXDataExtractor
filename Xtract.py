import pandas as pd
import zipfile
import re
import os
import pathlib

# Display banner
def display_banner():
    banner = r"""
.___        __         .__  ____  ___ __                        __                
|   | _____/  |_  ____ |  | \   \/  //  |_____________    _____/  |_  ___________ 
|   |/    \   __\/ __ \|  |  \     /\   __\_  __ \__  \ _/ ___\   __\/  _ \_  __ \
|   |   |  \  | \  ___/|  |__/     \ |  |  |  | \// __ \\  \___|  | (  <_> )  | \/
|___|___|  /__|  \___  >____/___/\  \|__|  |__|  (____  /\___  >__|  \____/|__|   
         \/          \/           \_/                 \/     \/                    
    
                Intelligence X Data Extractor
    """
    print(banner)

# Load and parse Info.csv from the ZIP
def load_info_csv_from_zip(zip_path):
    mapping = {}
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        with zip_ref.open('Info.csv') as info_file:
            info_df = pd.read_csv(info_file)
            for _, row in info_df.iterrows():
                system_id = row['System ID'].split('.')[0]
                name = re.sub(r" \[Part \d+ of \d+\]", "", row['Name'])
                date = row['Date']
                mapping[system_id] = {
                    "name": name,
                    "date": date,
                    "bucket": row.get('Bucket', ''),
                    "media": row.get('Media', ''),
                    "content_type": row.get('Content Type', ''),
                    "size": row.get('Size', '')
                }
    print("Info.csv mapping loaded successfully.")
    return mapping

# Extract and process data from each file in the ZIP
def extract_and_process_data(zip_path, domain):
    mapping = load_info_csv_from_zip(zip_path)
    extracted_data = []
    credentials = []
    raw_data_lines = []

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename == "Info.csv":
                continue
            system_id = file_info.filename.split('.')[0]
            file_info_data = mapping.get(system_id, {
                "name": file_info.filename,
                "date": "Unknown Date"
            })
            file_info_data["date"] = pd.to_datetime(file_info_data["date"], errors='coerce').date() if file_info_data["date"] != "Unknown Date" else None

            # Add verbosity (log file processing)
            print(f"Processing file: {system_id} -> Mapped to: {file_info_data['name']}, Date: {file_info_data['date']}")

            with zip_ref.open(file_info) as file:
                try:
                    content = file.read().decode(errors='ignore')
                    for line in content.splitlines():
                        if domain in line:
                            email_matches = re.findall(rf"\b[A-Za-z0-9._%+-]+@{domain}\b", line)
                            for email in email_matches:
                                password = extract_password(line, email)
                                if password:  # Only process if password exists
                                    row_data = {
                                        "Email": email,
                                        "Password": password,
                                        "Filename": file_info_data["name"],
                                        "Date": file_info_data["date"],
                                        "Phone": extract_phone(line),
                                        "Address": extract_address(line),
                                        "Bucket": file_info_data.get("bucket", ''),
                                        "Media": file_info_data.get("media", ''),
                                        "Content Type": file_info_data.get("content_type", ''),
                                        "Size": file_info_data.get("size", '')
                                    }
                                    extracted_data.append(row_data)
                                    credentials.append(f"{email}:{password}")
                                    raw_data_lines.append(f"Filename: {file_info_data['name']} | Date: {file_info_data['date']}\n{line}")
                except Exception as e:
                    print(f"Could not process file {file_info.filename}: {e}")

    return pd.DataFrame(extracted_data), credentials, raw_data_lines

# Filtering function to keep only the oldest record per Email & Password
def filter_oldest_entries(df):
    df_sorted = df.sort_values(by=["Date"], ascending=True)  # Sort by oldest date
    df_filtered = df_sorted.drop_duplicates(subset=["Email", "Password"], keep="first")
    return df_filtered

# Helper functions
def extract_password(line, email):
    match = re.search(rf"{email}:(\S+)", line)
    return match.group(1).split(':')[0] if match else ""

def extract_phone(line):
    match = re.search(r"\+?\d[\d\s.-]{8,14}\d", line)
    return match.group(0) if match else ""

def extract_address(line):
    match = re.search(r"\d{1,5}\s\w+\s\w+", line)
    return match.group(0) if match else ""

# Save all output files, including "filtered.xlsx"
def save_results(output_dir, extracted_df, credentials, raw_data_lines):
    output_dir = pathlib.Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save the full result to "result.xlsx"
    extracted_df.to_excel(output_dir / "result.xlsx", index=False)

    # Save the filtered result to "filtered.xlsx"
    filtered_df = filter_oldest_entries(extracted_df)
    filtered_df.to_excel(output_dir / "filtered.xlsx", index=False)

    # Save credentials to .txt files
    with open(output_dir / "credentials.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(credentials))

    with open(output_dir / "emails.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(set([cred.split(':')[0] for cred in credentials])))

    with open(output_dir / "passwords.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(set([cred.split(':')[1] for cred in credentials if ':' in cred])))

    # Save raw data to .txt file with added blank lines for readability
    raw_data_path = output_dir / "raw_data.txt"
    with open(raw_data_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(raw_data_lines))

    print("All results saved successfully.")

    # Remove raw_data.txt after processing
    try:
        os.remove(raw_data_path)
        print("raw_data.txt has been removed.")
    except Exception as e:
        print(f"Failed to delete raw_data.txt: {e}")

# Main function with input validation
def main():
    display_banner()
    
    while True:
        zip_path = input("Enter the path to the Intelligence X zip file: ")
        zip_path = str(pathlib.Path(zip_path).resolve())  # Ensure cross-platform path handling

        if not zip_path.endswith(".zip"):
            print("Error: The file must be a .zip archive. Please check your input and try again. Make sure the input ends with .zip (e.g. Search 2025-01-27 19_22_10.zip).")
            continue
        if not os.path.exists(zip_path):
            print("Error: The specified file does not exist. Please check the path and try again.")
            continue
        break

    domain = input("Enter the domain to search for (e.g., example.com): ")
    output_dir = input("Enter the output folder name: ")

    # Process data and create result DataFrame
    extracted_df, credentials, raw_data_lines = extract_and_process_data(zip_path, domain)

    # Save all outputs
    save_results(output_dir, extracted_df, credentials, raw_data_lines)
    print(f"All files saved successfully in '{output_dir}'.")

if __name__ == "__main__":
    main()
