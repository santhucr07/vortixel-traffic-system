#!/usr/bin/env python3
"""
VortixelAI Traffic Management System - Main Entry Point

This module provides the main entry point for running traffic management simulations.
It demonstrates the complete system with realistic scenarios and varied vehicle counts.

Command-line usage:
    python main.py                          # Run default demonstration
    python main.py --cycles 5               # Run with 5 cycles
    python main.py --input updates.txt      # Read vehicle counts from file
    python main.py --output results.txt     # Write logs to file
    python main.py -c 5 -i updates.txt -o results.txt  # Combined options
"""

import argparse
import sys
from pathlib import Path

from src.simulation_controller import SimulationController
from src.decision_engine import DecisionEngine
from src.decision_logger import DecisionLogger
from src.models import TrafficZone


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="VortixelAI Traffic Management System - Intelligent Traffic Signal Control",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Run default demonstration
  python main.py --cycles 5               # Run with 5 cycles
  python main.py --input updates.txt      # Read vehicle counts from file
  python main.py --output results.txt     # Write logs to file
  python main.py -c 5 -i updates.txt -o results.txt  # Combined options

Input file format (one line per cycle):
  zone_a_count,zone_b_count
  15,8
  5,20
  10,10
        """
    )
    
    parser.add_argument(
        "-c", "--cycles",
        type=int,
        metavar="N",
        help="Number of cycles to simulate (overrides input file length if provided)"
    )
    
    parser.add_argument(
        "-i", "--input",
        type=str,
        metavar="FILE",
        help="Input file with vehicle count updates (CSV format: zone_a_count,zone_b_count)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        metavar="FILE",
        help="Output file for decision logs (default: console)"
    )
    
    return parser.parse_args()


def read_vehicle_counts_from_file(filepath: str) -> list[tuple[int, int]]:
    """
    Read vehicle count updates from a file.
    
    Args:
        filepath: Path to the input file
        
    Returns:
        List of (zone_a_count, zone_b_count) tuples
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is invalid
    """
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")
    
    updates = []
    with open(path, 'r') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            try:
                parts = line.split(',')
                if len(parts) != 2:
                    raise ValueError(f"Line {line_num}: Expected 2 values, got {len(parts)}")
                
                count_a = int(parts[0].strip())
                count_b = int(parts[1].strip())
                
                if count_a < 0 or count_b < 0:
                    raise ValueError(f"Line {line_num}: Vehicle counts cannot be negative")
                
                updates.append((count_a, count_b))
            except ValueError as e:
                raise ValueError(f"Invalid format in {filepath} at line {line_num}: {e}")
    
    if not updates:
        raise ValueError(f"No valid vehicle count updates found in {filepath}")
    
    return updates


def get_default_scenario() -> list[tuple[int, int]]:
    """
    Get the default demonstration scenario.
    
    Returns:
        List of (zone_a_count, zone_b_count) tuples
    """
    return [
        (15, 8),   # Cycle 1: Zone A has clear priority
        (5, 20),   # Cycle 2: Zone B has clear priority
        (10, 10),  # Cycle 3: Equal counts - Zone A gets priority (default)
        (10, 10),  # Cycle 4: Equal counts - Zone B gets priority (alternating)
        (0, 0),    # Cycle 5: Both zones empty - Zone A gets priority (alternating)
        (25, 5),   # Cycle 6: Zone A has significantly more vehicles
        (3, 18),   # Cycle 7: Zone B has significantly more vehicles
        (12, 12),  # Cycle 8: Equal counts - Zone B gets priority (alternating)
        (0, 15),   # Cycle 9: Only Zone B has vehicles
        (20, 0),   # Cycle 10: Only Zone A has vehicles
    ]


def write_output(content: str, output_file: str | None):
    """
    Write content to file or console.
    
    Args:
        content: Content to write
        output_file: Output file path (None for console)
    """
    if output_file:
        path = Path(output_file)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Output written to: {output_file}")
    else:
        print(content)


def main():
    """
    Run the VortixelAI Traffic Management System demonstration.
    
    This example demonstrates:
    - Cycles where one zone has clear priority (higher vehicle count)
    - Cycles with equal vehicle counts showing alternation
    - Edge cases like zero vehicles
    - Multiple cycles to show the system behavior over time
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    # Determine vehicle count updates
    try:
        if args.input:
            vehicle_count_updates = read_vehicle_counts_from_file(args.input)
            print(f"✓ Loaded vehicle count updates from: {args.input}")
        else:
            vehicle_count_updates = get_default_scenario()
            print("✓ Using default demonstration scenario")
        
        # Override number of cycles if specified
        if args.cycles:
            if args.cycles > len(vehicle_count_updates):
                print(f"Warning: Requested {args.cycles} cycles but only {len(vehicle_count_updates)} updates available")
                print(f"         Using {len(vehicle_count_updates)} cycles")
            else:
                vehicle_count_updates = vehicle_count_updates[:args.cycles]
                print(f"✓ Limited to {args.cycles} cycles")
        
        num_cycles = len(vehicle_count_updates)
        
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Build output content
    output_lines = []
    
    # Print header
    output_lines.append("=" * 70)
    output_lines.append("VortixelAI Traffic Management System")
    output_lines.append("Intelligent Traffic Signal Control Demonstration")
    output_lines.append("=" * 70)
    output_lines.append("")
    
    # Initialize system components
    output_lines.append("Initializing system components...")
    decision_engine = DecisionEngine(default_zone_id="Zone_A")
    decision_logger = DecisionLogger()
    simulation_controller = SimulationController(decision_engine, decision_logger)
    output_lines.append("✓ Decision Engine initialized")
    output_lines.append("✓ Decision Logger initialized")
    output_lines.append("✓ Simulation Controller initialized")
    output_lines.append("")
    
    # Create two traffic zones
    output_lines.append("Creating traffic zones...")
    zone_a = TrafficZone("Zone_A", 0)
    zone_b = TrafficZone("Zone_B", 0)
    output_lines.append(f"✓ {zone_a.zone_id} created")
    output_lines.append(f"✓ {zone_b.zone_id} created")
    output_lines.append("")
    
    # Scenario description
    if not args.input:
        output_lines.append("Defining simulation scenario...")
        output_lines.append("This simulation demonstrates various traffic conditions:")
        output_lines.append("  • Clear priority scenarios (one zone has more vehicles)")
        output_lines.append("  • Equal traffic scenarios (alternating behavior)")
        output_lines.append("  • Edge cases (zero vehicles, high traffic)")
        output_lines.append("")
    
    output_lines.append(f"Scenario configured: {num_cycles} traffic cycles")
    output_lines.append("")
    
    # Run the simulation
    output_lines.append("-" * 70)
    output_lines.append("SIMULATION EXECUTION")
    output_lines.append("-" * 70)
    output_lines.append("")
    
    try:
        decision_logs = simulation_controller.run_simulation(
            zone_a=zone_a,
            zone_b=zone_b,
            num_cycles=num_cycles,
            vehicle_count_updates=vehicle_count_updates
        )
        
        # Format decision logs
        for log in decision_logs:
            formatted_log = decision_logger.format_log(log)
            output_lines.append(formatted_log)
        
        # Print summary
        output_lines.append("")
        output_lines.append("-" * 70)
        output_lines.append("SIMULATION SUMMARY")
        output_lines.append("-" * 70)
        output_lines.append(f"Total cycles executed: {num_cycles}")
        output_lines.append(f"Decision logs generated: {len(decision_logs)}")
        output_lines.append("")
        
        # Analyze results
        zone_a_green_count = sum(1 for log in decision_logs if log.zone_a_signal.value == "GREEN")
        zone_b_green_count = sum(1 for log in decision_logs if log.zone_b_signal.value == "GREEN")
        
        output_lines.append("Signal Distribution:")
        output_lines.append(f"  Zone A received GREEN: {zone_a_green_count} times ({zone_a_green_count/num_cycles*100:.1f}%)")
        output_lines.append(f"  Zone B received GREEN: {zone_b_green_count} times ({zone_b_green_count/num_cycles*100:.1f}%)")
        output_lines.append("")
        
        # Verify safety constraint
        safety_violations = sum(
            1 for log in decision_logs 
            if log.zone_a_signal.value == "GREEN" and log.zone_b_signal.value == "GREEN"
        )
        
        if safety_violations == 0:
            output_lines.append("✓ Safety constraint verified: No cycles with both zones GREEN")
        else:
            output_lines.append(f"✗ Safety violation detected: {safety_violations} cycles with both zones GREEN")
        
        output_lines.append("")
        output_lines.append("=" * 70)
        output_lines.append("Simulation completed successfully!")
        output_lines.append("=" * 70)
        
        # Write output
        output_content = "\n".join(output_lines)
        write_output(output_content, args.output)
        
    except Exception as e:
        print(f"Error during simulation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
