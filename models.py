"""
Domain models used across the application.
"""

from dataclasses import dataclass, field


@dataclass
class FileItem:
    """A single file / folder entry returned by Azure DevOps."""

    name: str
    path: str
    url: str
    is_folder: bool
    web_url: str = ""
    added_by: str = ""
    added_date: str = ""
    updated_by: str = ""
    updated_date: str = ""
