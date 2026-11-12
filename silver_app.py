import streamlit as st
import yfinance as yf

st.title("Silver Calculator")

st.markdown("""
<style>
html, body, [class*="css"], code {
    font-family: "Segoe UI", sans-serif !important;
}

/* Tighten the space under the title */
h1 {
    padding-bottom: 1rem !important;
    margin-bottom: 0 !important;
}

/* Collapse the invisible element that holds this <style> block */
div[data-testid="stElementContainer"]:has(> div[data-testid="stMarkdown"] style),
div[data-testid="stElementContainer"]:has(style) {
    display: none;
}

/* Pull the whole page up */

header[data-testid="stHeader"] {
    display: none;
}

.block-container,
[data-testid="stMainBlockContainer"] {
    padding-top: 4rem !important;
}

/* Trim the gap above the title */
h1 {
    padding-top: 0 !important;
}
</style>
""", unsafe_allow_html=True)

if "silver_spot_price" not in st.session_state:
    st.session_state.silver_spot_price = 0.0

if "gbp_usd" not in st.session_state:
    st.session_state.gbp_usd = 0.0

if "gold_spot_price" not in st.session_state:
    st.session_state.gold_spot_price = 0.0

if "dow_jones" not in st.session_state:
    st.session_state.dow_jones = 0.0

if "prices_loaded" not in st.session_state:
    st.session_state.prices_loaded = False

@st.cache_data(ttl=300)
def latest_close(symbol: str) -> float:
    df = yf.Ticker(symbol).history(period="5d")
    closes = df["Close"].dropna()
    if closes.empty:
        raise ValueError(f"No data returned for {symbol}")
    return float(closes.iloc[-1])

if st.button("Retrieve Latest Gold, Silver & USD Prices"):
    try:
        st.session_state.silver_spot_price = round(latest_close("SI=F"), 3)
        st.session_state.gold_spot_price = round(latest_close("GC=F"), 3)
        st.session_state.gbp_usd = round(latest_close("GBPUSD=X"), 3)
        st.session_state.dow_jones = round(latest_close("^DJI"), 3)

        st.session_state.prices_loaded = True

    except Exception as e:
        st.error(f"Failed to retrieve prices: {e}. You can enter them manually below.")

st.number_input("Spot Price ($/troy oz)", min_value=0.0, step=0.001,
                format="%.3f", key="silver_spot_price")
st.number_input("GBP USD ($)", min_value=0.0, step=0.0001,
                format="%.4f", key="gbp_usd")
st.number_input("Gold Spot Price ($/troy oz)", min_value=0.0, step=0.001,
                format="%.3f", key="gold_spot_price")

prices_available = (st.session_state.silver_spot_price > 0
                    and st.session_state.gbp_usd > 0
                    and st.session_state.gold_spot_price > 0)

dj_available = (st.session_state.dow_jones > 0
                and st.session_state.gold_spot_price > 0)

# Gold/Silver & DJ/Gold Ratio
gold_silver_ratio = 0.0
dj_gold_ratio = 0.0

if prices_available: 
    gold_silver_ratio = (st.session_state.gold_spot_price
                         / st.session_state.silver_spot_price)

if dj_available: 
    dj_gold_ratio = (st.session_state.dow_jones / st.session_state.gold_spot_price)

if prices_available: 
    st.success(
        f"Gold, Silver & USD prices retrieved successfully. "
        f"Silver: \\${st.session_state.silver_spot_price:.2f} per oz, "
        f"Gold: \\${st.session_state.gold_spot_price:.2f} per oz, "
        f"GBP/USD: {st.session_state.gbp_usd:.4f}, "
        f"Gold/Silver Ratio: {gold_silver_ratio:.2f}, "
        f"Dow Jones/Gold Ratio: {dj_gold_ratio:.2f}"
    )

# st.stop()

# Static Values #

# Troy
troy_ounce: float = 0.9115 # Of an Avoirdupois ounce

# Avoirdupois
# adp_ounce: float = 1.0971 # Of a Troy Ounce

# Metric
grams_per_Troy: float = 31.1035 # Grams in a Troy Ounce

# Silver Static Values
sterling_silver: float = 0.925
brittania_silver: float  = 0.958

# Weight inputs

weight_type = st.selectbox(
    "Weight Type",
    [
        "Troy Ounces",
        "Avoirdupois Ounces",
        "Grams"
    ],
    key="weight_type",
    disabled=not prices_available
)

weight = 0.0

if weight_type == "Troy Ounces":
    weight = st.number_input(
        "Troy Weight (oz)",
        min_value=0.0,
        value=0.0,
        key="troy_weight",
        disabled=not prices_available
    )

elif weight_type == "Avoirdupois Ounces":
    weight = st.number_input(
        "Avoirdupois Weight (oz)",
        min_value=0.0,
        value=0.0,
        key="adp_weight",
        disabled=not prices_available
    )

elif weight_type == "Grams":
    weight = st.number_input(
        "Metric Weight (g)",
        min_value=0.0,
        value=0.0,
        key="metric_weight",
        disabled=not prices_available
    )

# Other variables
troy_convert = 0.0
sterling_value = 0.0
st_conv_value = 0.0
st_silver_content = 0.0
br_silver_content = 0.0

if st.session_state.gbp_usd != 0:
    st_conv_value = round(1 / st.session_state.gbp_usd, 3)
else:
    st_conv_value = 0

col1, col2 = st.columns(2)

with col1:
    if st.button("Calculate", disabled=not prices_available):
        # Troy calcs
        if weight_type == "Troy Ounces":
            troy_convert = round(weight, 2)
        elif weight_type == "Avoirdupois Ounces":
            troy_convert = round(weight * troy_ounce, 2)
        elif weight_type == "Grams":
            troy_convert = round(weight / grams_per_Troy, 2)

        # st.write("Troy Convert is:", troy_convert)
        # st.write("Dow Jones is:", st.session_state.dow_jones)
        
        st_silver_content = round(sterling_silver * troy_convert, 2)
        # st.write("st_silver_content:", st_silver_content)
        sterling_value = (st_silver_content * st.session_state.silver_spot_price) * st_conv_value
        
        st.success(f"Sterling Melt Value = £{sterling_value:,.2f}")

        # st.write("Silver Price:", st.session_state.silver_spot_price)
        # st.write("GBP/USD:", st.session_state.gbp_usd)
        # st.write("Weight:", weight)
        # st.write("Conversion:", st_conv_value)

        br_silver_content = round(brittania_silver * troy_convert, 2)
        # st.write("br_silver_content:", br_silver_content)
        brittania_value = (br_silver_content * st.session_state.silver_spot_price) * st_conv_value
        
        st.success(f"Brittania Melt Value = £{brittania_value:,.2f}")

def clear_inputs():

    st.session_state.prices_loaded = False

    st.session_state["silver_spot_price"] = 0.0
    st.session_state["gold_spot_price"] = 0.0
    st.session_state["gbp_usd"] = 0.0
    st.session_state["dow_jones"] = 0.0

    st.session_state["weight_type"] = "Troy Ounces"

    if "troy_weight" in st.session_state:
        st.session_state["troy_weight"] = 0.0

    if "adp_weight" in st.session_state:
        st.session_state["adp_weight"] = 0.0

    if "metric_weight" in st.session_state:
        st.session_state["metric_weight"] = 0.0

with col2:
    st.button(
        "Clear",
        on_click=clear_inputs
    )







