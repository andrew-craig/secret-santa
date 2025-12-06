#!/usr/bin/env python3
"""
Secret Santa Assignment Script

This script randomly assigns Secret Santa recipients to participants,
ensuring that:
- Each person gives to exactly one recipient
- Each person receives from exactly one giver
- No one is assigned to themselves
- No one is assigned to their partner
"""

import random
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Optional


def create_valid_assignment(
    participants: List[str],
    partners: Dict[str, str]
) -> Optional[Dict[str, str]]:
    """
    Create a valid Secret Santa assignment.

    Args:
        participants: List of participant names
        partners: Dictionary mapping each person to their partner (if any)

    Returns:
        Dictionary mapping giver -> recipient, or None if no valid assignment exists
    """
    max_attempts = 1000

    for attempt in range(max_attempts):
        # Create a shuffled copy of participants as potential recipients
        recipients = participants.copy()
        random.shuffle(recipients)

        assignment = {}
        available_recipients = recipients.copy()

        valid = True
        for giver in participants:
            # Find a valid recipient for this giver
            found = False
            for i, recipient in enumerate(available_recipients):
                # Check if this is a valid assignment
                if recipient == giver:
                    continue  # Can't give to yourself
                if giver in partners and partners[giver] == recipient:
                    continue  # Can't give to your partner

                # Valid assignment found
                assignment[giver] = recipient
                available_recipients.pop(i)
                found = True
                break

            if not found:
                # No valid recipient for this giver, try again
                valid = False
                break

        if valid:
            return assignment

    return None


def validate_assignment(
    assignment: Dict[str, str],
    participants: List[str],
    partners: Dict[str, str]
) -> bool:
    """Validate that an assignment meets all constraints."""
    # Check everyone is assigned
    if set(assignment.keys()) != set(participants):
        return False

    # Check everyone receives exactly once
    if set(assignment.values()) != set(participants):
        return False

    # Check no self-assignments
    for giver, recipient in assignment.items():
        if giver == recipient:
            return False

    # Check no partner assignments
    for giver, recipient in assignment.items():
        if giver in partners and partners[giver] == recipient:
            return False

    return True


def load_participants(yaml_file: str = "participants.yaml") -> tuple[List[str], Dict[str, str]]:
    """
    Load participants and their partners from a YAML file.

    Args:
        yaml_file: Path to the YAML file containing participants

    Returns:
        Tuple of (participants list, partners dictionary)

    Raises:
        FileNotFoundError: If the YAML file doesn't exist
        ValueError: If the YAML file is invalid
    """
    yaml_path = Path(yaml_file)

    if not yaml_path.exists():
        raise FileNotFoundError(
            f"Participants file '{yaml_file}' not found.\n"
            f"Please create it using 'participants.yaml.template' as a reference."
        )

    try:
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")

    if not isinstance(data, dict):
        raise ValueError("YAML file must contain a dictionary")

    if 'participants' not in data:
        raise ValueError("YAML file must contain a 'participants' key")

    participants_data = data['participants']
    if not isinstance(participants_data, list):
        raise ValueError("'participants' must be a list")

    participants = []
    partners = {}

    for participant in participants_data:
        if isinstance(participant, str):
            # Simple participant without partner
            participants.append(participant)
        elif isinstance(participant, dict):
            # Participant with partner info
            for name, info in participant.items():
                participants.append(name)
                if isinstance(info, dict) and 'partner' in info:
                    partner_name = info['partner']
                    partners[name] = partner_name
        else:
            raise ValueError(f"Invalid participant format: {participant}")

    return participants, partners


def main():
    """Main function to run Secret Santa assignment."""

    # Load participants from YAML file
    try:
        participants, partners = load_participants()
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ ERROR: Invalid YAML file: {e}")
        sys.exit(1)

    print("=" * 50)
    print("SECRET SANTA ASSIGNMENT")
    print("=" * 50)
    print(f"\nParticipants: {len(participants)}")
    for participant in participants:
        partner = partners.get(participant, "None")
        print(f"  - {participant}" + (f" (partner: {partner})" if partner != "None" else ""))

    print("\nGenerating assignments...")

    assignment = create_valid_assignment(participants, partners)

    if assignment is None:
        print("\n❌ ERROR: Could not find a valid assignment!")
        print("This might happen if the constraints are too restrictive.")
        sys.exit(1)

    # Validate the assignment
    if not validate_assignment(assignment, participants, partners):
        print("\n❌ ERROR: Assignment validation failed!")
        sys.exit(1)

    print("\n✅ Assignment successful!\n")
    print("=" * 50)
    print("ASSIGNMENTS")
    print("=" * 50)

    for giver in sorted(assignment.keys()):
        recipient = assignment[giver]
        print(f"{giver:15} → {recipient}")

    print("\n" + "=" * 50)
    print("\nNote: Keep these assignments secret!")


if __name__ == "__main__":
    main()
