import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configure Streamlit page
st.set_page_config(page_title="Spotify Data Explorer", layout="wide")

st.title("🎶 Spotify Data Explorer")
st.write("Upload your Spotify dataset and explore insights interactively.")

# --- File uploader ---
uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "parquet"])

if uploaded_file is not None:
    # Load file depending on type
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, encoding_errors="ignore")
    elif uploaded_file.name.endswith(".parquet"):
        df = pd.read_parquet(uploaded_file)

    st.write("Data Preview:", df.head())

    # --- Data Cleaning ---
    if "duration_ms" in df.columns:
        df["duration_min"] = df["duration_ms"] / 60000

    if "year" in df.columns:
        df = df[df["year"] >= 1900]  # remove invalid years
        df["decade"] = (df["year"] // 10) * 10

    # --- Define visualization options ---
    questions = {
        "Are shorter songs more danceable?": "scatter_duration_danceability",
        "Do energetic songs also feel happier?": "scatter_energy_valence",
        "Has the average song duration changed over time?": "line_duration_over_time",
        "How are tempo, energy, and valence distributed?": "hist_features",
        "How does the distribution of tempo vary by decade?": "hist_tempo_decade",
        "How does the distribution of energy vary by decade?": "hist_energy_decade",
        "How does the distribution of valence (happiness) vary by decade?": "hist_valence_decade",
        "How have tempo, energy, and valence changed across decades?": "line_decade_trends",
    }

    # Track which visualizations have been shown
    if "shown" not in st.session_state:
        st.session_state["shown"] = set()

    # --- Reset button ---
    if st.button("🔄 Reset App"):
        st.session_state["shown"] = set()
        st.rerun()

    # --- Bubble CSS ---
    st.markdown("""
        <style>
        .bubble-btn {
            display: inline-block;
            padding: 10px 18px;
            margin: 6px;
            border-radius: 25px;
            background-color: #f0f2f6;
            border: 1px solid #ccc;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 14px;
            text-align: center;
        }
        .bubble-btn:hover {
            background-color: #ff4b4b;
            color: white;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Remaining questions ---
    remaining = {k: v for k, v in questions.items() if v not in st.session_state["shown"]}

    if remaining:
        st.markdown("### 💬 Pick a bubble to pop an insight:")

        for q, viz in remaining.items():
            if st.button(q, key=viz):
                st.session_state["shown"].add(viz)

    # --- Render all selected visualizations ---
    for viz in st.session_state["shown"]:
        st.markdown(f"### 📊 {viz.replace('_',' ').title()}")

        if viz == "hist_features":
            features = ["tempo", "energy", "valence"]
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            for j, feature in enumerate(features):
                sns.histplot(df[feature].dropna(), bins=50, kde=True, color="skyblue", ax=axes[j])
                axes[j].set_title(f"Distribution of {feature.capitalize()}")
                axes[j].set_xlabel(feature.capitalize())
                axes[j].set_ylabel("Count")
            st.pyplot(fig)

        else:
            plt.figure(figsize=(8, 6))
            if viz == "scatter_duration_danceability":
                sns.scatterplot(data=df, x="duration_min", y="danceability", alpha=0.2)
                plt.title("Are shorter songs more danceable?")
                plt.xlabel("Duration (minutes)")
                plt.ylabel("Danceability")

            elif viz == "scatter_energy_valence":
                sns.scatterplot(data=df, x="energy", y="valence", alpha=0.2)
                plt.title("Do energetic songs also feel happier?")
                plt.xlabel("Energy")
                plt.ylabel("Valence (Positivity)")

            elif viz == "line_duration_over_time":
                yearly = df.groupby("year")["duration_min"].mean().dropna()
                yearly = yearly[yearly.index >= 1900]
                plt.plot(yearly.index, yearly.values, marker="o")
                plt.title("Average Song Duration Over Time")
                plt.xlabel("Year")
                plt.ylabel("Average Duration (minutes)")

            elif viz == "hist_tempo_decade":
                sns.histplot(
                    data=df, x="tempo", hue="decade", bins=50,
                    element="step", stat="density", common_norm=False, alpha=0.6
                )
                plt.title("Distribution of Tempo by Decade")
                plt.xlabel("Tempo (BPM)")
                plt.ylabel("Density")

            elif viz == "hist_energy_decade":
                sns.histplot(
                    data=df, x="energy", hue="decade", bins=40,
                    element="step", stat="density", common_norm=False, alpha=0.6
                )
                plt.title("Distribution of Energy by Decade")
                plt.xlabel("Energy")
                plt.ylabel("Density")

            elif viz == "hist_valence_decade":
                sns.histplot(
                    data=df, x="valence", hue="decade", bins=40,
                    element="step", stat="density", common_norm=False, alpha=0.6
                )
                plt.title("Distribution of Valence (Happiness) by Decade")
                plt.xlabel("Valence (0 = Sad, 1 = Happy)")
                plt.ylabel("Density")

            elif viz == "line_decade_trends":
                decade_trends = df.groupby("decade")[["tempo", "energy", "valence"]].mean().reset_index()
                sns.lineplot(data=decade_trends, x="decade", y="tempo", marker="o", label="Tempo")
                sns.lineplot(data=decade_trends, x="decade", y="energy", marker="o", label="Energy")
                sns.lineplot(data=decade_trends, x="decade", y="valence", marker="o", label="Valence")
                plt.title("Average Tempo, Energy, Valence by Decade")
                plt.xlabel("Decade")
                plt.ylabel("Value")
                plt.legend()

            st.pyplot(plt)

    if not remaining:
        st.success("🎉 You’ve popped all the bubbles and explored every insight!")
