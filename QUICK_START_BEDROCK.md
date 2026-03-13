# Quick Start: Amazon Bedrock Integration

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install boto3 streamlit
```

### Step 2: Configure AWS Credentials

```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `us-east-1`
- Default output format: `json`

### Step 3: Enable Bedrock Model Access

1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Click "Model access" in the left sidebar
3. Click "Request model access"
4. Find and enable: **nvidia.nemotron-nano-12b-v2**
5. Wait for approval (usually instant)

### Step 4: Test the Integration

Run the example script:

```bash
python bedrock_example.py
```

You should see AI-generated explanations for different traffic scenarios!

### Step 5: Launch the Dashboard

```bash
streamlit run streamlit_dashboard.py
```

Your browser will open with the interactive dashboard at `http://localhost:8501`

## 🎯 Quick Function Usage

### In Your Python Code

```python
from src.bedrock_ai import get_ai_explanation

# Generate AI explanation
explanation = get_ai_explanation(
    zone_a_vehicles=20,
    zone_b_vehicles=5
)

print(explanation)
```

### In Your Streamlit Dashboard

```python
import streamlit as st
from src.bedrock_ai import get_ai_explanation

# Your dashboard code...
zone_a_vehicles = st.slider("Zone A Vehicles", 0, 100, 20)
zone_b_vehicles = st.slider("Zone B Vehicles", 0, 100, 5)

if st.button("Get AI Explanation"):
    explanation = get_ai_explanation(zone_a_vehicles, zone_b_vehicles)
    st.write(explanation)
```

## 📝 Example Output

**Input:**
- Zone A: 20 vehicles
- Zone B: 5 vehicles

**Output:**
> "Zone A has significantly more vehicles (20 vs 5), requiring priority to optimize traffic flow. Granting GREEN signal to Zone A will reduce overall congestion and improve intersection efficiency."

## ⚠️ Troubleshooting

### Problem: "Access Denied"
**Solution:** Enable model access in Bedrock console (Step 3 above)

### Problem: "Credentials not found"
**Solution:** Run `aws configure` and enter your credentials

### Problem: "Region not supported"
**Solution:** Use `us-east-1`, `us-west-2`, or `eu-west-1`

## 💰 Cost Estimate

- ~$0.001-0.002 per explanation
- 1000 explanations ≈ $1-2
- Very affordable for most use cases!

## 📚 Full Documentation

See [BEDROCK_INTEGRATION.md](BEDROCK_INTEGRATION.md) for complete documentation.

## 🎉 You're Ready!

Your VortixelAI system now has AI-powered explanations using Amazon Bedrock!
