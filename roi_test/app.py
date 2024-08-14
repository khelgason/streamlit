import streamlit as st
import plotly.graph_objects as go

# Title of the Streamlit app
st.title("ROI Calculator for Sports Team SaaS")

# Sidebar inputs
st.sidebar.header("Input Parameters")

# Define input sliders
num_players = st.sidebar.slider("Number of Players", min_value=10, max_value=500, value=100)
num_orders = st.sidebar.slider("Number of Orders per Player", min_value=1, max_value=100, value=10)
transaction_fee = st.sidebar.slider("Transaction Fee (in %)", min_value=0.0, max_value=10.0, value=2.5, step=0.1)

# Calculations
time_saved_coach = num_players * 10  # hours saved
time_saved_admin = num_players * 5   # hours saved
time_saved_guardians = num_players * 2 # hours saved
better_collection_rate = num_orders * num_players * 0.05  # improvement in collection rate
total_fee_collected = num_orders * num_players * (transaction_fee / 100)

# Assuming costs for time (can be adjusted)
cost_per_hour_coach = 50  # dollars per hour
cost_per_hour_admin = 25  # dollars per hour
cost_per_hour_guardian = 15  # dollars per hour

# Total savings
total_savings = (time_saved_coach * cost_per_hour_coach +
                 time_saved_admin * cost_per_hour_admin +
                 time_saved_guardians * cost_per_hour_guardian +
                 better_collection_rate - total_fee_collected)

# Display total cost and net profit
st.write(f"### Total Fee Collected: ${total_fee_collected:.2f}")
st.write(f"### Total Savings: ${total_savings:.2f}")

# Waterfall chart components
cost_benefits = [
    {"label": "Coach Time Saved", "value": time_saved_coach * cost_per_hour_coach},
    {"label": "Admin Time Saved", "value": time_saved_admin * cost_per_hour_admin},
    {"label": "Guardians Time Saved", "value": time_saved_guardians * cost_per_hour_guardian},
    {"label": "Better Collection Rate", "value": better_collection_rate},
    {"label": "Transaction Fee Collected", "value": -total_fee_collected},
]

# Create Waterfall chart
fig = go.Figure(go.Waterfall(
    orientation="v",
    measure=["relative", "relative", "relative", "relative", "relative"],
    x=[item["label"] for item in cost_benefits],
    y=[item["value"] for item in cost_benefits],
    text=[f"${item['value']:.2f}" for item in cost_benefits],
    connector={"line": {"color": "rgb(63, 63, 63)"}},
))

fig.update_layout(
    title="Cost-Benefit Waterfall Chart",
    showlegend=False
)

st.plotly_chart(fig)
