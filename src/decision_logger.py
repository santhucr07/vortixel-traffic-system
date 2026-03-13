"""Decision Logger for creating and managing decision log entries."""

from src.models import TrafficZone, DecisionLog


class LoggingError(Exception):
    """Raised when decision log creation fails."""
    pass


class DecisionLogger:
    """
    Creates and manages decision log entries.
    """
    
    def __init__(self):
        """Initialize the decision logger."""
        pass
    
    def log_decision(
        self,
        cycle_number: int,
        zone_a: TrafficZone,
        zone_b: TrafficZone,
        explanation: str
    ) -> DecisionLog:
        """
        Create a decision log entry for a traffic cycle.
        
        Args:
            cycle_number: The current cycle number
            zone_a: First traffic zone with assigned signal
            zone_b: Second traffic zone with assigned signal
            explanation: Textual explanation of the decision
            
        Returns:
            DecisionLog entry
            
        Raises:
            LoggingError: If log creation fails
        """
        try:
            # Validate all required fields are present and non-empty
            if cycle_number <= 0:
                raise ValueError("Cycle number must be positive")
            
            if not zone_a.zone_id:
                raise ValueError("Zone A ID cannot be empty")
            
            if not zone_b.zone_id:
                raise ValueError("Zone B ID cannot be empty")
            
            if zone_a.signal_state is None:
                raise ValueError("Zone A signal state not assigned")
            
            if zone_b.signal_state is None:
                raise ValueError("Zone B signal state not assigned")
            
            if not explanation or not explanation.strip():
                raise ValueError("Explanation cannot be empty")
            
            # Create and return the decision log
            return DecisionLog(
                cycle_number=cycle_number,
                zone_a_id=zone_a.zone_id,
                zone_a_count=zone_a.vehicle_count,
                zone_a_signal=zone_a.signal_state,
                zone_b_id=zone_b.zone_id,
                zone_b_count=zone_b.vehicle_count,
                zone_b_signal=zone_b.signal_state,
                explanation=explanation
            )
        except Exception as e:
            raise LoggingError(
                f"Failed to create decision log for cycle {cycle_number}"
            ) from e
    
    def format_log(self, log: DecisionLog) -> str:
        """
        Format a decision log entry as human-readable text.
        
        Args:
            log: Decision log entry to format
        
        Returns:
            Formatted string representation
        """
        return (
            f"Cycle {log.cycle_number}:\n"
            f"  {log.zone_a_id}: {log.zone_a_count} vehicles -> {log.zone_a_signal.value}\n"
            f"  {log.zone_b_id}: {log.zone_b_count} vehicles -> {log.zone_b_signal.value}\n"
            f"  Decision: {log.explanation}"
        )
