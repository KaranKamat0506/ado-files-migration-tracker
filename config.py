"""
Centralised configuration — loads secrets from environment / .env
and defines all application constants.
"""

import os

# ── Azure DevOps connection ─────────────────────────────────────────
# All values must be provided via environment variables or .env file
# No hardcoded defaults for security
ADO_ORG = os.getenv("ADO_ORG", "")
ADO_PROJECT = os.getenv("ADO_PROJECT", "")
ADO_REPO = os.getenv("ADO_REPO", "")
ADO_BRANCH = os.getenv("ADO_BRANCH", "main")
ADO_PAT = os.getenv("ADO_PAT", "")
API_VERSION = "7.1-preview.1"

# ── Release versions available in the UI ────────────────────────────
# Customize these based on your release naming convention
RELEASES: list[str] = [
    "1.0.0",
    "1.1.0",
    "1.2.0",
]

# ── Folder mapping ──────────────────────────────────────────────────
# Display name  →  actual scripts path in the repo
# Customize these based on your repository structure
FOLDER_MAP: dict[str, str] = {
    "folder1": "folder1/scripts",
    "folder2": "folder2/scripts",
    "folder3": "folder3/scripts",
}
