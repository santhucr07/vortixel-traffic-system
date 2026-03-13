"""
Simple example of using Amazon Bedrock AI with VortixelAI Traffic Management

This script demonstrates how to use the Bedrock AI integration to generate
explanations for traffic decisions.
"""

from src.bedrock_ai import get_ai_explanation


def main():
    print("=" * 70)
    print("VortixelAI + Amazon Bedrock Integration Example")
    print("=" * 70)
    
    # Example 1: Normal traffic priority
    print("\n📊 Example 1: Normal Traffic Priority")
    print("-" * 70)
    print("Zone A: 20 vehicles")
    print("Zone B: 5 vehicles")
    print("\nGenerating AI explanation...")
    
    explanation = get_ai_explanation(
        zone_a_vehicles=20,
        zone_b_vehicles=5,
        zone_a_has_emergency=False,
        zone_b_has_emergency=False,
        decision="Zone A receives GREEN signal"
    )
    
    print(f"\n🤖 AI Explanation:\n{explanation}")
    
    # Example 2: Emergency vehicle priority
    print("\n\n📊 Example 2: Emergency Vehicle Priority")
    print("-" * 70)
    print("Zone A: 3 vehicles (EMERGENCY VEHICLE)")
    print("Zone B: 25 vehicles")
    print("\nGenerating AI explanation...")
    
    explanation = get_ai_explanation(
        zone_a_vehicles=3,
        zone_b_vehicles=25,
        zone_a_has_emergency=True,
        zone_b_has_emergency=False,
        decision="Zone A receives GREEN signal (Emergency Override)"
    )
    
    print(f"\n🤖 AI Explanation:\n{explanation}")
    
    # Example 3: Equal traffic
    print("\n\n📊 Example 3: Equal Traffic (Fair Alternation)")
    print("-" * 70)
    print("Zone A: 15 vehicles")
    print("Zone B: 15 vehicles")
    print("\nGenerating AI explanation...")
    
    explanation = get_ai_explanation(
        zone_a_vehicles=15,
        zone_b_vehicles=15,
        zone_a_has_emergency=False,
        zone_b_has_emergency=False,
        decision="Zone A receives GREEN signal (Default Priority)"
    )
    
    print(f"\n🤖 AI Explanation:\n{explanation}")
    
    print("\n" + "=" * 70)
    print("Examples Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
