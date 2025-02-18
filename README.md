# **Intelligence X Data Extractor**

A powerful Python script for extracting and analyzing Intelligence X `.zip` archives containing leaked data. This script processes the archive, extracts relevant credentials and metadata, and filters the data in a separate file to indicate the first leaked instance of the leaked credentials per unique Email + Password pair.

---

## **🔹 Features**
- Extracts data from **Intelligence X** `.zip` archives.
- Saves all extracted credentials, emails, and passwords in structured files.
- **Filters and keeps only the oldest entry** per **Email + Password** in `filtered.xlsx` to indicate the first leaked instance of the credentials.
- Works on **Windows, macOS, and Linux** (uses `pathlib` for cross-platform compatibility).
- Implements **error handling** for user input.

---

## **📌 Prerequisites**
Before using this script, you need:
1. A `.zip` archive downloaded from [Intelligence X](https://intelx.io/).  
   - This archive contains **Info.csv** and other extracted dataset files.
2. **Python 3.7 or later** installed on your system.
3. Required Python libraries: `pandas` (all others are built-in).

💡 **Recommended:** Run this script inside a Python **virtual environment** to avoid dependency issues.

---

## **📂 Installation & Setup**
### **🔸 Step 1: Clone the Repository**
```sh
git clone https://github.com/hamzairshad02/IntelXDataExtractor.git
cd IntelXDataExtractor
```

### **🔸 Step 2: Create a Virtual Environment**
A virtual environment ensures package isolation and prevents conflicts.

#### **Windows (PowerShell or CMD)**
```sh
python -m venv intelx_env
intelx_env\Scripts\activate
```

#### **macOS & Linux**
```sh
python3 -m venv intelx_env
source intelx_env/bin/activate
```

---

### **🔸 Step 3: Install Dependencies**
Once inside the virtual environment, install the required packages:
```sh
pip install pandas
pip install openpyxl
```

---

### **🔸 Step 4: Download & Place the Intelligence X Archive**
- Download the `.zip` archive from [Intelligence X](https://intelx.io/).
- Place it in a known directory before running the script.

---

## **⚡ Usage**
### **Run the script**
Execute the script and follow the prompts:
```sh
python Xtract.py
```

### **Input Parameters**
1. **Path to Intelligence X Zip File:**  
   - Example: `C:\Users\YourUser\Downloads\IntelX_Leak.zip` (Windows)  
   - Example: `/home/user/Downloads/IntelX_Leak.zip` (macOS/Linux)  
   - 💡 **Ensure the filename ends with `.zip`**, or the script will alert you with:  
     ```
     Error: The file must be a .zip archive. Please check your input and try again. Make sure the input ends with .zip (e.g. Search 2025-01-27 19_22_10.zip).
     ```

2. **Domain to search for:**  
   - Example: `example.com`

3. **Output folder name:**  
   - Example: `IntelX_Results` (All processed files will be stored in this folder).

---

## **📁 Output Files & Formats**
After execution, the script creates an output folder with these files:

| **Filename**       | **Description** |
|-------------------|---------------|
| `result.xlsx`     | Full extracted data, including **Email, Password, Filename, Date, Phone, Address, Bucket, Media, Content Type, and Size**. |
| `filtered.xlsx`   | **Filtered version** of `result.xlsx`, keeping only the **oldest record** for each **Email + Password** pair to indicate the first leaked instance of the credentials. |
| `credentials.txt` | List of `email:password` pairs. |
| `emails.txt`      | Extracted email addresses. |
| `passwords.txt`   | Extracted passwords. |

---

## **🛠 Troubleshooting**
### **1. Python Not Recognized?**
Ensure Python is installed and added to `PATH`:
```sh
python --version
```
If not found, install [Python](https://www.python.org/downloads/).

### **2. Virtual Environment Not Activating?**
- **Windows:** Use `intelx_env\Scripts\activate.bat` instead of `activate`.
- **macOS/Linux:** Run `chmod +x intelx_env/bin/activate` and try again.

### **3. File Not Found Errors?**
- Ensure the `.zip` file path is correct.
- Use **absolute paths** instead of relative ones.

---

## **📜 License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **📧 Contact & Support**
For any issues or improvements, feel free to open a **GitHub Issue** or reach out.

---
