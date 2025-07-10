import streamlit as st
import pandas as pd
import os
import time  # ✅ for sleep

# ----- Config -----
POINTS_LIMIT = 10
NUM_SLIDERS = 4
CSV_FILE = "votes.csv"

st.set_page_config(page_title="Team Vote", layout="centered")

# ----- Title -----
st.title("🗳️ Allocate 10 Points Across 4 Projects")

# ----- Initialize session state -----
if "submitted" not in st.session_state:
    st.session_state.submitted = False

for i in range(NUM_SLIDERS):
    slider_key = f"slider_{i}"
    if slider_key not in st.session_state:
        st.session_state[slider_key] = 0

# ----- Slider change constraint -----
def total_excluding(index):
    return sum(
        st.session_state[f"slider_{j}"]
        for j in range(NUM_SLIDERS)
        if j != index
    )

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

# ----- Voting UI -----
if not st.session_state.submitted:
    for i in range(NUM_SLIDERS):
        st.slider(
            f"Project {i + 1}",
            min_value=0,
            max_value=10,
            key=f"slider_{i}",
            on_change=handle_slider_change,
            args=(i,)
        )

    total = sum(st.session_state[f"slider_{i}"] for i in range(NUM_SLIDERS))
    st.markdown(f"**Total allocated:** {total} / {POINTS_LIMIT}")

    if st.button("✅ Submit and Show Results"):
        if total != POINTS_LIMIT:
            st.error(f"Please allocate exactly {POINTS_LIMIT} points before submitting.")
        else:
            vote_data = {
                f"Project {i+1}": st.session_state[f"slider_{i}"]
                for i in range(NUM_SLIDERS)
            }
            df_new = pd.DataFrame([vote_data])

            if os.path.exists(CSV_FILE):
                df_existing = pd.read_csv(CSV_FILE)
                df_all = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_all = df_new

            df_all.to_csv(CSV_FILE, index=False)

            st.session_state.submitted = True
            st.experimental_rerun()
            st.stop()

# ----- Results UI -----
if st.session_state.submitted:
    st.success("✅ Your vote has been submitted. Chart auto-updates every 10s.")

    if os.path.exists(CSV_FILE):
        df_results = pd.read_csv(CSV_FILE)
        totals = df_results.sum()

        st.markdown("## 📊 Aggregated Results")
        st.bar_chart(totals)

        with st.expander("📄 See all submissions"):
            st.dataframe(df_results)
    else:
        st.info("No votes submitted yet.")

    # ✅ Manual refresh every 10 seconds
    time.sleep(10)
    st.rerun()
