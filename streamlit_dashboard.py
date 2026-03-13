"""
VortixelAI Traffic Management Dashboard with Amazon Bedrock Integration

A Streamlit dashboard that visualizes traffic management decisions and uses
Amazon Bedrock AI to generate intelligent explanations.
"""

import streamlit as st
from src.models import TrafficZone, SignalState
from src.decision_engine import DecisionEngine
from src.bedrock_ai import get_ai_explanation


# Page configuration
st.set_page_config(
    page_title="VortixelAI Traffic Management",
    page_icon="🚦",
    layout="wide"
)

# Title and description
st.title("🚦 VortixelAI Traffic Management System")
st.markdown("### AI-Powered Traffic Signal Control with Amazon Bedrock")

# Create two columns for the zones
col1, col2 = st.columns(2)

with col1:
    st.subheader("🅰️ Zone A")
    zone_a_vehicles = st.number_input(
        "Number of vehicles in Zone A",
        min_value=0,
        max_value=100,
        value=20,
        step=1
    )
    zone_a_emergency = st.checkbox("Emergency vehicle in Zone A", value=False)

with col2:
    st.subheader("🅱️ Zone B")
    zone_b_vehicles = st.number_input(
        "Number of vehicles in Zone B",
        min_value=0,
        max_value=100,
        value=5,
        step=1
    )
    zone_b_emergency = st.checkbox("Emergency vehicle in Zone B", value=False)

# AWS Configuration
st.sidebar.header("⚙️ AWS Configuration")
aws_region = st.sidebar.selectbox(
    "AWS Region",
    ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
    index=0
)
use_bedrock = st.sidebar.checkbox("Use Amazon Bedrock AI", value=True)

# Decision button
if st.button("🚦 Make Traffic Decision", type="primary"):
    # Create traffic zones
    zone_a = TrafficZone("Zone_A", zone_a_vehicles, zone_a_emergency)
    zone_b = TrafficZone("Zone_B", zone_b_vehicles, zone_b_emergency)
    
    # Create decision engine
    engine = DecisionEngine()
    
    # Make decision
    signal_a, signal_b, explanation = engine.make_decision(zone_a, zone_b)
    
    # Apply signals
    zone_a.set_signal_state(signal_a)
    zone_b.set_signal_state(signal_b)
    
    # Display results
    st.markdown("---")
    st.subheader("📊 Traffic Decision Results")
    
    # Show signals with color coding
    result_col1, result_col2 = st.columns(2)
    
    with result_col1:
        if signal_a == SignalState.GREEN:
            st.success(f"### Zone A: 🟢 GREEN")
        else:
            st.error(f"### Zone A: 🔴 RED")
        st.metric("Vehicles", zone_a_vehicles)
        if zone_a_emergency:
            st.warning("⚠️ Emergency Vehicle Present")
    
    with result_col2:
        if signal_b == SignalState.GREEN:
            st.success(f"### Zone B: 🟢 GREEN")
        else:
            st.error(f"### Zone B: 🔴 RED")
        st.metric("Vehicles", zone_b_vehicles)
        if zone_b_emergency:
            st.warning("⚠️ Emergency Vehicle Present")
    
    # System explanation
    st.markdown("---")
    st.subheader("💡 System Explanation")
    st.info(f"**Decision Logic:** {explanation}")
    
    # AI-powered explanation using Amazon Bedrock
    if use_bedrock:
        st.markdown("---")
        st.subheader("🤖 AI-Powered Explanation (Amazon Bedrock)")
        
        with st.spinner("Generating AI explanation using Amazon Bedrock..."):
            try:
                # Determine which zone got GREEN
                if signal_a == SignalState.GREEN:
                    decision_text = "Zone A receives GREEN signal"
                else:
                    decision_text = "Zone B receives GREEN signal"
                
                # Call Bedrock AI
                ai_explanation = get_ai_explanation(
                    zone_a_vehicles=zone_a_vehicles,
                    zone_b_vehicles=zone_b_vehicles,
                    zone_a_has_emergency=zone_a_emergency,
                    zone_b_has_emergency=zone_b_emergency,
                    decision=decision_text,
                    region_name=aws_region
                )
                
                st.success("✅ AI Explanation Generated")
                st.markdown(f"**{ai_explanation}**")
                
            except Exception as e:
                st.error(f"❌ Bedrock API Error: {str(e)}")
                st.info("💡 Make sure your AWS credentials are configured and you have access to Bedrock.")
    
    # Network architecture visualization
    st.markdown("---")
    st.subheader("🌐 Network Architecture")
    
    st.code(f"""
Networked Traffic Control Flow:

Zone A Node → Sending: {zone_a_vehicles} vehicles{' + EMERGENCY' if zone_a_emergency else ''}
Zone B Node → Sending: {zone_b_vehicles} vehicles{' + EMERGENCY' if zone_b_emergency else ''}
              ↓
    Decision Engine AI
              ↓
    Decision: {signal_a.value} for Zone A, {signal_b.value} for Zone B
    """, language="text")

# Sidebar information
st.sidebar.markdown("---")
st.sidebar.header("ℹ️ About")
st.sidebar.info("""
**VortixelAI Traffic Management**

An intelligent traffic signal control system that:
- Prioritizes zones based on vehicle density
- Gives immediate priority to emergency vehicles
- Uses AI to explain decisions
- Simulates networked architecture

**Powered by:**
- Amazon Bedrock (nvidia.nemotron-nano-12b-v2)
- Python + Streamlit
""")

st.sidebar.markdown("---")
st.sidebar.header("📚 How It Works")
st.sidebar.markdown("""
1. **Data Collection**: Each zone acts as an independent node collecting traffic data
2. **Data Transmission**: Zones send data to the central Decision Engine
3. **AI Processing**: Decision Engine analyzes inputs and makes optimal decisions
4. **Emergency Override**: Emergency vehicles receive immediate priority
5. **AI Explanation**: Bedrock generates human-friendly explanations
""")
