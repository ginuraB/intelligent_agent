# config.py
# Central configuration file for the agent.
# Loads environment variables and defines constants.

import os
from dotenv import load_dotenv

# Load environment variables from a .env file at the project root
load_dotenv()

# --- Application Settings ---
AGENT_NAME = "Intelligent Agent v1.0"

# --- API & Security Settings ---
# Retrieves the supervisor's email from the .env file.
# The second argument is a default value if the variable is not found.
SUPERVISOR_EMAIL = os.getenv("SUPERVISOR_EMAIL", "default.supervisor@example.com")

# --- Agent Behavior Settings ---
# Time in seconds for the agent to wait before checking for new emails again.
SLEEP_TIME_SECONDS = 300  # 5 minutes

print("Configuration loaded.")

