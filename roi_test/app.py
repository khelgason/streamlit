import streamlit as st
import plotly.graph_objects as go

# Title of the Streamlit app
st.title("ROI Calculator for Sports Team SaaS")

# Sidebar inputs
st.sidebar.header("Input Parameters")

# Define Club input widgets
st.sidebar.subheader("Club Parameters")
num_players = st.sidebar.slider("Number of Players", min_value=10, max_value=2000, value=500, step=5)
num_orders = st.sidebar.slider("Number of Orders per Month", min_value=1, max_value=1000, value=400)
transaction_fee_avg = st.sidebar.slider("Avg. Transaction Fee", min_value=1, max_value=100, value=20, step=5)

# Hourly rates
st.sidebar.subheader("Cost Parameters")
cost_per_hour_coach = st.sidebar.number_input("Coach Avg. Hourly Rate", min_value=0, value=15)
cost_per_hour_admin = st.sidebar.number_input("Admin Avg. Hourly Rate", min_value=0, value=15)
cost_per_hour_guardian = st.sidebar.number_input("Guardian Avg. Hourly Rate", min_value=0, value=15)
net_transaction = st.toggle("Use Net Transaction Fees", value=1)

if net_transaction:
    st.write("Net fees activated!")
  
# Multiplier definitions
coaches_per_100 = 4.2    # Multiplier for coach for each 100 players
admin_per_100 = 0.9      # Multiplier for admin for each 100 players
guardians_per_100 = 110  # Multiplier for guardians for each 100 players

# Calculations
time_saved_coach = num_players * coaches_per_100/100  # hours saved by coach
time_saved_admin = num_players * admin_per_100/100  # hours saved by admin
time_saved_guardians = num_players * guardians_per_100/100  # hours saved by guardians
better_collection_rate = num_orders * 12 * 0.05  # Annual improvement in collection rate
total_fee_collected = num_orders * transaction_fee_avg

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
