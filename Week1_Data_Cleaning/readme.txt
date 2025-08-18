🧹 Data Cleaning Assistant

An interactive Streamlit web app to clean messy housing datasets (like the Nashville Housing dataset). This tool automates common data cleaning tasks while letting you preview before-and-after transformations.

🚀 Features

✔️ Upload CSV – Load your dataset directly.
✔️ Standardize Columns – Lowercase, underscores instead of spaces.
✔️ Date Parsing – Convert sale_date to datetime.
✔️ Year Built Cleaning

Converts to numeric.

Removes impossible years (<1800 or > current sale year).

Filters valid years (1800–2023).
✔️ Duplicate Removal – Drop exact duplicate rows.
✔️ Missing Value Handling

Numeric: filled with median (except year_built).

Categorical: filled with mode.
✔️ Sale Price Cleaning – Remove $/commas, convert to numeric, filter extreme values.
✔️ Categorical Fixes – Standardizes casing in land_use.
✔️ Acreage Filter – Remove unrealistic values (≥50 acres).
✔️ Visual Comparison – Before vs After plots (boxplots & histograms).
✔️ Download Cleaned Data – Export as CSV.

📦 Installation

Clone this repository:

git clone https://github.com/HealiMehta/DataWithHeali.git
cd DataWithHeali/Week1_Data_Cleaning


Create & activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


(If requirements.txt doesn’t exist, create one with the following)

streamlit
pandas
matplotlib

▶️ Usage

Run the Streamlit app:

streamlit run app.py


Then open the app in your browser (default: http://localhost:8501).

📊 Example Workflow

Upload your Nashville Housing CSV.

Review the raw data preview.

See a log of cleaning steps applied.

Compare Before vs After distributions for:

Sale Price

Acreage

Year Built

Download the cleaned dataset for further analysis.

🔮 Future Enhancements

Configurable cleaning rules (user-selectable).

Support for additional datasets beyond Nashville Housing.

Advanced outlier detection methods.

Summary statistics report (before vs after).

🧑‍💻 Author

Created by DataWithHeali as part of a Data Science Twitter journey (Week 1: Data Cleaning Glow-Up).
