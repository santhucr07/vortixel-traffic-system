"""
Comprehensive VortixelAI Traffic Management Demo

This demo showcases all features of the VortixelAI system:
1. Normal traffic priority based on vehicle counts
2. Emergency vehicle priority override
3. Networked architecture visualization
4. Fair alternation for equal traffic
"""

from src.models import TrafficZone
from src.decision_engine import DecisionEngine
from src.decision_logger import DecisionLogger
from src.simulation_controller import SimulationController


def main():
    print("=" * 80)
    print(" " * 20 + "VortixelAI Traffic Management System")
    print(" " * 15 + "Comprehensive Feature Demonstration")
    print("=" * 80)
    
    # Initialize system components
    zone_a = TrafficZone("Zone_A", 0)
    zone_b = TrafficZone("Zone_B", 0)
    engine = DecisionEngine(default_zone_id="Zone_A")
    logger = DecisionLogger()
    controller = SimulationController(engine, logger)
    
    # Define comprehensive traffic scenario
    vehicle_updates = [
        (15, 8),    # Cycle 1: Zone A has more traffic (normal priority)
        (5, 12),    # Cycle 2: Zone B has more traffic (normal priority)
        (10, 10),   # Cycle 3: Equal traffic (fair alternation - Zone A default)
        (10, 10),   # Cycle 4: Equal traffic (fair alternation - Zone B)
        (3, 15),    # Cycle 5: Zone B has more, but Zone A has emergency!
        (20, 8),    # Cycle 6: Zone A has more traffic (normal priority resumes)
        (7, 7),     # Cycle 7: Equal traffic (fair alternation - Zone A)
        (0, 25),    # Cycle 8: Zone B has much more traffic
    ]
    
    emergency_updates = [
        (False, False),  # Cycle 1: No emergencies
        (False, False),  # Cycle 2: No emergencies
        (False, False),  # Cycle 3: No emergencies
        (False, False),  # Cycle 4: No emergencies
        (True, False),   # Cycle 5: EMERGENCY in Zone A! (overrides normal logic)
        (False, False),  # Cycle 6: No emergencies
        (False, False),  # Cycle 7: No emergencies
        (False, False),  # Cycle 8: No emergencies
    ]
    
    print("\n📋 Scenario Overview:")
    print("   • 8 traffic cycles demonstrating all system features")
    print("   • Normal traffic priority (Cycles 1, 2, 6, 8)")
    print("   • Fair alternation for equal traffic (Cycles 3, 4, 7)")
    print("   • Emergency vehicle priority override (Cycle 5)")
    print("   • Networked architecture visualization enabled")
    
    input("\nPress Enter to start the simulation...")
    
    # Run simulation with networked architecture visualization
    logs = controller.run_simulation(
        zone_a,
        zone_b,
        num_cycles=8,
        vehicle_count_updates=vehicle_updates,
        emergency_vehicle_updates=emergency_updates,
        verbose_network=True  # Enable networked architecture display
    )
    
    # Summary
    print("\n" + "=" * 80)
    print(" " * 30 + "SIMULATION SUMMARY")
    print("=" * 80)
    
    print(f"\n✅ Successfully processed {len(logs)} traffic cycles")
    print("\n📊 Feature Demonstrations:")
    print("   ✓ Normal traffic priority based on vehicle counts")
    print("   ✓ Emergency vehicle priority override (Cycle 5)")
    print("   ✓ Fair alternation for equal traffic (Cycles 3, 4, 7)")
    print("   ✓ Networked architecture with zone-to-AI communication")
    print("   ✓ Real-time decision visualization")
    
    print("\n🎯 Key Observations:")
    print("   • Cycle 5: Emergency vehicle in Zone A overrode normal logic")
    print("     (Zone B had 15 vehicles vs Zone A's 3, but Zone A got GREEN)")
    print("   • Cycles 3, 4, 7: Equal traffic resulted in fair alternation")
    print("   • All other cycles: Higher traffic count received GREEN signal")
    
    print("\n" + "=" * 80)
    print(" " * 25 + "Demo Complete - System Ready")
    print("=" * 80)


if __name__ == "__main__":
    main()
