"""
DB Migration – Release Scripts Viewer

Entry point.  Run with:
    streamlit run app.py
"""

import requests
import streamlit as st

from services.ado_client import (
    enrich_with_authors,
    filter_by_release,
    list_files,
    sort_naturally,
)
from ui.components import (
    inject_styles,
    render_header,
    render_results,
    render_selectors,
)


def main() -> None:
    st.set_page_config(
        page_title="DB Migration \u2013 Release Scripts",
        page_icon="\U0001F4C2",
        layout="wide",
    )

    # Global styles
    inject_styles()

    # Page sections
    render_header()
    selected_release, selected_folder, scripts_path = render_selectors()

    # Fetch action
    if st.button("Fetch Scripts", type="primary", use_container_width=True):
        with st.spinner("Fetching file list from Azure DevOps\u2026"):
            try:
                all_items = list_files(scripts_path)
                matched = filter_by_release(all_items, selected_release)
                matched = sort_naturally(matched)

                if matched:
                    enrich_with_authors(matched)

            except requests.exceptions.HTTPError as exc:
                st.error(
                    f"ADO API error: {exc.response.status_code} "
                    f"\u2013 {exc.response.text[:300]}"
                )
                return
            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to Azure DevOps. "
                    "Check your configuration in .env file."
                )
                return
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
                return

        render_results(matched, selected_release, selected_folder, scripts_path)


if __name__ == "__main__":
    main()
