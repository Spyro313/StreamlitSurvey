import streamlit as st
import pandas as pd
import os

# Config
POINTS_LIMIT = 10
NUM_SLIDERS = 4
CSV_FILE = "votes.csv"

st.title("🗳️ Allocate 10 Points Across 4 Projects")

# Initialize sliders in session state
for i in range(NUM_SLIDERS):
    key = f"slider_{i}"
    if key not in st.session_state:
        st.session_state[key] = 0

# Helper to get total excluding one slider
def total_excluding(index):
    return sum(
        st.session_state[f"slider_{j}"]
        for j in range(NUM_SLIDERS)
        if j != index
    )

# Handle changes: clamp to max allowed
def handle_slider_change(index):
    key = f"slider_{index}"
    current_value = st.session_state[key]
    other_total = total_excluding(index)
    max_allowed = POINTS_LIMIT - other_total

    if current_value > max_allowed:
        st.warning(
            f"Total exceeds {POINTS_LIMIT}. "
            f"Reducing Project {index + 1} to {max_allowed}."
        )
        st.session_state[key] = max_allowed

# Create sliders
for i in range(NUM_SLIDERS):
    key = f"slider_{i}"
    st.slider(
        f"Project {i + 1}",
        min_value=0,
        max_value=10,
        key=key,
        on_change=handle_slider_change,
        args=(i,)
    )

# Show current total
total = sum(st.session_state[f"slider_{i}"] for i in range(NUM_SLIDERS))
st.markdown(f"**Total allocated:** {total} / {POINTS_LIMIT}")

# Submit button
if st.button("✅ Submit and Show Results"):
    if total != POINTS_LIMIT:
        st.error(f"Please allocate exactly {POINTS_LIMIT} points before submitting.")
    else:
        # Store results to CSV
        user_data = {f"Project {i+1}": st.session_state[f"slider_{i}"] for i in range(NUM_SLIDERS)}
        df_new = pd.DataFrame([user_data])

        # Append to file
        if os.path.exists(CSV_FILE):
            df_existing = pd.read_csv(CSV_FILE)
            df_all = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_all = df_new

        df_all.to_csv(CSV_FILE, index=False)

        st.success("Vote submitted!")

        # Show total results
        st.markdown("## 📊 Aggregated Results")
        vote_sums = df_all.sum().sort_index()
        st.bar_chart(vote_sums)

        # Optional: Show raw data table
        with st.expander("📄 See all votes"):
            st.dataframe(df_all)
