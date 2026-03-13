"""Decision Engine for traffic signal priority assignment."""

from src.models import TrafficZone, SignalState


class SafetyViolationError(Exception):
    """Raised when both zones would be assigned GREEN signal."""
    pass


class DecisionEngine:
    """
    Implements the traffic signal decision-making algorithm.
    
    The engine compares vehicle counts and assigns signals based on:
    - Higher count gets GREEN
    - Lower count gets RED
    - Equal counts alternate (with default zone for first tie)
    """
    
    def __init__(self, default_zone_id: str = "Zone_A"):
        """
        Initialize the decision engine.
        
        Args:
            default_zone_id: Zone to receive GREEN on first tie (default "Zone_A")
        """
        self.default_zone_id = default_zone_id
        self.last_tie_winner: str | None = None
    
    def _compare_counts(self, count_a: int, count_b: int) -> str:
        """
        Compare vehicle counts and determine priority.
        
        Args:
            count_a: Vehicle count for zone A
            count_b: Vehicle count for zone B
        
        Returns:
            "A" if zone A has priority
            "B" if zone B has priority
            "TIE" if counts are equal
        """
        if count_a > count_b:
            return "A"
        elif count_b > count_a:
            return "B"
        else:
            return "TIE"
    
    def _handle_tie(self) -> str:
        """
        Handle tie-breaking for equal vehicle counts.
        
        Returns:
            Zone ID that should receive GREEN
            
        Alternates between zones on consecutive ties.
        """
        if self.last_tie_winner is None:
            # First tie: use default zone
            self.last_tie_winner = self.default_zone_id
            return self.default_zone_id
        elif self.last_tie_winner == "Zone_A":
            # Alternate to Zone B
            self.last_tie_winner = "Zone_B"
            return "Zone_B"
        else:
            # Alternate to Zone A
            self.last_tie_winner = "Zone_A"
            return "Zone_A"
    
    def make_decision(
        self, 
        zone_a: TrafficZone, 
        zone_b: TrafficZone
    ) -> tuple[SignalState, SignalState, str]:
        """
        Determine signal assignments for both zones with emergency vehicle priority.
        
        Emergency vehicles receive highest priority and override normal traffic logic.
        If an emergency vehicle is present in a zone, that zone immediately receives GREEN.
        
        Args:
            zone_a: First traffic zone
            zone_b: Second traffic zone
            
        Returns:
            Tuple of (zone_a_signal, zone_b_signal, explanation)
            
        Raises:
            SafetyViolationError: If both zones would be assigned GREEN
            
        The explanation describes the reasoning for the assignment.
        """
        # Check for emergency vehicles FIRST (highest priority)
        if zone_a.has_emergency_vehicle and zone_b.has_emergency_vehicle:
            # Both zones have emergency vehicles - prioritize Zone A
            return (
                SignalState.GREEN,
                SignalState.RED,
                "Emergency vehicle priority in Zone A (both zones have emergency vehicles)"
            )
        elif zone_a.has_emergency_vehicle:
            # Zone A has emergency vehicle
            return (
                SignalState.GREEN,
                SignalState.RED,
                f"Emergency vehicle priority in {zone_a.zone_id}"
            )
        elif zone_b.has_emergency_vehicle:
            # Zone B has emergency vehicle
            return (
                SignalState.RED,
                SignalState.GREEN,
                f"Emergency vehicle priority in {zone_b.zone_id}"
            )
        
        # No emergency vehicles - use normal traffic logic
        # Compare vehicle counts
        priority = self._compare_counts(zone_a.vehicle_count, zone_b.vehicle_count)
        
        # Determine signal assignments based on priority
        if priority == "A":
            zone_a_signal = SignalState.GREEN
            zone_b_signal = SignalState.RED
            explanation = f"Zone A has higher vehicle count ({zone_a.vehicle_count} > {zone_b.vehicle_count})"
        elif priority == "B":
            zone_a_signal = SignalState.RED
            zone_b_signal = SignalState.GREEN
            explanation = f"Zone B has higher vehicle count ({zone_b.vehicle_count} > {zone_a.vehicle_count})"
        else:  # TIE
            # Check if this is the first tie before calling _handle_tie
            is_first_tie = self.last_tie_winner is None
            winner = self._handle_tie()
            
            if winner == "Zone_A":
                zone_a_signal = SignalState.GREEN
                zone_b_signal = SignalState.RED
                if is_first_tie:
                    # First tie case
                    explanation = f"Equal vehicle counts ({zone_a.vehicle_count}), Zone A receives priority (default)"
                else:
                    # Alternating back to Zone A
                    explanation = f"Equal vehicle counts ({zone_a.vehicle_count}), alternating to Zone A"
            else:  # winner == "Zone_B"
                zone_a_signal = SignalState.RED
                zone_b_signal = SignalState.GREEN
                explanation = f"Equal vehicle counts ({zone_a.vehicle_count}), alternating to Zone B"
        
        # Validate safety constraint
        if zone_a_signal == SignalState.GREEN and zone_b_signal == SignalState.GREEN:
            raise SafetyViolationError("Safety violation: Both zones assigned GREEN signal")
        
        return (zone_a_signal, zone_b_signal, explanation)
