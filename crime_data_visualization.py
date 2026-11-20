"""
=====================================================================
 PROJECT   : Crime Data Visualization
             (Crime types by year and area using stacked bar charts)
 SUBMITTED BY : Ashutosh Varshney
                2026B01010220
 COURSE    : B.Tech (1st Year) - Mini Project
 LIBRARIES : Python, Pandas, NumPy, Matplotlib
=====================================================================

HOW TO RUN
  1. Install libraries (only once):
         pip install pandas numpy matplotlib
  2. Run this file:
         python crime_data_visualization.py
  3. Output:
         - crime_data.csv          (the dataset)
         - chart1_crime_by_year.png
         - chart2_crime_by_area.png
         - chart3_area_by_year.png
         - chart4_percentage_by_year.png

NOTE
  If you have a real dataset (e.g. from data.gov.in or Kaggle), save it
  as 'crime_data.csv' with these 4 columns and the program will use it:
         Year, Area, Crime_Type, Cases
"""

# ---------------------------------------------------------------
# STEP 1 : Import the libraries
# ---------------------------------------------------------------
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------
# STEP 2 : Create (or load) the dataset
# ---------------------------------------------------------------
FILE_NAME = "crime_data.csv"


def create_sample_data():
    """Create a sample crime dataset using NumPy random numbers.
    (Used only when no real CSV file is available.)"""
    np.random.seed(42)  # seed makes the random numbers repeat every run

    years = [2018, 2019, 2020, 2021, 2022, 2023]
    areas = ["Central", "North", "South", "East", "West"]
    crime_types = ["Theft", "Burglary", "Assault", "Robbery", "Fraud", "Vandalism"]

    rows = []
    for year in years:
        for area in areas:
            for crime in crime_types:
                # base number of cases for each crime type
                base = {"Theft": 220, "Burglary": 90, "Assault": 110,
                        "Robbery": 60, "Fraud": 70, "Vandalism": 80}[crime]
                # Fraud grows every year (online fraud is increasing)
                if crime == "Fraud":
                    base = base + (year - 2018) * 25
                # 2020 had a lockdown, so street crimes were lower
                if year == 2020 and crime in ["Theft", "Robbery", "Assault"]:
                    base = base * 0.6
                # Central area is busier, so it has more crime
                if area == "Central":
                    base = base * 1.3
                # add a little randomness
                cases = int(base + np.random.randint(-20, 21))
                rows.append([year, area, crime, cases])

    df = pd.DataFrame(rows, columns=["Year", "Area", "Crime_Type", "Cases"])
    df.to_csv(FILE_NAME, index=False)
    print("Sample dataset created and saved as", FILE_NAME)
    return df


if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    print("Dataset loaded from", FILE_NAME)
else:
    df = create_sample_data()


# ---------------------------------------------------------------
# STEP 3 : Explore the data (Pandas basics)
# ---------------------------------------------------------------
print("\n----- First 5 rows -----")
print(df.head())

print("\n----- Shape (rows, columns) -----")
print(df.shape)

print("\n----- Data types and info -----")
print(df.dtypes)

print("\n----- Missing values in each column -----")
print(df.isnull().sum())

print("\n----- Statistical summary of Cases -----")
print(df["Cases"].describe())


# ---------------------------------------------------------------
# STEP 4 : Clean the data
# ---------------------------------------------------------------
df = df.drop_duplicates()          # remove repeated rows
df = df.dropna()                   # remove rows with missing values
df["Cases"] = df["Cases"].astype(int)
df["Year"] = df["Year"].astype(int)
print("\nData cleaned. Rows after cleaning:", len(df))


# ---------------------------------------------------------------
# STEP 5 : Analyse the data (groupby, pivot_table, NumPy)
# ---------------------------------------------------------------
# Total cases per year
total_by_year = df.groupby("Year")["Cases"].sum()
print("\n----- Total crimes per year -----")
print(total_by_year)

# Total cases per area
total_by_area = df.groupby("Area")["Cases"].sum().sort_values(ascending=False)
print("\n----- Total crimes per area -----")
print(total_by_area)

# Total cases per crime type
total_by_type = df.groupby("Crime_Type")["Cases"].sum().sort_values(ascending=False)
print("\n----- Total crimes per crime type -----")
print(total_by_type)

# Pivot tables : these are the tables used for stacked bar charts
# (rows = what goes on the X-axis, columns = the stacked parts)
year_vs_type = df.pivot_table(index="Year", columns="Crime_Type",
                              values="Cases", aggfunc="sum")
area_vs_type = df.pivot_table(index="Area", columns="Crime_Type",
                              values="Cases", aggfunc="sum")
year_vs_area = df.pivot_table(index="Year", columns="Area",
                              values="Cases", aggfunc="sum")

print("\n----- Pivot table : Year vs Crime Type -----")
print(year_vs_type)

# Some quick facts using NumPy
cases_array = df["Cases"].to_numpy()
print("\n----- NumPy quick facts -----")
print("Average cases per record :", round(np.mean(cases_array), 2))
print("Median cases per record  :", np.median(cases_array))
print("Maximum cases            :", np.max(cases_array))
print("Minimum cases            :", np.min(cases_array))
print("Standard deviation       :", round(np.std(cases_array), 2))

# Percentage change from first to last year
first_year, last_year = total_by_year.index[0], total_by_year.index[-1]
change = (total_by_year[last_year] - total_by_year[first_year]) / total_by_year[first_year] * 100
print(f"\nTotal crime change from {first_year} to {last_year}: {change:.2f}%")

print("Most common crime overall :", total_by_type.idxmax())
print("Area with most crime      :", total_by_area.idxmax())
print("Year with most crime      :", total_by_year.idxmax())
print("Year with least crime     :", total_by_year.idxmin())


# ---------------------------------------------------------------
# STEP 6 : Visualisation - Stacked bar charts
# ---------------------------------------------------------------
# A stacked bar chart places the parts of a total on top of each other.
# In Pandas we only need:  table.plot(kind="bar", stacked=True)

colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]


# ---- Chart 1 : Crime types by YEAR (stacked) ----
ax = year_vs_type.plot(kind="bar", stacked=True, figsize=(10, 6),
                       color=colors, edgecolor="white")
ax.set_title("Crime Types by Year (Stacked Bar Chart)", fontsize=14, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Cases")
ax.legend(title="Crime Type", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart1_crime_by_year.png", dpi=150)
plt.show()


# ---- Chart 2 : Crime types by AREA (stacked) ----
ax = area_vs_type.plot(kind="bar", stacked=True, figsize=(10, 6),
                       color=colors, edgecolor="white")
ax.set_title("Crime Types by Area (Stacked Bar Chart)", fontsize=14, fontweight="bold")
ax.set_xlabel("Area")
ax.set_ylabel("Number of Cases")
ax.legend(title="Crime Type", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart2_crime_by_area.png", dpi=150)
plt.show()


# ---- Chart 3 : Areas stacked within each YEAR ----
ax = year_vs_area.plot(kind="bar", stacked=True, figsize=(10, 6),
                       colormap="Set2", edgecolor="white")
ax.set_title("Total Crimes per Year Split by Area", fontsize=14, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Cases")
ax.legend(title="Area", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart3_area_by_year.png", dpi=150)
plt.show()


# ---- Chart 4 : 100% stacked bar (share of each crime type per year) ----
percent_table = year_vs_type.div(year_vs_type.sum(axis=1), axis=0) * 100
ax = percent_table.plot(kind="bar", stacked=True, figsize=(10, 6),
                        color=colors, edgecolor="white")
ax.set_title("Share of Each Crime Type per Year (%)", fontsize=14, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Percentage of Total Cases")
ax.legend(title="Crime Type", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart4_percentage_by_year.png", dpi=150)
plt.show()


# ---------------------------------------------------------------
# STEP 7 : Conclusion printed on screen
# ---------------------------------------------------------------
print("\n================ CONCLUSION ================")
print("1. Most common crime  :", total_by_type.idxmax())
print("2. Most affected area :", total_by_area.idxmax())
print("3. Highest crime year :", total_by_year.idxmax())
print("4. Lowest crime year  :", total_by_year.idxmin())
print("5. Change from", first_year, "to", last_year, ":", round(change, 2), "%")
print("All charts have been saved as PNG files.")
