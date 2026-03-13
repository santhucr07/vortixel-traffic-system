"""Demonstration of the VortixelAI Traffic Management System."""

from src.simulation_controller import SimulationController
from src.decision_engine import DecisionEngine
from src.decision_logger import DecisionLogger
from src.models import TrafficZone


def main():
    """Run a demonstration simulation."""
    print("=" * 60)
    print("VortixelAI Traffic Management System - Simulation Demo")
    print("=" * 60)
    print()
    
    # Initialize components
    engine = DecisionEngine(default_zone_id="Zone_A")
    logger = DecisionLogger()
    controller = SimulationController(engine, logger)
    
    # Create traffic zones
    zone_a = TrafficZone("Zone_A", 0)
    zone_b = TrafficZone("Zone_B", 0)
    
    # Define vehicle count updates for demonstration
    print("Running 8-cycle simulation with varying traffic conditions...")
    print()
    
    updates = [
        (15, 8),   # Cycle 1: Zone A has more vehicles
        (5, 12),   # Cycle 2: Zone B has more vehicles
        (10, 10),  # Cycle 3: Equal counts - Zone A gets priority (default)
        (10, 10),  # Cycle 4: Equal counts - Zone B gets priority (alternating)
        (0, 0),    # Cycle 5: Both zones empty - Zone A gets priority (alternating)
        (20, 5),   # Cycle 6: Zone A has significantly more vehicles
        (3, 25),   # Cycle 7: Zone B has significantly more vehicles
        (7, 7),    # Cycle 8: Equal counts - Zone B gets priority (alternating)
    ]
    
    # Run simulation
    logs = controller.run_simulation(
        zone_a, zone_b,
        num_cycles=8,
        vehicle_count_updates=updates
    )
    
    # Output results
    controller.output_logs(logs)
    
    print()
    print("=" * 60)
    print("Simulation completed successfully!")
    print(f"Total cycles executed: {len(logs)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
