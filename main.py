import streamlit as st

POINTS_LIMIT = 10
NUM_SLIDERS = 7

# Initialize sliders and their previous values
for i in range(NUM_SLIDERS):
    slider_key = f"slider_{i}"
    if slider_key not in st.session_state:
        st.session_state[slider_key] = 0

# Helper function to calculate total excluding one slider
def total_excluding(index):
    return sum(
        st.session_state[f"slider_{j}"]
        for j in range(NUM_SLIDERS)
        if j != index
    )

# Callback to enforce max total
def handle_slider_change(index):
    key = f"slider_{index}"
    current_value = st.session_state[key]
    other_total = total_excluding(index)

    # Max value this slider is allowed to have
    max_allowed = POINTS_LIMIT - other_total

    # If it's too high, clamp it
    if current_value > max_allowed:
        st.warning(
            f"Total exceeds {POINTS_LIMIT}. "
            f"Reducing Project {index + 1} to {max_allowed}."
        )
        st.session_state[key] = max_allowed

# Title
st.title("Distribute 10 Points Across 7 Projects")

# Sliders
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

# Show total
total = sum(st.session_state[f"slider_{i}"] for i in range(NUM_SLIDERS))
st.markdown(f"**Total allocated:** {total} / {POINTS_LIMIT}")
