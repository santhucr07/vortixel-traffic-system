import boto3
import json

def get_ai_explanation(decision):

    prompt = f"Explain in 2 simple sentences why the traffic signal decision is {decision}."

    try:
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1"
        )

        body = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 100
        })

        response = client.invoke_model(
            modelId="nvidia.nemotron-nano-12b-v2",
            body=body
        )

        result = json.loads(response["body"].read())

        # Extract only the AI text
        ai_text = result["choices"][0]["message"]["content"]

        return ai_text

    except Exception as e:
        return f"Bedrock connection error: {str(e)}"