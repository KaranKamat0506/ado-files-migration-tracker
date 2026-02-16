"""
Azure DevOps REST API client.

Handles authentication, request construction, and response parsing
for the Git Items and Commits endpoints.
"""

import base64
import re
import urllib.parse

import requests

from config import ADO_BRANCH, ADO_ORG, ADO_PAT, ADO_PROJECT, ADO_REPO, API_VERSION
from models import FileItem


def _auth_headers() -> dict[str, str]:
    """Return HTTP headers with Basic-auth from the configured PAT."""
    token_b64 = base64.b64encode(f":{ADO_PAT}".encode()).decode()
    return {
        "Authorization": f"Basic {token_b64}",
        "Content-Type": "application/json",
    }


def _encoded_project() -> str:
    return urllib.parse.quote(ADO_PROJECT)


# ── File listing ────────────────────────────────────────────────────
def list_files(folder_path: str) -> list[FileItem]:
    """
    List every item (files + sub-folders) under *folder_path*
    on the configured branch of the ADO Git repository.
    """
    url = (
        f"{ADO_ORG}/{_encoded_project()}/_apis/git/repositories/{ADO_REPO}"
        f"/items?scopePath=/{folder_path}"
        f"&recursionLevel=Full"
        f"&versionDescriptor.version={ADO_BRANCH}"
        f"&versionDescriptor.versionType=branch"
        f"&api-version={API_VERSION}"
    )

    resp = requests.get(url, headers=_auth_headers(), timeout=30)
    resp.raise_for_status()

    items = []
    for entry in resp.json().get("value", []):
        file_path = entry.get("path", "")
        encoded_path = urllib.parse.quote(file_path, safe="/")
        web_url = (
            f"{ADO_ORG}/{_encoded_project()}/_git/{ADO_REPO}"
            f"?path={encoded_path}"
            f"&version=GB{ADO_BRANCH}"
        )
        items.append(
            FileItem(
                name=file_path.rsplit("/", 1)[-1],
                path=file_path,
                url=entry.get("url", ""),
                web_url=web_url,
                is_folder=entry.get("isFolder", False),
            )
        )
    return items


# ── Commit / author lookup ──────────────────────────────────────────
def enrich_with_authors(items: list[FileItem]) -> None:
    """
    For each FileItem fetch commit history and populate:
      - added_by / added_date   → person who first committed the file
      - updated_by / updated_date → person who last modified the file
    """
    base = (
        f"{ADO_ORG}/{_encoded_project()}/_apis/git/repositories/{ADO_REPO}"
        f"/commits"
    )
    headers = _auth_headers()

    for item in items:
        if item.is_folder:
            continue
        try:
            # Fetch ALL commits for this file path (oldest → newest via API)
            params = {
                "searchCriteria.itemPath": item.path,
                "searchCriteria.itemVersion.version": ADO_BRANCH,
                "searchCriteria.itemVersion.versionType": "branch",
                "api-version": API_VERSION,
            }
            resp = requests.get(base, headers=headers, params=params, timeout=20)
            resp.raise_for_status()
            commits = resp.json().get("value", [])

            if commits:
                # ADO returns newest first → index 0 = latest, index -1 = oldest
                oldest = commits[-1]

                # Added = first ever commit for this file
                item.added_by = oldest.get("author", {}).get("name", "")
                raw_added = oldest.get("author", {}).get("date", "")
                if raw_added:
                    item.added_date = raw_added[:10]

                # Updated = only if someone modified after initial add
                if len(commits) > 1:
                    latest = commits[0]
                    item.updated_by = latest.get("author", {}).get("name", "")
                    raw_updated = latest.get("author", {}).get("date", "")
                    if raw_updated:
                        item.updated_date = raw_updated[:10]
        except Exception:
            # Non-critical — leave fields blank rather than crashing
            pass


# ── Filtering ───────────────────────────────────────────────────────
def filter_by_release(
    items: list[FileItem],
    release: str,
) -> list[FileItem]:
    """
    Keep only files whose name starts with ``V{release}.``

    Example: release ``1.29.1`` -> matches ``V1.29.1.1``, ``V1.29.1.2``, ...
    """
    prefix = f"V{release}."
    return [
        f
        for f in items
        if not f.is_folder and f.name.upper().startswith(prefix.upper())
    ]


# ── Natural sorting ─────────────────────────────────────────────────
def _natural_sort_key(item: FileItem):
    """
    Split the filename into text and numeric parts so that
    V1.29.0.2 sorts before V1.29.0.10.
    """
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", item.name)
    ]


def sort_naturally(items: list[FileItem]) -> list[FileItem]:
    """Return items sorted in natural (human-friendly) order."""
    return sorted(items, key=_natural_sort_key)
