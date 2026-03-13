# Amazon Bedrock Integration for VortixelAI

## Overview

This integration adds AI-powered explanations to the VortixelAI Traffic Management System using **Amazon Bedrock** with the **nvidia.nemotron-nano-12b-v2** model.

## Features

✅ **AI-Generated Explanations** - Natural language explanations for traffic decisions  
✅ **Emergency Vehicle Context** - AI understands emergency priority overrides  
✅ **Streamlit Dashboard** - Interactive web interface with Bedrock integration  
✅ **Fallback Mechanism** - Graceful degradation if Bedrock API fails  
✅ **Easy Integration** - Simple function calls for any Python application

## Prerequisites

### 1. AWS Account Setup

You need an AWS account with access to Amazon Bedrock.

### 2. AWS Credentials Configuration

Configure your AWS credentials using one of these methods:

**Option A: AWS CLI**
```bash
aws configure
```

**Option B: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

**Option C: AWS Credentials File**
Create `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = your-access-key
aws_secret_access_key = your-secret-key
```

### 3. Bedrock Model Access

Enable access to the `nvidia.nemotron-nano-12b-v2` model in your AWS Bedrock console:

1. Go to AWS Console → Bedrock
2. Navigate to "Model access"
3. Request access to "nvidia.nemotron-nano-12b-v2"
4. Wait for approval (usually instant)

### 4. Install Dependencies

```bash
pip install boto3 streamlit
```

## Usage

### Basic Function Call

```python
from src.bedrock_ai import get_ai_explanation

# Generate AI explanation
explanation = get_ai_explanation(
    zone_a_vehicles=20,
    zone_b_vehicles=5,
    zone_a_has_emergency=False,
    zone_b_has_emergency=False,
    decision="Zone A receives GREEN signal"
)

print(explanation)
```

### Using the BedrockAIExplainer Class

```python
from src.bedrock_ai import BedrockAIExplainer

# Initialize explainer
explainer = BedrockAIExplainer(region_name="us-east-1")

# Generate explanation
explanation = explainer.generate_traffic_explanation(
    zone_a_vehicles=20,
    zone_b_vehicles=5,
    zone_a_has_emergency=False,
    zone_b_has_emergency=False,
    decision="Zone A receives GREEN signal"
)

print(explanation)
```

### Streamlit Dashboard

Run the interactive dashboard:

```bash
streamlit run streamlit_dashboard.py
```

Features:
- Interactive sliders for vehicle counts
- Emergency vehicle toggles
- Real-time AI explanations
- Network architecture visualization
- AWS region selection

### Example Script

Run the example script to see Bedrock in action:

```bash
python bedrock_example.py
```

## API Reference

### `get_ai_explanation()`

Convenience function for generating AI explanations.

**Parameters:**
- `zone_a_vehicles` (int): Number of vehicles in Zone A
- `zone_b_vehicles` (int): Number of vehicles in Zone B
- `zone_a_has_emergency` (bool): Emergency vehicle in Zone A (default: False)
- `zone_b_has_emergency` (bool): Emergency vehicle in Zone B (default: False)
- `decision` (str): The decision made (optional)
- `region_name` (str): AWS region (default: "us-east-1")

**Returns:**
- `str`: AI-generated explanation

**Example:**
```python
explanation = get_ai_explanation(
    zone_a_vehicles=20,
    zone_b_vehicles=5
)
```

### `BedrockAIExplainer` Class

Main class for Bedrock integration.

#### `__init__(region_name="us-east-1")`

Initialize the Bedrock AI explainer.

**Parameters:**
- `region_name` (str): AWS region for Bedrock service

#### `generate_traffic_explanation(...)`

Generate an AI explanation for a traffic decision.

**Parameters:**
- `zone_a_vehicles` (int): Number of vehicles in Zone A
- `zone_b_vehicles` (int): Number of vehicles in Zone B
- `zone_a_has_emergency` (bool): Emergency vehicle in Zone A
- `zone_b_has_emergency` (bool): Emergency vehicle in Zone B
- `decision` (str): The decision made (optional)

**Returns:**
- `str`: AI-generated explanation

**Raises:**
- `Exception`: If Bedrock API call fails (returns fallback explanation)

## Example Outputs

### Normal Traffic Priority

**Input:**
- Zone A: 20 vehicles
- Zone B: 5 vehicles

**AI Explanation:**
> "Zone A has significantly more vehicles (20 vs 5), requiring priority to optimize traffic flow. Granting GREEN signal to Zone A will reduce overall congestion and improve intersection efficiency. This decision maximizes throughput while maintaining safety standards."

### Emergency Vehicle Priority

**Input:**
- Zone A: 3 vehicles (EMERGENCY)
- Zone B: 25 vehicles

**AI Explanation:**
> "Emergency vehicle detected in Zone A triggers immediate priority override. Despite Zone B having higher traffic density (25 vehicles), emergency response takes precedence. This ensures rapid emergency vehicle passage, potentially saving lives in critical situations."

### Equal Traffic

**Input:**
- Zone A: 15 vehicles
- Zone B: 15 vehicles

**AI Explanation:**
> "Both zones have equal traffic density (15 vehicles each). The system implements fair alternation protocol, defaulting to Zone A for this cycle. This prevents starvation and ensures equitable access for all traffic zones over time."

## Integration with Existing System

The Bedrock integration works seamlessly with your existing VortixelAI system:

```python
from src.models import TrafficZone
from src.decision_engine import DecisionEngine
from src.bedrock_ai import get_ai_explanation

# Create zones
zone_a = TrafficZone("Zone_A", 20, has_emergency_vehicle=False)
zone_b = TrafficZone("Zone_B", 5, has_emergency_vehicle=False)

# Make decision
engine = DecisionEngine()
signal_a, signal_b, system_explanation = engine.make_decision(zone_a, zone_b)

# Get AI explanation
ai_explanation = get_ai_explanation(
    zone_a_vehicles=zone_a.vehicle_count,
    zone_b_vehicles=zone_b.vehicle_count,
    zone_a_has_emergency=zone_a.has_emergency_vehicle,
    zone_b_has_emergency=zone_b.has_emergency_vehicle,
    decision=f"Zone A: {signal_a.value}, Zone B: {signal_b.value}"
)

print(f"System: {system_explanation}")
print(f"AI: {ai_explanation}")
```

## Error Handling

The integration includes robust error handling:

1. **Fallback Explanations**: If Bedrock API fails, the system generates rule-based explanations
2. **Graceful Degradation**: Dashboard continues to work even if Bedrock is unavailable
3. **Clear Error Messages**: Helpful error messages guide troubleshooting

## Cost Considerations

Amazon Bedrock pricing is based on:
- **Input tokens**: Text sent to the model
- **Output tokens**: Text generated by the model

Typical costs for VortixelAI:
- ~50-100 tokens per request
- Estimated: $0.001-0.002 per explanation
- For 1000 explanations: ~$1-2

See [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) for current rates.

## Troubleshooting

### "Access Denied" Error

**Problem**: No access to Bedrock model

**Solution**:
1. Go to AWS Console → Bedrock → Model access
2. Request access to nvidia.nemotron-nano-12b-v2
3. Wait for approval

### "Credentials Not Found" Error

**Problem**: AWS credentials not configured

**Solution**:
```bash
aws configure
# Enter your AWS Access Key ID and Secret Access Key
```

### "Region Not Supported" Error

**Problem**: Bedrock not available in selected region

**Solution**: Use a supported region:
- us-east-1 (recommended)
- us-west-2
- eu-west-1

### Model Not Responding

**Problem**: Bedrock API timeout or error

**Solution**: The system automatically falls back to rule-based explanations. Check:
1. AWS service health
2. Your account limits
3. Network connectivity

## Security Best Practices

1. **Never hardcode credentials** - Use AWS credentials file or environment variables
2. **Use IAM roles** - For EC2/Lambda deployments, use IAM roles instead of access keys
3. **Limit permissions** - Grant only `bedrock:InvokeModel` permission
4. **Rotate credentials** - Regularly rotate AWS access keys
5. **Monitor usage** - Set up CloudWatch alarms for unusual activity

## Next Steps

- ✅ Integrate Bedrock AI explanations
- ✅ Create Streamlit dashboard
- ✅ Add fallback mechanism
- 🔄 Add caching for repeated queries
- 🔄 Implement batch processing
- 🔄 Add multi-language support
- 🔄 Create custom fine-tuned model

## Support

For issues or questions:
1. Check AWS Bedrock documentation
2. Review error messages in dashboard
3. Test with `bedrock_example.py`
4. Verify AWS credentials and permissions

## License

This integration is part of the VortixelAI Traffic Management System.
