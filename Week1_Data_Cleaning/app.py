import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



st.set_page_config(page_title="🧹 Data Cleaning Tool", layout="wide")
st.title("🧹 Data Cleaning Assistant")

# --- Upload CSV ---
uploaded_file = st.file_uploader("Upload your CSV data file", type=["csv"])


if uploaded_file is not None:
    # Load raw data
    df_raw = pd.read_csv(uploaded_file)
    st.write("### 📊 Raw Data Preview", df_raw.head())

    # Keep copy for comparison
    df = df_raw.copy()

    # --- Cleaning Logs ---
    logs = []

    # 🔹 Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    logs.append("Standardized column names (lowercase, underscores).")

    # 🔹 Convert date columns
    if "sale_date" in df.columns:
        df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
        logs.append("Converted `sale_date` to datetime format.")

    # --- YEAR BUILT: clean & DO NOT globally impute ---
    if "year_built" in df.columns:
        # Coerce to numeric and treat impossible values as missing
        df["year_built"] = pd.to_numeric(df["year_built"], errors="coerce")
        # Common bad entries are 0 or tiny years; mark them missing
        df.loc[df["year_built"] < 1800, "year_built"] = pd.NA

        # If sale_date exists, ensure year_built <= sale year
        if "sale_date" in df.columns:
            sale_year = df["sale_date"].dt.year
            df.loc[df["year_built"] > sale_year, "year_built"] = pd.NA

        logs.append("Cleaned `year_built` (coerced to numeric, removed impossible/future years).")

    # 🔹 Remove duplicates
    dupes = df.duplicated().sum()
    if dupes > 0:
        df = df.drop_duplicates()
        logs.append(f"Removed {dupes} duplicate rows.")

    # --- Handle missing values: SKIP year_built here ---
    missing_before = int(df.isnull().sum().sum())

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    numeric_to_impute = [c for c in numeric_cols if c != "year_built"]
    for col in numeric_to_impute:
        df[col].fillna(df[col].median(), inplace=True)

    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        if df[col].isnull().any():
            df[col].fillna(df[col].mode().iloc[0], inplace=True)

    missing_after = int(df.isnull().sum().sum())
    fixed = missing_before - missing_after
    if fixed > 0:
        logs.append(f"Filled {fixed} missing values (median/mode), excluding `year_built`.")



    # 🔹 Remove symbols & convert sale_price
    if "sale_price" in df.columns:
        df["sale_price"] = df["sale_price"].replace('[\$,]', '', regex=True).astype(float)
        logs.append("Converted `sale_price` to numeric (removed $ and commas).")

        # Outlier removal
        before = len(df)
        df = df[df["sale_price"].between(1000, 5_000_000)]
        logs.append(f"Filtered extreme sale_price values. Removed {before - len(df)} rows.")

    # 🔹 Fix categorical inconsistencies
    if "land_use" in df.columns:
        df["land_use"] = df["land_use"].str.title()
        logs.append("Standardized text casing in `land_use` column.")

    # --- YEAR BUILT: clean same as notebook ---
    if "year_built" in df.columns:
        # Convert to numeric
        df["year_built"] = pd.to_numeric(df["year_built"], errors="coerce")

        # Filter valid years
        before = len(df)
        df = df[(df["year_built"] >= 1800) & (df["year_built"] <= 2023)]
        logs.append(f"Filtered invalid `year_built` values (kept between 1800–2023). Removed {before - len(df)} rows.")


    # 🔹 Acreage filter
    if "acreage" in df.columns:
        before = len(df)
        df = df[df["acreage"] < 50]
        logs.append(f"Removed extreme `acreage` values. Removed {before - len(df)} rows.")

  

    st.subheader("📝 Cleaning Steps Performed")
    for log in logs:
        st.success(log)



    # --- Before vs After Plots (side-by-side grid) ---
    st.subheader("📉 Before vs After Distributions")

    fig, axes = plt.subplots(3, 2, figsize=(14, 12))

    # Sale Price
    if "Sale Price" in df_raw.columns and "sale_price" in df.columns:
        df_raw_sp = pd.to_numeric(df_raw["Sale Price"].replace('[\$,]', '', regex=True), errors="coerce")
        df_raw_sp.plot(kind="box", ax=axes[0, 0], title="Before: Sale Price")
        df["sale_price"].plot(kind="box", ax=axes[0, 1], title="After: Sale Price")

    # Acreage
    if "Acreage" in df_raw.columns and "acreage" in df.columns:
        pd.to_numeric(df_raw["Acreage"], errors="coerce").plot(kind="box", ax=axes[1, 0], title="Before: Acreage")
        df["acreage"].plot(kind="box", ax=axes[1, 1], title="After: Acreage")

    # Year Built (use dropna to avoid spikes from imputation)
    if "Year Built" in df_raw.columns and "year_built" in df.columns:
        yb_before = pd.to_numeric(df_raw["Year Built"], errors="coerce")
        yb_before = yb_before[(yb_before >= 1800) & (yb_before <= 2023)]
        axes[2, 0].hist(yb_before.dropna(), bins=50)
        axes[2, 0].set_title("Before: Year Built")

        yb_after = df["year_built"]
        yb_after = yb_after[(yb_after >= 1800) & (yb_after <= 2023)]
        axes[2, 1].hist(yb_after.dropna(), bins=50)
        axes[2, 1].set_title("After: Year Built")

    plt.tight_layout()
    st.pyplot(fig)

    # --- Final Preview ---
    st.subheader("✅ Cleaned Data Preview")
    st.dataframe(df.head())

    # --- Download Button ---
    st.download_button(
        "⬇️ Download Cleaned CSV",
        df.to_csv(index=False).encode("utf-8"),
        "nashville_cleaned.csv",
        "text/csv"
    )
