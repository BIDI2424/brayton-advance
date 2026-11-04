import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# MESTI JADI ARAHAN PERTAMA STREAMLIT
st.set_page_config(
    page_title="Advanced Brayton Cycle Simulator (KJM442)", 
    layout="wide"
)

st.title("🔥 Advanced Brayton Cycle Interactive Simulator (KJM442)")
st.markdown("A comprehensive educational tool for analyzing Ideal, Actual, and Regenerative Brayton Cycles for gas turbine engines.")

# --- NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs([
    "🔥 1. Ideal Brayton Cycle", 
    "⚙️ 2. Actual Brayton Cycle (Isentropic)", 
    "🔄 3. Regenerative Brayton Cycle"
])

# =====================================================================
# TAB 1: IDEAL BRAYTON CYCLE
# =====================================================================
with tab1:
    st.header("Ideal Brayton Cycle Analysis")
    st.markdown("Standard air-standard ideal cycle assuming isentropic compression and expansion.")

    col_sidebar1, col_main1 = st.columns([1, 3])

    with col_sidebar1:
        st.subheader("Parameters")
        p1_1 = st.slider("Initial Pressure, P1 (kPa)", 50.0, 200.0, 100.0, 5.0, key="i_p1")
        t1_1 = st.slider("Initial Temperature, T1 (K)", 250.0, 400.0, 300.0, 5.0, key="i_t1")
        rp_1 = st.slider("Pressure Ratio (rp)", 2.0, 30.0, 10.0, 0.5, key="i_rp")
        t3_1 = st.slider("Max Turbine Inlet Temp, T3 (K)", 800.0, 1800.0, 1200.0, 10.0, key="i_t3")
        k_1 = st.slider("Specific Heat Ratio (k)", 1.2, 1.67, 1.4, 0.01, key="i_k")

    # Calculations (Ideal)
    cp = 1.005
    p2_1 = p1_1 * rp_1
    t2_1 = t1_1 * (rp_1 ** ((k_1 - 1) / k_1))
    p3_1 = p2_1
    p4_1 = p1_1
    t4_1 = t3_1 / (rp_1 ** ((k_1 - 1) / k_1))

    q_in_1 = cp * (t3_1 - t2_1)
    q_out_1 = cp * (t4_1 - t1_1)
    w_net_1 = q_in_1 - q_out_1
    eta_th_1 = w_net_1 / q_in_1
    w_comp_1 = cp * (t2_1 - t1_1)
    w_turb_1 = cp * (t3_1 - t4_1)
    bwr_1 = w_comp_1 / w_turb_1

    with col_main1:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Thermal Efficiency", f"{eta_th_1 * 100:.2f}%")
        m2.metric("Back Work Ratio (BWR)", f"{bwr_1:.4f}")
        m3.metric("Net Work Output", f"{w_net_1:.2f} kJ/kg")
        m4.metric("Compressor Exit (T2)", f"{t2_1:.2f} K")

        # Plotting Ideal (T-s & P-v Diagrams)
        fig1, (ax1_1, ax1_2) = plt.subplots(1, 2, figsize=(12, 5))

        # T-s Diagram Ideal (Bersambung)
        s1 = 0.0
        s2 = 0.0
        s3 = s2 + cp * np.log(t3_1 / t2_1)
        s4 = s3
        s_cycle = [s1, s2, s3, s4, s1]
        t_cycle = [t1_1, t2_1, t3_1, t4_1, t1_1]

        ax1_1.plot(s_cycle, t_cycle, 'b-', lw=2, label="Ideal Brayton Cycle")
        ax1_1.text(s1, t1_1, ' 1', fontsize=11, fontweight='bold')
        ax1_1.text(s2, t2_1, ' 2', fontsize=11, fontweight='bold')
        ax1_1.text(s3, t3_1, ' 3', fontsize=11, fontweight='bold')
        ax1_1.text(s4, t4_1, ' 4', fontsize=11, fontweight='bold')
        ax1_1.set_title("T-s Diagram (Ideal)")
        ax1_1.set_xlabel("Entropy, s")
        ax1_1.set_ylabel("Temperature, T (K)")
        ax1_1.grid(True)
        ax1_1.legend(fontsize=8)

        # P-v Diagram Ideal
        v1 = 0.287 * t1_1 / p1_1
        v2 = 0.287 * t2_1 / p2_1
        v3 = 0.287 * t3_1 / p3_1
        v4 = 0.287 * t4_1 / p4_1
        ax1_2.plot([v1, v2], [p1_1, p2_1], "r-", lw=2, label="1-2: Compression")
        ax1_2.plot([v2, v3], [p2_1, p3_1], "b-", lw=2, label="2-3: Heat Add")
        ax1_2.plot([v3, v4], [p3_1, p4_1], "g-", lw=2, label="3-4: Expansion")
        ax1_2.plot([v4, v1], [p4_1, p1_1], "k-", lw=2, label="4-1: Heat Reject")
        ax1_2.set_title("P-v Diagram (Ideal)")
        ax1_2.set_xlabel("Specific Volume, v")
        ax1_2.set_ylabel("Pressure, P (kPa)")
        ax1_2.grid(True)
        ax1_2.legend(fontsize=8)

        st.pyplot(fig1)


# =====================================================================
# TAB 2: ACTUAL BRAYTON CYCLE (WITH ISENTROPIC EFFICIENCIES)
# =====================================================================
with tab2:
    st.header("Actual Brayton Cycle (Isentropic Efficiencies)")
    st.markdown("Incorporates compressor and turbine non-idealities (irreversibilities).")

    col_sidebar2, col_main2 = st.columns([1, 3])

    with col_sidebar2:
        st.subheader("Parameters & Efficiencies")
        p1_2 = st.slider("Initial Pressure, P1 (kPa)", 50.0, 200.0, 100.0, 5.0, key="a_p1")
        t1_2 = st.slider("Initial Temperature, T1 (K)", 250.0, 400.0, 300.0, 5.0, key="a_t1")
        rp_2 = st.slider("Pressure Ratio (rp)", 2.0, 30.0, 10.0, 0.5, key="a_rp")
        t3_2 = st.slider("Max Turbine Inlet Temp, T3 (K)", 800.0, 1800.0, 1200.0, 10.0, key="a_t3")
        k_2 = st.slider("Specific Heat Ratio (k)", 1.2, 1.67, 1.4, 0.01, key="a_k")
        eta_c = st.slider("Compressor Efficiency (η_c)", 0.70, 1.00, 0.85, 0.01, key="a_etac")
        eta_t = st.slider("Turbine Efficiency (η_t)", 0.70, 1.00, 0.88, 0.01, key="a_etat")

    # Calculations (Actual)
    p2_2 = p1_2 * rp_2
    t2s = t1_2 * (rp_2 ** ((k_2 - 1) / k_2))
    t2_2 = t1_2 + (t2s - t1_2) / eta_c

    p3_2 = p2_2
    p4_2 = p1_2
    t4s = t3_2 / (rp_2 ** ((k_2 - 1) / k_2))
    t4_2 = t3_2 - eta_t * (t3_2 - t4s)

    q_in_2 = cp * (t3_2 - t2_2)
    q_out_2 = cp * (t4_2 - t1_2)
    w_net_2 = q_in_2 - q_out_2
    eta_th_2 = w_net_2 / q_in_2
    w_comp_2 = cp * (t2_2 - t1_2)
    w_turb_2 = cp * (t3_2 - t4_2)
    bwr_2 = w_comp_2 / w_turb_2

    with col_main2:
        am1, am2, am3, am4 = st.columns(4)
        am1.metric("Actual Thermal Efficiency", f"{eta_th_2 * 100:.2f}%")
        am2.metric("Back Work Ratio (BWR)", f"{bwr_2:.4f}")
        am3.metric("Net Work Output", f"{w_net_2:.2f} kJ/kg")
        am4.metric("Actual Exit Temp (T4)", f"{t4_2:.2f} K")

        # Pengiraan Entropi untuk Tab 2
        s1 = 0.0
        s2s = 0.0
        s2_actual = s1 + cp * np.log(t2_2 / t1_2) - (0.287) * np.log(p2_2 / p1_2)
        s3 = s2_actual + cp * np.log(t3_2 / t2_2)
        s4_actual = s3 + cp * np.log(t4_2 / t3_2) - (0.287) * np.log(p4_2 / p3_2)

        fig2, ax2_1 = plt.subplots(figsize=(8, 5))
        
        # Garisan Proses Sebenar (Actual Cycle Loop)
        ax2_1.plot([s1, s2_actual], [t1_2, t2_2], 'r-', lw=2, label=f"Actual Compression (η_c={eta_c})")
        ax2_1.plot([s2_actual, s3], [t2_2, t3_2], 'b-', lw=2, label="Heat Addition (2-3)")
        ax2_1.plot([s3, s4_actual], [t3_2, t4_2], 'g-', lw=2, label=f"Actual Expansion (η_t={eta_t})")
        ax2_1.plot([s4_actual, s1], [t4_2, t1_2], 'k-', lw=2, label="Heat Rejection (4-1)")

        # Garisan Rujukan Isentropik
        ax2_1.plot([s1, s2s], [t1_2, t2s], 'r--', alpha=0.4, label="Isentropic Comp")
        ax2_1.plot([s3, s3 + cp * np.log(t4s / t3_2)], [t3_2, t4s], 'g--', alpha=0.4, label="Isentropic Exp")

        # Label Status
        ax2_1.text(s1, t1_2, ' 1', fontsize=11, fontweight='bold')
        ax2_1.text(s2_actual, t2_2, ' 2a', fontsize=11, fontweight='bold')
        ax2_1.text(s3, t3_2, ' 3', fontsize=11, fontweight='bold')
        ax2_1.text(s4_actual, t4_2, ' 4a', fontsize=11, fontweight='bold')

        ax2_1.set_title("T-s Diagram (Actual Cycle with Irreversibilities)")
        ax2_1.set_xlabel("Entropy, s")
        ax2_1.set_ylabel("Temperature, T (K)")
        ax2_1.grid(True)
        ax2_1.legend(fontsize=8, loc='upper left')
        st.pyplot(fig2)


# =====================================================================
# TAB 3: REGENERATIVE BRAYTON CYCLE
# =====================================================================
with tab3:
    st.header("Regenerative Brayton Cycle Analysis")
    st.markdown("Utilizes a heat exchanger (regenerator) to capture exhaust heat and preheat air before combustion.")

    col_sidebar3, col_main3 = st.columns([1, 3])

    with col_sidebar3:
        st.subheader("Parameters & Effectiveness")
        p1_3 = st.slider("Initial Pressure, P1 (kPa)", 50.0, 200.0, 100.0, 5.0, key="r_p1")
        t1_3 = st.slider("Initial Temperature, T1 (K)", 250.0, 400.0, 300.0, 5.0, key="r_t1")
        rp_3 = st.slider("Pressure Ratio (rp)", 2.0, 30.0, 10.0, 0.5, key="r_rp")
        t3_3 = st.slider("Max Turbine Inlet Temp, T3 (K)", 800.0, 1800.0, 1200.0, 10.0, key="r_t3")
        k_3 = st.slider("Specific Heat Ratio (k)", 1.2, 1.67, 1.4, 0.01, key="r_k")
        epsilon = st.slider("Regenerator Effectiveness (ε)", 0.0, 1.0, 0.75, 0.05, key="r_eps")

    # Calculations (Regenerative)
    t2_3 = t1_3 * (rp_3 ** ((k_3 - 1) / k_3))
    t4_3 = t3_3 / (rp_3 ** ((k_3 - 1) / k_3))
    tx = t2_3 + epsilon * (t4_3 - t2_3)

    q_in_3 = cp * (t3_3 - tx)
    q_out_3 = cp * (t4_3 - tx)
    w_net_3 = cp * (t3_3 - t4_3) - cp * (t2_3 - t1_3)
    eta_th_3 = w_net_3 / q_in_3 if q_in_3 > 0 else 0

    with col_main3:
        rm1, rm2, rm3 = st.columns(3)
        rm1.metric("Regenerative Thermal Efficiency", f"{eta_th_3 * 100:.2f}%")
        rm2.metric("Preheater Exit Temp (Tx)", f"{tx:.2f} K")
        rm3.metric("Net Work Output", f"{w_net_3:.2f} kJ/kg")

        st.info(f"💡 Dengan keberkesanan regenerator sebanyak **{epsilon * 100:.0f}%**, suhu udara sebelum masuk ke ruang pembakaran ditingkatkan kepada **{tx:.2f} K**, sekaligus mengurangkan tenaga haba ($q_{in}$).")

        fig3, ax3_1 = plt.subplots(figsize=(8, 5))
        ax3_1.plot([0, 0], [t1_3, t2_3], "r-", lw=2, label="Compression")
        ax3_1.plot([0, 0.5], [t2_3, tx], "m--", lw=2, label=f"Regenerator Heating (Tx={tx:.1f}K)")
        ax3_1.plot([0.5, 0.8], [tx, t3_3], "b-", lw=2, label="Main Heat Addition (Combustor)")
        ax3_1.plot([0.8, 0.8], [t3_3, t4_3], "g-", lw=2, label="Expansion")
        ax3_1.plot([0.8, 0.3], [t4_3, tx], "c--", lw=2, label="Regenerator Cooling")
        ax3_1.plot([0.3, 0], [tx, t1_3], "k-", lw=2, label="Heat Rejection")
        ax3_1.set_title("T-s Diagram (Regenerative Brayton Cycle)")
        ax3_1.set_xlabel("Entropy, s")
        ax3_1.set_ylabel("Temperature, T (K)")
        ax3_1.grid(True)
        ax3_1.legend(fontsize=8)
        st.pyplot(fig3)