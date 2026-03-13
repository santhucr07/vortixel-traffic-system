import boto3
import json


def get_ai_explanation(zone_a_vehicles, zone_b_vehicles, decision):

    try:
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        prompt = f"""
        You are an AI traffic management assistant.

        Analyze the following traffic data and explain the decision.

        Zone A vehicles: {zone_a_vehicles}
        Zone B vehicles: {zone_b_vehicles}

        Explain which zone should get priority and why.
        """

        body = json.dumps({
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 0.5
        })

        response = client.invoke_model(
            modelId="nvidia.nemotron-nano-12b-v2",
            body=body
        )

        result = json.loads(response["body"].read())

        return result.get("completion", "AI explanation generated.")

    except Exception as e:

        # fallback explanation if Bedrock fails
        if zone_a_vehicles > zone_b_vehicles:
            decision = "Zone A gets priority due to higher congestion."
        elif zone_b_vehicles > zone_a_vehicles:
            decision = "Zone B gets priority due to higher congestion."
        else:
            decision = "Both zones have equal traffic. Alternating signal."

        return f"""
AI fallback explanation (Bedrock unavailable):

Zone A vehicles: {zone_a_vehicles}
Zone B vehicles: {zone_b_vehicles}

Decision: {decision}

Error detail: {str(e)}
"""