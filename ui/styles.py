"""
All custom CSS injected into the Streamlit page.
Kept in one place so styling is easy to maintain.
"""

CUSTOM_CSS = """
<style>
/* ── Header gradient bar ────────────────────────────────────────── */
.header-bar {
    background: linear-gradient(90deg, #0078D4 0%, #50E6FF 100%);
    padding: 1.2rem 2rem;
    border-radius: 0.6rem;
    margin-bottom: 1.5rem;
}
.header-bar h1 {
    color: white;
    margin: 0;
    font-size: 1.6rem;
}
.header-bar p {
    color: #e0f0ff;
    margin: 0.2rem 0 0 0;
    font-size: 0.95rem;
}

/* ── Metric / info cards ────────────────────────────────────────── */
.metric-card {
    background: #f0f6ff;
    border-left: 4px solid #0078D4;
    border-radius: 0.4rem;
    padding: 1rem 1.2rem;
    margin-bottom: 0.5rem;
}
.metric-card .label  { font-size: 0.85rem; color: #555; }
.metric-card .value  { font-size: 1.3rem; font-weight: 700; color: #0078D4; }

/* ── File results table ─────────────────────────────────────────── */
.file-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.5rem;
}
.file-table th {
    background: #0078D4;
    color: white;
    text-align: left;
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
}
.file-table td {
    padding: 0.55rem 1rem;
    border-bottom: 1px solid #e8e8e8;
    font-size: 0.88rem;
}
.file-table tr:hover td { background: #f4f9ff; }
.file-name { font-weight: 600; }
.file-name a { color: #0078D4; text-decoration: none; }
.file-name a:hover { text-decoration: underline; }
</style>
"""
