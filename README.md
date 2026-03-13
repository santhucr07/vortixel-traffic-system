# VortixelAI Traffic Management Prototype

An intelligent traffic signal control system that manages two traffic zones dynamically, optimizing traffic flow based on real-time vehicle counts.

## Features

- **Dynamic Signal Priority**: Automatically assigns GREEN/RED signals based on vehicle density
- **Fair Alternation**: When traffic is equal, the system alternates fairly between zones
- **Safety-First Design**: Enforces mutual exclusion - both zones never receive GREEN simultaneously
- **Transparent Decision-Making**: Every signal assignment is logged with clear explanations
- **Multi-Cycle Simulation**: Supports running multiple traffic cycles with configurable vehicle counts
- **Property-Based Testing**: Comprehensive test coverage using Hypothesis for correctness validation

## Requirements

- Python 3.10 or higher
- pip (Python package installer)

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Main Simulation

Execute the main simulation with a predefined scenario:

```bash
python main.py
```

This runs a demonstration with varied vehicle counts across multiple cycles and outputs decision logs to the console.

### Running Tests

Run all unit tests:
```bash
pytest tests/unit/
```

Run all property-based tests:
```bash
pytest tests/property/
```

Run integration tests:
```bash
pytest tests/integration/
```

Run all tests:
```bash
pytest
```

### Using the System Programmatically

```python
from src.models import TrafficZone
from src.decision_engine import DecisionEngine
from src.decision_logger import DecisionLogger
from src.simulation_controller import SimulationController

# Initialize traffic zones
zone_a = TrafficZone("Zone_A", 0)
zone_b = TrafficZone("Zone_B", 0)

# Create decision engine and logger
engine = DecisionEngine(default_zone_id="Zone_A")
logger = DecisionLogger()

# Create simulation controller
controller = SimulationController(engine, logger)

# Define vehicle count updates for each cycle
vehicle_updates = [
    (10, 5),   # Cycle 1: Zone A has more vehicles
    (3, 8),    # Cycle 2: Zone B has more vehicles
    (6, 6),    # Cycle 3: Equal counts (alternates)
]

# Run simulation
logs = controller.run_simulation(zone_a, zone_b, 3, vehicle_updates)

# Output results
controller.output_logs(logs)
```

## Architecture Overview

The system follows a layered architecture with clear separation of concerns:

### Components

1. **TrafficZone** (`src/models.py`)
   - Represents a monitored area with vehicle detection and signal control
   - Tracks vehicle count and current signal state
   - Validates input constraints (non-negative counts, non-empty IDs)

2. **DecisionEngine** (`src/decision_engine.py`)
   - Core decision-making logic for signal priority assignment
   - Compares vehicle counts and determines signal states
   - Implements fair alternation for equal traffic scenarios
   - Validates safety constraints (mutual exclusion)

3. **DecisionLogger** (`src/decision_logger.py`)
   - Creates structured decision log entries
   - Generates human-readable explanations for each decision
   - Formats output for display and analysis

4. **SimulationController** (`src/simulation_controller.py`)
   - Orchestrates multi-cycle simulation execution
   - Coordinates between DecisionEngine and DecisionLogger
   - Manages vehicle count updates between cycles
   - Outputs formatted decision logs

### Data Flow

```
Vehicle Counts → DecisionEngine → Signal Assignments
                       ↓
                 DecisionLogger → Decision Log Entry
                       ↓
             SimulationController → Formatted Output
```

### Decision Algorithm

The system uses a deterministic algorithm:

1. **Compare vehicle counts** between zones
2. **Assign signals** based on priority:
   - Higher count → GREEN signal
   - Lower count → RED signal
   - Equal counts → Alternate fairly (Zone A default for first tie)
3. **Validate safety** constraint (at most one GREEN)
4. **Log decision** with explanation

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── models.py                 # Core data models (TrafficZone, SignalState, DecisionLog)
│   ├── decision_engine.py        # Signal priority assignment logic
│   ├── decision_logger.py        # Decision logging and formatting
│   └── simulation_controller.py  # Multi-cycle simulation orchestration
├── tests/
│   ├── unit/                     # Unit tests for individual components
│   ├── property/                 # Property-based tests using Hypothesis
│   └── integration/              # End-to-end integration tests
├── main.py                       # Main entry point with example simulation
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Testing

The project uses a dual testing approach:

### Unit Tests
- Verify specific examples and edge cases
- Test error conditions and input validation
- Ensure individual components work correctly

### Property-Based Tests
- Verify universal properties across all inputs using Hypothesis
- Test correctness properties like safety constraints, alternation fairness, and log completeness
- Run with minimum 100 iterations per property

### Test Coverage
- 12 correctness properties validated through property-based testing
- Comprehensive unit test coverage for all components
- Integration tests for end-to-end scenarios

## License

This is a prototype system for demonstration and educational purposes.

## Contributing

This is a prototype project. For questions or suggestions, please contact the development team.
