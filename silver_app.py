import streamlit as st

st.title("Silver Calculator")

# Inputs and Static Values #

# Troy
troy_weight = st.number_input("Troy Weight (oz)", value=0.0, key="troy_weight")
troy_ounce: float = 0.9115 # Of an Avoirdupois ounce

# Avoirdupois
adp_weight = st.number_input("Adp Weight (oz)", value=0.0, key="adp_weight")
adp_ounce: float = 1.0971 # Of a Troy Ounce

# Metric
metric_weight = st.number_input("Metric Weight (gr)", value=0.0, key="metric_weight")
grams_per_Troy: float = 31.1035 # Grams in a Troy Ounce

# Silver Static Values
sterling_silver: float = 0.925
brittania_silver: float  = 0.958

# Other inputs
silver_spot_price = st.number_input("Spot Price ($)",
                        value=0.000,
                        step=0.001,
                        format="%.3f",
                        key="silver_spot_price")

gbp_usd = st.number_input("GBP USD ($)",
                        value=0.0,
                        step=0.001,
                        format="%.3f",
                        key="gbp_usd")

# Other variables
troy_convert = 0.0
sterling_value = 0.0
st_conv_value = 0.0
st_silver_content = 0.0
br_silver_content = 0.0

if gbp_usd != 0:
    st_conv_value = 1 / gbp_usd
else:
    st_conv_value = 0

col1, col2 = st.columns(2)

with col1:
    if st.button("Calculate"):
        # Troy calcs
        if troy_weight != 0:
            st_silver_content = sterling_silver * troy_weight
            sterling_value = (st_silver_content * silver_spot_price) * st_conv_value
            st.success(f"Sterling Melt Value (Troy)= £{sterling_value:,.2f}")

            br_silver_content = brittania_silver * troy_weight
            brittania_value = (br_silver_content * silver_spot_price) * st_conv_value
            st.success(f"Brittania Melt Value (Troy)= £{brittania_value:,.2f}")

        # ADP calcs
        elif adp_weight != 0:
            troy_convert = troy_ounce * adp_weight
            # print(troy_convert)
            st_silver_content = troy_convert * sterling_silver
            sterling_value = (st_silver_content * silver_spot_price) * st_conv_value
            st.success(f"Sterling Melt Value (ADP)= £{sterling_value:,.2f}")

            # troy_convert = troy_ounce * adp_weight
            br_silver_content = troy_convert * brittania_silver
            brittania_value = (br_silver_content * silver_spot_price) * st_conv_value
            st.success(f"Brittania Melt Value (ADP)= £{brittania_value:,.2f}")

        # Gram calcs
        elif metric_weight != 0:
            troy_convert = metric_weight/grams_per_Troy
            st_silver_content = troy_convert * sterling_silver
            sterling_value = (st_silver_content * silver_spot_price) * st_conv_value
            st.success(f"Sterling Melt Value (Gr)= £{sterling_value:,.2f}")

            # troy_convert = metric_weight/grams_per_Troy
            br_silver_content = troy_convert * brittania_silver
            brittania_value = (br_silver_content * silver_spot_price) * st_conv_value
            st.success(f"Brittania Melt Value (Gr)= £{brittania_value:,.2f}")

def clear_inputs():
    st.session_state["troy_weight"] = 0.0
    st.session_state["adp_weight"] = 0.0
    st.session_state["metric_weight"] = 0.0
    st.session_state["silver_spot_price"] = 0.0
    st.session_state["gbp_usd"] = 0.0

with col2:
    st.button(
        "Clear",
        on_click=clear_inputs
    )







