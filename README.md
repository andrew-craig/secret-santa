# Secret Santa Assignment

A Python script that randomly assigns Secret Santa recipients with support for partner constraints.

## Features

- ✅ Random assignment of Secret Santa recipients
- ✅ Each person gives to exactly one recipient
- ✅ Each person receives from exactly one giver
- ✅ No one is assigned to themselves
- ✅ No one is assigned to their partner
- ✅ Validates assignments to ensure all constraints are met

## Usage

### Basic Usage

Run the script:

```bash
python3 secret_santa.py
```

### Customizing Participants

Edit the `secret_santa.py` file and modify the `participants` list:

```python
participants = [
    "Alice",
    "Bob",
    "Charlie",
    "Diana",
    "Eve",
    "Frank"
]
```

### Adding Partner Constraints

Edit the `partners` dictionary to specify who is partnered with whom:

```python
partners = {
    "Alice": "Bob",
    "Bob": "Alice",
    "Charlie": "Diana",
    "Diana": "Charlie"
}
```

**Note:** Partner relationships must be bidirectional (if Alice's partner is Bob, then Bob's partner must be Alice).

### Example Output

```
==================================================
SECRET SANTA ASSIGNMENT
==================================================

Participants: 6
  - Alice (partner: Bob)
  - Bob (partner: Alice)
  - Charlie (partner: Diana)
  - Diana (partner: Charlie)
  - Eve
  - Frank

Generating assignments...

✅ Assignment successful!

==================================================
ASSIGNMENTS
==================================================
Alice           → Frank
Bob             → Eve
Charlie         → Bob
Diana           → Alice
Eve             → Charlie
Frank           → Diana

==================================================

Note: Keep these assignments secret!
```

## How It Works

The script uses a randomized assignment algorithm with validation:

1. Shuffles the list of participants
2. Attempts to assign each person a valid recipient
3. Validates that no one is assigned to themselves or their partner
4. If assignment fails, retries (up to 1000 attempts)
5. Validates the final assignment meets all constraints

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## License

MIT License - See LICENSE file for details