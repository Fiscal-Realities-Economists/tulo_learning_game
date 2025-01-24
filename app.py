import streamlit as st
import pandas as pd
import numpy as np

# Predefined data for hypothetical First Nations
FIRST_NATION_PROFILES = [
    {
        "name": "Nation A",
        "location": "Rural",
        "population": 1500,
        "settlement_amount": 1000000,
        "initial_success_factors": {
            "Investment Facilitation": 0.6,
            "Economic Opportunity Realization": 0.5,
        },
    },
    {
        "name": "Nation B",
        "location": "Urban",
        "population": 5000,
        "settlement_amount": 5000000,
        "initial_success_factors": {
            "Investment Facilitation": 0.8,
            "Economic Opportunity Realization": 0.7,
        },
    },
]

# Success factor weights
SUCCESS_FACTOR_WEIGHTS = {
    "Education": 1.5,
    "Health": 1.2,
    "Housing": 1.1,
    "Land Purchase & Development": 1.8,
    "Infrastructure": 2.0,
}

# Expenditure profiles
EXPENDITURE_PROFILES = {
    "Education": [
        {"name": "Build Schools", "impact_multiplier": 1.5},
        {"name": "Scholarships", "impact_multiplier": 1.2},
    ],
    "Health": [
        {"name": "Clinics & Hospitals", "impact_multiplier": 1.6},
        {"name": "Health Programs", "impact_multiplier": 1.3},
    ],
    "Housing": [
        {"name": "Affordable Housing", "impact_multiplier": 1.4},
        {"name": "Community Development", "impact_multiplier": 1.2},
    ],
    "Land Purchase & Development": [
        {"name": "Agricultural Land", "impact_multiplier": 2.0},
        {"name": "Commercial Land", "impact_multiplier": 1.7},
    ],
    "Infrastructure": [
        {"name": "Roads & Utilities", "impact_multiplier": 2.2},
        {"name": "Public Infrastructure", "impact_multiplier": 1.9},
    ],
}

def main():
    st.title("Tulo Centre Learning Game")
    st.subheader("Maximizing Realized Economic Impacts from Specific Claims Settlements")

    # Step 1: Choose a Hypothetical First Nation
    st.header("Step 1: Choose a Hypothetical First Nation")
    nation_choice = st.selectbox(
        "Select a First Nation Profile:",
        [nation["name"] for nation in FIRST_NATION_PROFILES],
    )
    selected_nation = next(
        nation for nation in FIRST_NATION_PROFILES if nation["name"] == nation_choice
    )
    st.write(f"Location: {selected_nation['location']}")
    st.write(f"Population: {selected_nation['population']}")
    st.write(f"Settlement Amount: ${selected_nation['settlement_amount']:,.2f}")

    # Step 2: Allocate Settlement Funds
    st.header("Step 2: Allocate Settlement Funds")
    settlement_amount = selected_nation["settlement_amount"]

    per_capita_dist = st.slider(
        "Percentage of settlement for Per Capita Distribution (PCD):", 0, 100, 30
    )
    priority_areas = st.slider(
        "Percentage of settlement for Priority Areas:", 0, 100 - per_capita_dist, 50
    )
    savings = 100 - per_capita_dist - priority_areas

    st.write(f"Allocation Summary:")
    st.write(f"- Per Capita Distribution: {per_capita_dist}%")
    st.write(f"- Priority Areas: {priority_areas}%")
    st.write(f"- Savings: {savings}%")

    # Step 3: PCD Distribution Decisions
    st.header("Step 3: Per Capita Distribution Decisions")
    lump_sum = st.radio(
        "Choose payment type:", ["Lump Sum Payment", "Smaller Payments Over Time"]
    )
    years = 0
    if lump_sum == "Smaller Payments Over Time":
        years = st.slider("Number of years for smaller payments:", 1, 20, 5)
    st.write(f"PCD Payment Type: {lump_sum}")
    if years:
        st.write(f"Duration: {years} years")

    # Step 4: Allocate Priority Areas
    st.header("Step 4: Allocate Priority Areas")
    priorities = {}
    for area in EXPENDITURE_PROFILES.keys():
        priorities[area] = st.slider(f"Percentage for {area}:", 0, 100, 0, key=area)

    # Ensure total allocation does not exceed the budget
    total_priority_allocation = sum(priorities.values())
    if total_priority_allocation > 100:
        st.error("Total allocation for priority areas exceeds 100%. Adjust your sliders.")

    # Step 5: Select Expenditure Profiles
    st.header("Step 5: Select Expenditure Profiles")
    expenditure_choices = {}
    for area, profiles in EXPENDITURE_PROFILES.items():
        choice = st.selectbox(f"Select a profile for {area}:", ["None"] + [p["name"] for p in profiles])
        if choice != "None":
            expenditure_choices[area] = next(p for p in profiles if p["name"] == choice)

    # Step 6: Economic Impact Calculations
    st.header("Step 6: Economic Impact Summary")
    economic_impact = sum(
        (priorities[area] / 100) * settlement_amount * expenditure_choices[area]["impact_multiplier"]
        if area in expenditure_choices else 0
        for area in EXPENDITURE_PROFILES.keys()
    )
    recurring_impact = economic_impact * 0.05  # Assume 5% of the economic impact recurs annually

    st.write(f"Estimated One-Time Economic Impact: ${economic_impact:,.2f}")
    st.write(f"Estimated Annual Recurring Impact: ${recurring_impact:,.2f}")

    # Display Success Factors
    st.subheader("Reassessment of Success Factors")
    updated_factors = {
        factor: value + (economic_impact / settlement_amount) * SUCCESS_FACTOR_WEIGHTS.get(factor, 1.0)
        for factor, value in selected_nation["initial_success_factors"].items()
    }
    st.write("Updated Success Factors:")
    st.json(updated_factors)

    # Visualize Results
    st.subheader("Impact Visualization")
    impact_df = pd.DataFrame(
        {
            "Category": list(priorities.keys()),
            "Allocation (%)": [priorities[area] for area in priorities.keys()],
            "Economic Impact ($)": [
                (priorities[area] / 100) * settlement_amount * expenditure_choices[area]["impact_multiplier"]
                if area in expenditure_choices else 0
                for area in priorities.keys()
            ],
        }
    )
    st.bar_chart(impact_df.set_index("Category"))

    # Iterative Gameplay
    st.header("Step 7: Optimize Your Strategy")
    st.write("Replay the game to explore different strategies and maximize cumulative economic impacts over a 25-30 year horizon.")

if __name__ == "__main__":
    main()
