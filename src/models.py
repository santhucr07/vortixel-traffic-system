"""Core data models for the VortixelAI Traffic Management System."""

from dataclasses import dataclass
from enum import Enum


class SignalState(Enum):
    """Traffic signal states."""
    GREEN = "GREEN"
    RED = "RED"


class TrafficZone:
    """
    Represents a traffic zone with vehicle count, signal control, and emergency vehicle detection.
    
    Attributes:
        zone_id: Unique identifier for the zone (e.g., "Zone_A", "Zone_B")
        vehicle_count: Number of vehicles currently in the zone (non-negative)
        signal_state: Current signal state (GREEN or RED)
        has_emergency_vehicle: Whether an emergency vehicle is present in this zone
    """
    
    def __init__(self, zone_id: str, vehicle_count: int, has_emergency_vehicle: bool = False):
        """
        Initialize a traffic zone with given ID and vehicle count.
        
        Args:
            zone_id: Unique identifier for the zone
            vehicle_count: Initial number of vehicles in the zone
            has_emergency_vehicle: Whether emergency vehicle is present (default False)
            
        Raises:
            ValueError: If zone_id is empty or vehicle_count is negative
        """
        if not zone_id:
            raise ValueError("Zone ID cannot be empty")
        if vehicle_count < 0:
            raise ValueError("Vehicle count cannot be negative")
        
        self.zone_id = zone_id
        self.vehicle_count = vehicle_count
        self.signal_state: SignalState | None = None
        self.has_emergency_vehicle = has_emergency_vehicle
    
    def update_vehicle_count(self, count: int) -> None:
        """
        Update the vehicle count for this zone.
        
        Args:
            count: New vehicle count
            
        Raises:
            ValueError: If count is negative
        """
        if count < 0:
            raise ValueError("Vehicle count cannot be negative")
        self.vehicle_count = count
    
    def set_signal_state(self, state: SignalState) -> None:
        """
        Set the signal state for this zone.
        
        Args:
            state: Signal state to assign (GREEN or RED)
        """
        self.signal_state = state
    
    def set_emergency_vehicle(self, present: bool) -> None:
        """
        Set whether an emergency vehicle is present in this zone.
        
        Args:
            present: True if emergency vehicle present, False otherwise
        """
        self.has_emergency_vehicle = present


@dataclass
class DecisionLog:
    """
    Record of a single traffic cycle decision.
    
    Attributes:
        cycle_number: The traffic cycle number (1-indexed)
        zone_a_id: Identifier for zone A
        zone_a_count: Vehicle count in zone A
        zone_a_signal: Signal state assigned to zone A
        zone_b_id: Identifier for zone B
        zone_b_count: Vehicle count in zone B
        zone_b_signal: Signal state assigned to zone B
        explanation: Textual explanation of the decision
    """
    cycle_number: int
    zone_a_id: str
    zone_a_count: int
    zone_a_signal: SignalState
    zone_b_id: str
    zone_b_count: int
    zone_b_signal: SignalState
    explanation: str


@dataclass
class SystemState:
    """
    Complete state of the traffic management system at a point in time.
    
    Attributes:
        cycle_number: Current cycle number
        zone_a: State of zone A
        zone_b: State of zone B
        last_tie_winner: Zone ID that won the last tie (for alternation)
    """
    cycle_number: int
    zone_a: TrafficZone
    zone_b: TrafficZone
    last_tie_winner: str | None
