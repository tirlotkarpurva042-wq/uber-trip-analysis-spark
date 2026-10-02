import pandas as pd
import matplotlib.pyplot as plt
import os

# Folder for saving charts
output_folder = "../output/charts"
os.makedirs(output_folder, exist_ok=True)


# =========================================================
# 1. BUSINESS VS PERSONAL TRIPS
# =========================================================

category = pd.read_csv("../output/category_analysis.csv")

plt.figure(figsize=(7, 5))

plt.pie(
    category["count"],
    labels=category["CATEGORY"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Business vs Personal Trips")
plt.tight_layout()

plt.savefig(
    output_folder + "/business_vs_personal.png",
    dpi=300
)

plt.show()


# =========================================================
# 2. MONTHLY TRIP TREND
# =========================================================

monthly = pd.read_csv("../output/monthly_analysis.csv")

plt.figure(figsize=(9, 5))

plt.plot(
    monthly["MONTH"],
    monthly["count"],
    marker="o"
)

plt.title("Monthly Uber Trips")
plt.xlabel("Month")
plt.ylabel("Number of Trips")

plt.xticks(range(1, 13))
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    output_folder + "/monthly_trip_trend.png",
    dpi=300
)

plt.show()


# =========================================================
# 3. TRIP PURPOSE ANALYSIS
# =========================================================

purpose = pd.read_csv("../output/purpose_analysis.csv")

purpose = purpose.sort_values(
    by="count",
    ascending=True
)

plt.figure(figsize=(9, 6))

plt.barh(
    purpose["PURPOSE"],
    purpose["count"]
)

plt.title("Trips by Purpose")
plt.xlabel("Number of Trips")
plt.ylabel("Trip Purpose")

plt.tight_layout()

plt.savefig(
    output_folder + "/trip_purpose.png",
    dpi=300
)

plt.show()


# =========================================================
# 4. TOP 10 START LOCATIONS
# =========================================================

start_location = pd.read_csv(
    "../output/start_location_analysis.csv"
)

start_location = start_location.head(10)

plt.figure(figsize=(9, 6))

plt.barh(
    start_location["START"].iloc[::-1],
    start_location["count"].iloc[::-1]
)

plt.title("Top 10 Start Locations")
plt.xlabel("Number of Trips")
plt.ylabel("Start Location")

plt.tight_layout()

plt.savefig(
    output_folder + "/top_start_locations.png",
    dpi=300
)

plt.show()


# =========================================================
# 5. TOP 10 STOP LOCATIONS
# =========================================================

stop_location = pd.read_csv(
    "../output/stop_location_analysis.csv"
)

stop_location = stop_location.head(10)

plt.figure(figsize=(9, 6))

plt.barh(
    stop_location["STOP"].iloc[::-1],
    stop_location["count"].iloc[::-1]
)

plt.title("Top 10 Stop Locations")
plt.xlabel("Number of Trips")
plt.ylabel("Stop Location")

plt.tight_layout()

plt.savefig(
    output_folder + "/top_stop_locations.png",
    dpi=300
)

plt.show()


# =========================================================
# 6. MILES SUMMARY
# =========================================================

miles = pd.read_csv(
    "../output/miles_analysis.csv"
)

miles_values = [
    miles["TOTAL_MILES"].iloc[0],
    miles["AVERAGE_MILES"].iloc[0],
    miles["MINIMUM_MILES"].iloc[0],
    miles["MAXIMUM_MILES"].iloc[0]
]

miles_labels = [
    "Total",
    "Average",
    "Minimum",
    "Maximum"
]

plt.figure(figsize=(8, 5))

plt.bar(
    miles_labels,
    miles_values
)

plt.title("Uber Trip Distance Summary")
plt.xlabel("Measure")
plt.ylabel("Miles")

plt.tight_layout()

plt.savefig(
    output_folder + "/miles_summary.png",
    dpi=300
)

plt.show()


# =========================================================
# 7. DURATION SUMMARY
# =========================================================

duration = pd.read_csv(
    "../output/duration_analysis.csv"
)

duration_values = [
    duration["TOTAL_DURATION_MINUTES"].iloc[0],
    duration["AVERAGE_DURATION_MINUTES"].iloc[0],
    duration["MINIMUM_DURATION_MINUTES"].iloc[0],
    duration["MAXIMUM_DURATION_MINUTES"].iloc[0]
]

duration_labels = [
    "Total",
    "Average",
    "Minimum",
    "Maximum"
]

plt.figure(figsize=(8, 5))

plt.bar(
    duration_labels,
    duration_values
)

plt.title("Uber Trip Duration Summary")
plt.xlabel("Measure")
plt.ylabel("Duration (Minutes)")

plt.tight_layout()

plt.savefig(
    output_folder + "/duration_summary.png",
    dpi=300
)

plt.show()


print()
print("========================================")
print("ALL VISUALIZATIONS CREATED SUCCESSFULLY")
print("========================================")
print("Charts saved in: ../output/charts/")