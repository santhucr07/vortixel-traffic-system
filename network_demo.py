"""
Networked Traffic Control Architecture Demo

This demo showcases the VortixelAI traffic system as a networked architecture where:
- Each traffic zone acts as an independent node collecting traffic data
- Zones send their data to the central Decision Engine AI
- The Decision Engine processes inputs and makes decisions
- Emergency vehicles trigger immediate priority overrides
"""

from src.models import TrafficZone
from src.decision_engine import DecisionEngine
from src.decision_logger import DecisionLogger
from src.simulation_controller import SimulationController


def main():
    print("=" * 70)
    print("VortixelAI Networked Traffic Control Architecture Demo")
    print("=" * 70)
    print("\nSimulating a networked traffic control system where zones")
    print("communicate with a central AI Decision Engine.\n")
    
    # Initialize traffic zones (independent nodes in the network)
    zone_a = TrafficZone("Zone_A", 0)
    zone_b = TrafficZone("Zone_B", 0)
    
    # Create central Decision Engine AI
    engine = DecisionEngine(default_zone_id="Zone_A")
    logger = DecisionLogger()
    
    # Create simulation controller
    controller = SimulationController(engine, logger)
    
    # Define traffic scenario with emergency vehicle
    vehicle_updates = [
        (10, 5),    # Cycle 1: Zone A has more traffic
        (8, 12),    # Cycle 2: Zone B has more traffic
        (10, 8),    # Cycle 3: Zone A has more, but Zone B has emergency
        (15, 15),   # Cycle 4: Equal traffic, no emergency
        (5, 20),    # Cycle 5: Zone B has much more traffic
    ]
    
    emergency_updates = [
        (False, False),  # Cycle 1: No emergencies
        (False, False),  # Cycle 2: No emergencies
        (False, True),   # Cycle 3: Emergency in Zone B!
        (False, False),  # Cycle 4: No emergencies
        (False, False),  # Cycle 5: No emergencies
    ]
    
    # Run simulation with networked architecture visualization
    print("\n" + "=" * 70)
    print("STARTING NETWORKED SIMULATION")
    print("=" * 70)
    
    logs = controller.run_simulation(
        zone_a,
        zone_b,
        num_cycles=5,
        vehicle_count_updates=vehicle_updates,
        emergency_vehicle_updates=emergency_updates,
        verbose_network=True  # Enable networked architecture display
    )
    
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)
    print(f"\nProcessed {len(logs)} traffic cycles successfully.")
    print("All zones communicated with the central Decision Engine AI.")
    print("Emergency vehicle priority was enforced when detected.")


if __name__ == "__main__":
    main()
