"""
Excel export utilities for generating downloadable reports.
"""

import io
from datetime import datetime

import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill

from models import FileItem


def generate_excel(
    files: list[FileItem],
    release: str,
    folder: str,
) -> bytes:
    """
    Generate an Excel file from a list of FileItem objects.

    Parameters
    ----------
    files : list[FileItem]
        List of file items to export
    release : str
        Release version (e.g., "1.29.1")
    folder : str
        Folder path (e.g., "de/noncost2")

    Returns
    -------
    bytes
        Excel file content as bytes
    """
    # Prepare data for DataFrame
    data = []
    for idx, file_item in enumerate(files, start=1):
        data.append({
            "#": idx,
            "File Name": file_item.name,
            "Full Path": file_item.path,
            "Added By": file_item.added_by,
            "Added On": file_item.added_date,
            "ADO URL": file_item.web_url,
        })

    df = pd.DataFrame(data)

    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Release Scripts")

        # Get the workbook and worksheet for formatting
        workbook = writer.book
        worksheet = writer.sheets["Release Scripts"]

        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

        # Add header row formatting (bold)
        header_fill = PatternFill(start_color="0078D4", end_color="0078D4", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")

        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")

    output.seek(0)
    return output.getvalue()


def get_excel_filename(release: str, folder: str) -> str:
    """
    Generate a filename for the Excel export.

    Parameters
    ----------
    release : str
        Release version
    folder : str
        Folder path

    Returns
    -------
    str
        Filename like "Release_1.29.1_de-noncost2_2024-02-14.xlsx"
    """
    timestamp = datetime.now().strftime("%Y-%m-%d")
    folder_safe = folder.replace("/", "-").replace("_", "-")
    return f"Release_{release}_{folder_safe}_{timestamp}.xlsx"
