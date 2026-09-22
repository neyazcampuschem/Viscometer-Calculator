import streamlit as st

# ==========================================
# PAGE CONFIGURATION & DARK THEME STYLING
# ==========================================
st.set_page_config(
    page_title="Viscosity Calculator | AMU",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI styling
st.markdown("""
    <style>
    /* Main App Canvas - Clean, modern light slate */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }

    /* Sidebar - Dark, elegant slate base */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }

    /* Sidebar text readability */
    [data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }

    /* Result Cards - Dark cool blue-gray contrast blocks */
    .result-card {
        background-color: #1e293b;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -4px rgba(15, 23, 42, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 20px -3px rgba(15, 23, 42, 0.12);
    }

    .result-title {
        color: #94a3b8;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    /* Accent color - Vivid Sky Blue for key figures */
    .result-value {
        color: #38bdf8;
        font-size: 32px;
        font-weight: 800;
        line-height: 1.1;
    }

    .result-unit {
        color: #64748b;
        font-size: 13px;
        margin-top: 4px;
    }

    /* Formula / Accent Box */
    .formula-box {
        background-color: #ffffff;
        border-left: 4px solid #0284c7;
        border-top: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        padding: 16px;
        border-radius: 0 8px 8px 0;
        margin-top: 20px;
        color: #334155;
        font-size: 14px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)
# ==========================================
# SIDEBAR: CREDITS PANEL (LEFT SIDE)
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/2/23/Aligarh_Muslim_University_logo.png", width=100)
    st.markdown("### 🧪 Viscosity Calculator")
    st.markdown("---")
    
    st.caption("DESIGNED BY")
    st.markdown("**Neyaz Reza**")
    
    st.caption("UNDER THE SUPERVISION OF")
    st.markdown("**Mr. Mohammad Abdul Hakeem**")
    
    st.markdown("---")
    st.markdown("🏛️ **Department of Chemical Engineering**")
    st.markdown("🏫 **Aligarh Muslim University**")

# ==========================================
# MAIN PANEL: CALCULATOR INTERFACE (RIGHT SIDE)
# ==========================================
st.title("Dynamic & Kinematic Viscosity Calculator")
st.markdown("Calculate fluid viscosity based on standard industrial viscometer physical models.")

st.markdown("---")

# Layout: 2 Columns for inputs
col1, col2 = st.columns([1, 1])

with col1:
    v_type = st.selectbox(
        "Select Viscometer Type:",
        [
            "Rotational (Brookfield)",
            "Glass Capillary (Ubbelohde/Ostwald)",
            "Falling Ball (Höppler/Stokes)",
            "Efflux Cup (Ford Cup #4)"
        ]
    )

with col2:
    rho = st.number_input(
        "Fluid Density (g/cm³):",
        min_value=0.01,
        value=0.95,
        step=0.01,
        format="%.3f"
    )

st.markdown("#### Input Parameters")

# Dynamic Input Fields based on Viscometer Selection
dynamic_viscosity = 0.0
kinematic_viscosity = 0.0
formula_text = ""

if "Rotational" in v_type:
    c_input1, c_input2 = st.columns(2)
    with c_input1:
        torque = st.slider("Torque (%)", min_value=1.0, max_value=100.0, value=45.0, step=0.5)
    with c_input2:
        factor = st.number_input("Spindle Factor Constant:", min_value=0.1, value=20.0, step=0.5)
    
    dynamic_viscosity = torque * factor
    kinematic_viscosity = dynamic_viscosity / rho
    formula_text = "Formula: Dynamic Viscosity = Torque (%) × Spindle Factor"

elif "Capillary" in v_type:
    c_input1, c_input2 = st.columns(2)
    with c_input1:
        t = st.number_input("Flow Time (seconds):", min_value=0.1, value=120.0, step=1.0)
    with c_input2:
        C = st.number_input("Tube Constant (cSt/s):", min_value=0.0001, value=0.05, step=0.001, format="%.4f")
    
    kinematic_viscosity = C * t
    dynamic_viscosity = kinematic_viscosity * rho
    formula_text = "Formula: Kinematic Viscosity = Tube Constant (C) × Flow Time (t)"

elif "Falling Ball" in v_type:
    c_input1, c_input2 = st.columns(2)
    with c_input1:
        r_mm = st.number_input("Sphere Radius (mm):", min_value=0.1, value=5.0, step=0.1)
        rho_s = st.number_input("Sphere Density (g/cm³):", min_value=0.1, value=7.8, step=0.1)
    with c_input2:
        dist_cm = st.number_input("Fall Distance (cm):", min_value=0.1, value=10.0, step=0.5)
        t_sec = st.number_input("Fall Time (seconds):", min_value=0.1, value=2.5, step=0.1)
    
    if t_sec > 0 and dist_cm > 0:
        r = r_mm / 1000.0                       # m
        rho_s_si = rho_s * 1000.0              # kg/m³
        rho_f_si = rho * 1000.0                # kg/m³
        dist = dist_cm / 100.0                  # m
        g = 9.81                               # m/s²
        v = dist / t_sec                       # m/s

        dynamic_pas = (2 * (r**2) * (rho_s_si - rho_f_si) * g) / (9 * v)
        dynamic_viscosity = max(0.0, dynamic_pas * 1000.0)
        kinematic_viscosity = dynamic_viscosity / rho
    formula_text = "Formula (Stokes' Law): µ = [2r²(ρ_s - ρ_f)g] / 9v"

elif "Efflux Cup" in v_type:
    t = st.number_input("Drain Time (seconds):", min_value=1.0, value=45.0, step=0.5)
    if t > 0:
        kinematic_viscosity = max(0.0, (3.85 * t) - (240.0 / t))
        dynamic_viscosity = kinematic_viscosity * rho
    formula_text = "Formula (Ford Cup #4): Kinematic (cSt) = 3.85t - (240/t)"

# ==========================================
# RESULTS DISPLAY CARDS
# ==========================================
st.markdown("---")
st.markdown("#### Calculated Results")

res_col1, res_col2 = st.columns(2)

with res_col1:
    st.markdown(f"""
        <div class="result-card">
            <div class="result-title">DYNAMIC VISCOSITY</div>
            <div class="result-value">{dynamic_viscosity:.2f} cP</div>
            <div class="result-unit">or mPa·s</div>
        </div>
    """, unsafe_allow_html=True)

with res_col2:
    st.markdown(f"""
        <div class="result-card">
            <div class="result-title">KINEMATIC VISCOSITY</div>
            <div class="result-value">{kinematic_viscosity:.2f} cSt</div>
            <div class="result-unit">or mm²/s</div>
        </div>
    """, unsafe_allow_html=True)

# Live Formula Note
st.markdown(f"""
    <div class="formula-box">
        <b>Equation Used:</b> {formula_text}
    </div>
""", unsafe_allow_html=True)
