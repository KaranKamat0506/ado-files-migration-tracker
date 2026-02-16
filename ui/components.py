"""
Reusable Streamlit UI components.

Each public function renders one logical section of the page and
returns any user-selected values the caller needs.
"""

from __future__ import annotations

import streamlit as st

from config import ADO_BRANCH, ADO_REPO, FOLDER_MAP, RELEASES
from models import FileItem
from ui.styles import CUSTOM_CSS
from utils.excel_export import generate_excel, get_excel_filename


# ── Page setup & global styles ──────────────────────────────────────
def inject_styles() -> None:
    """Inject custom CSS into the page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ── Header ──────────────────────────────────────────────────────────
def render_header() -> None:
    """Blue gradient header bar with repo / branch info."""
    st.markdown(
        f"""
        <div class="header-bar">
            <h1>DB Migration &mdash; Release Scripts Viewer</h1>
            <p>Repository: <b>{ADO_REPO}</b> &nbsp;|&nbsp; Branch: <b>{ADO_BRANCH}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Release & folder selectors ──────────────────────────────────────
def render_selectors() -> tuple[str, str, str]:
    """
    Two-column dropdowns for release and folder.

    Returns
    -------
    (selected_release, selected_folder_label, scripts_path)
    """
    col1, col2 = st.columns(2)

    with col1:
        selected_release = st.selectbox(
            "Select Release",
            options=RELEASES,
            index=0,
            help="Files matching V{release}.* will be shown",
        )

    with col2:
        selected_folder = st.selectbox(
            "Select Folder",
            options=list(FOLDER_MAP.keys()),
            help="Folder path inside the repository",
        )

    scripts_path = FOLDER_MAP[selected_folder]

    # Info strip showing resolved path
    st.markdown(
        f"""
        <div class="metric-card">
            <span class="label">Scripts path in repo</span><br/>
            <span class="value" style="font-size:1rem;">{scripts_path}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return selected_release, selected_folder, scripts_path


# ── Results ─────────────────────────────────────────────────────────
def render_results(
    matched: list[FileItem],
    selected_release: str,
    selected_folder: str,
    scripts_path: str,
) -> None:
    """Display summary metrics and the file list table."""
    st.divider()

    # Summary cards
    m1, m2, m3 = st.columns(3)
    with m1:
        _metric_card("Release", selected_release)
    with m2:
        _metric_card("Folder", selected_folder)
    with m3:
        _metric_card("Scripts Found", str(len(matched)))

    if matched:
        # Download Excel button
        excel_data = generate_excel(matched, selected_release, selected_folder)
        filename = get_excel_filename(selected_release, selected_folder)
        
        st.download_button(
            label="📥 Download as Excel",
            data=excel_data,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary",
        )
        
        st.divider()
        _render_file_table(matched)
    else:
        st.warning(
            f"No scripts found matching **V{selected_release}.*** "
            f"in `{scripts_path}` on branch **{ADO_BRANCH}**."
        )


# ── Private helpers ─────────────────────────────────────────────────
def _metric_card(label: str, value: str) -> None:
    st.markdown(
        f'<div class="metric-card">'
        f'<span class="label">{label}</span><br/>'
        f'<span class="value">{value}</span></div>',
        unsafe_allow_html=True,
    )


def _render_file_table(files: list[FileItem]) -> None:
    rows = "".join(
        f"<tr>"
        f'<td style="text-align:center;">{idx}</td>'
        f'<td class="file-name"><a href="{f.web_url}" target="_blank">{f.name}</a></td>'
        f"<td>{f.added_by}</td>"
        f"<td>{f.added_date}</td>"
        f"</tr>"
        for idx, f in enumerate(files, start=1)
    )
    headers = (
        '<th style="width:60px; text-align:center;">#</th>'
        "<th>File Name</th>"
        "<th>Added By</th>"
        "<th>Added On</th>"
    )

    st.markdown(
        f"""
        <table class="file-table">
            <thead><tr>{headers}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )
