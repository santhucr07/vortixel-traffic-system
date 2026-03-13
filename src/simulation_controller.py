"""Simulation Controller for orchestrating multi-cycle traffic management simulation."""

from src.models import TrafficZone, DecisionLog
from src.decision_engine import DecisionEngine
from src.decision_logger import DecisionLogger


class SimulationController:
    """
    Manages the execution of traffic management simulation.
    """
    
    def __init__(
        self,
        decision_engine: DecisionEngine,
        decision_logger: DecisionLogger
    ):
        """
        Initialize the simulation controller.
        
        Args:
            decision_engine: Decision engine instance for signal assignments
            decision_logger: Decision logger instance for recording decisions
        """
        self.decision_engine = decision_engine
        self.decision_logger = decision_logger
    
    def run_simulation(
        self,
        zone_a: TrafficZone,
        zone_b: TrafficZone,
        num_cycles: int,
        vehicle_count_updates: list[tuple[int, int]],
        emergency_vehicle_updates: list[tuple[bool, bool]] | None = None,
        verbose_network: bool = False
    ) -> list[DecisionLog]:
        """
        Execute a multi-cycle traffic management simulation with optional emergency vehicle support.
        
        Args:
            zone_a: First traffic zone
            zone_b: Second traffic zone
            num_cycles: Number of cycles to simulate
            vehicle_count_updates: List of (zone_a_count, zone_b_count) 
                                   for each cycle
            emergency_vehicle_updates: Optional list of (zone_a_has_emergency, zone_b_has_emergency)
                                      for each cycle. If None, no emergency vehicles present.
            verbose_network: If True, displays networked architecture communication (zones sending
                           data to Decision Engine AI). Default False for backward compatibility.
            
        Returns:
            List of decision log entries, one per cycle
            
        Raises:
            ValueError: If num_cycles is not positive or doesn't match 
                       length of updates, or if vehicle counts are negative,
                       or if emergency_vehicle_updates length doesn't match num_cycles
        """
        # Validate num_cycles is positive
        if num_cycles <= 0:
            raise ValueError("Number of cycles must be positive")
        
        # Validate vehicle_count_updates length matches num_cycles
        if len(vehicle_count_updates) != num_cycles:
            raise ValueError("Number of vehicle count updates must match number of cycles")
        
        # Validate emergency_vehicle_updates if provided
        if emergency_vehicle_updates is not None:
            if len(emergency_vehicle_updates) != num_cycles:
                raise ValueError("Number of emergency vehicle updates must match number of cycles")
        
        # Validate all vehicle counts are non-negative
        for i, (count_a, count_b) in enumerate(vehicle_count_updates):
            if count_a < 0 or count_b < 0:
                raise ValueError("Vehicle count cannot be negative")
        
        # Execute cycles sequentially
        logs = []
        for cycle_num in range(1, num_cycles + 1):
            # Display network communication if verbose mode enabled
            if verbose_network:
                print(f"\n{'='*60}")
                print(f"Cycle {cycle_num}:")
                print(f"{'='*60}")
            
            # Update vehicle counts from vehicle_count_updates
            count_a, count_b = vehicle_count_updates[cycle_num - 1]
            zone_a.update_vehicle_count(count_a)
            zone_b.update_vehicle_count(count_b)
            
            # Update emergency vehicle status
            if emergency_vehicle_updates is not None:
                has_emergency_a, has_emergency_b = emergency_vehicle_updates[cycle_num - 1]
                zone_a.set_emergency_vehicle(has_emergency_a)
                zone_b.set_emergency_vehicle(has_emergency_b)
            else:
                # No emergency vehicles
                zone_a.set_emergency_vehicle(False)
                zone_b.set_emergency_vehicle(False)
            
            # Display zones sending data (networked architecture visualization)
            if verbose_network:
                self._display_zone_data_transmission(zone_a, zone_b)
            
            # Call decision_engine.make_decision()
            if verbose_network:
                print("\nDecision Engine AI processing inputs...")
            
            zone_a_signal, zone_b_signal, explanation = self.decision_engine.make_decision(
                zone_a, zone_b
            )
            
            # Display AI decision output
            if verbose_network:
                self._display_ai_decision(zone_a, zone_b, zone_a_signal, zone_b_signal, explanation)
            
            # Apply signal states to zones
            zone_a.set_signal_state(zone_a_signal)
            zone_b.set_signal_state(zone_b_signal)
            
            # Call decision_logger.log_decision()
            log_entry = self.decision_logger.log_decision(
                cycle_num, zone_a, zone_b, explanation
            )
            
            # Collect log entry
            logs.append(log_entry)
        
        return logs
    
    def output_logs(self, logs: list[DecisionLog]) -> None:
        """
        Output all decision logs in human-readable format.
        
        Args:
            logs: List of decision log entries to output
        """
        for log in logs:
            formatted_log = self.decision_logger.format_log(log)
            print(formatted_log)
    
    def _display_zone_data_transmission(self, zone_a: TrafficZone, zone_b: TrafficZone) -> None:
        """
        Display zones sending data to the central Decision Engine (networked architecture).
        
        Args:
            zone_a: First traffic zone
            zone_b: Second traffic zone
        """
        print(f"\n{zone_a.zone_id} -> sending traffic data: {zone_a.vehicle_count} vehicles")
        if zone_a.has_emergency_vehicle:
            print(f"   ⚠️  EMERGENCY VEHICLE DETECTED in {zone_a.zone_id}")
        
        print(f"{zone_b.zone_id} -> sending traffic data: {zone_b.vehicle_count} vehicles")
        if zone_b.has_emergency_vehicle:
            print(f"   ⚠️  EMERGENCY VEHICLE DETECTED in {zone_b.zone_id}")
    
    def _display_ai_decision(
        self, 
        zone_a: TrafficZone, 
        zone_b: TrafficZone,
        zone_a_signal,
        zone_b_signal,
        explanation: str
    ) -> None:
        """
        Display the AI Decision Engine's output.
        
        Args:
            zone_a: First traffic zone
            zone_b: Second traffic zone
            zone_a_signal: Signal assigned to zone A
            zone_b_signal: Signal assigned to zone B
            explanation: Explanation for the decision
        """
        print(f"\n🤖 Decision Engine AI Output:")
        print(f"   Decision -> {zone_a.zone_id}: {zone_a_signal.value}, {zone_b.zone_id}: {zone_b_signal.value}")
        print(f"   Reason -> {explanation}")
