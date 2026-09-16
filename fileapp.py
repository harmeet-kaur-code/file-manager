"""
File Manager — Streamlit UI
A safe, friendly front end for basic file CRUD operations
(create, read, update/rename/append/overwrite, delete).

All operations are scoped to a local "workspace" folder next to this
script, so the app never touches files outside it. Run with:

    streamlit run app.py
"""

from pathlib import Path
from datetime import datetime
import streamlit as st

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------
WORKSPACE = Path(__file__).parent / "workspace"
WORKSPACE.mkdir(exist_ok=True)

st.set_page_config(page_title="File Manager", page_icon="🗂️", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(180deg, #f7fafc 0%, #eef2f6 100%);
    }
    .block-container { padding-top: 1.6rem; max-width: 1000px; }

    .hero {
        background: linear-gradient(120deg, #0f2f3d 0%, #14532d 140%);
        border-radius: 20px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 8px 22px rgba(15, 47, 61, 0.18);
    }
    .hero h1 { margin: 0; font-size: 2rem; font-weight: 800; color: #eafff4; }
    .hero p { margin: 0.35rem 0 0 0; color: #b9e4cf; font-size: 0.95rem; }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 14px;
        padding: 0.85rem 1rem;
        border: 1px solid #e3e9ee;
        box-shadow: 0 3px 12px rgba(20, 40, 60, 0.05);
    }
    div[data-testid="stMetricValue"] { color: #0f5132; font-weight: 700; }
    div[data-testid="stMetricLabel"] { color: #6b7c8a; font-weight: 500; }

    div[data-testid="stForm"], .card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.5rem 1.7rem;
        border: 1px solid #e3e9ee;
        box-shadow: 0 3px 14px rgba(20, 40, 60, 0.05);
    }

    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(120deg, #14532d, #1b7a43);
        color: white;
        border: none;
        border-radius: 9px;
        padding: 0.5rem 1.4rem;
        font-weight: 600;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 14px rgba(27, 122, 67, 0.35);
        color: white;
    }

    button[kind="secondary"] {
        background: #fff0f0 !important;
        color: #b3261e !important;
    }

    section[data-testid="stSidebar"] {
        background: #0f2f3d;
    }
    section[data-testid="stSidebar"] * { color: #eafff4 !important; }
    section[data-testid="stSidebar"] .stRadio > label { color: #eafff4 !important; }

    .stTextArea textarea, .stTextInput input {
        font-family: 'JetBrains Mono', monospace;
        border-radius: 10px !important;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #e3e9ee;
    }

    .badge {
        display: inline-block;
        background: #e6f4ea;
        color: #146c2e;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def safe_path(name: str) -> Path:
    """Resolve a user-given filename inside the workspace, blocking path escape."""
    candidate = (WORKSPACE / name).resolve()
    if WORKSPACE.resolve() not in candidate.parents and candidate != WORKSPACE.resolve():
        raise ValueError("Invalid file name.")
    return candidate


def list_files():
    return sorted([p for p in WORKSPACE.iterdir() if p.is_file()], key=lambda p: p.name.lower())


def human_size(num_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.0f} {unit}" if unit == "B" else f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


# ----------------------------------------------------------------------
# Header + stats
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🗂️ File Manager</h1>
        <p>Create, read, update and delete files — all safely sandboxed inside a local workspace folder.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

files = list_files()
total_size = sum(f.stat().st_size for f in files)

c1, c2, c3 = st.columns(3)
c1.metric("📄 Files", len(files))
c2.metric("💾 Total Size", human_size(total_size))
c3.metric("📁 Workspace", str(WORKSPACE.name))

st.write("")

# ----------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------
st.sidebar.markdown("## 🧭 Menu")
page = st.sidebar.radio(
    "Choose an action",
    ["📂 File Explorer", "📝 Create File", "📖 Read File", "✏️ Update File", "🗑️ Delete File"],
    label_visibility="collapsed",
)

# ---------------- File Explorer ----------------
if page == "📂 File Explorer":
    st.subheader("📂 Workspace Files")
    if not files:
        st.info("No files yet — head to **Create File** to add your first one.")
    else:
        rows = [
            {
                "Name": f.name,
                "Size": human_size(f.stat().st_size),
                "Modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            }
            for f in files
        ]
        st.dataframe(rows, use_container_width=True, hide_index=True)

# ---------------- Create File ----------------
elif page == "📝 Create File":
    st.subheader("📝 Create a New File")
    with st.form("create_form", clear_on_submit=True):
        name = st.text_input("File name", placeholder="notes.txt")
        content = st.text_area("Content", height=180, placeholder="Type what you want to write...")
        submitted = st.form_submit_button("Create File")

    if submitted:
        if not name.strip():
            st.error("Please enter a file name.")
        else:
            try:
                path = safe_path(name.strip())
                if path.exists():
                    st.error(f"❌ A file named **{name}** already exists.")
                else:
                    path.write_text(content)
                    st.success(f"✅ File **{name}** created successfully.")
            except Exception as err:
                st.error(f"An error occurred: {err}")

# ---------------- Read File ----------------
elif page == "📖 Read File":
    st.subheader("📖 Read a File")
    if not files:
        st.info("No files yet — create one first.")
    else:
        options = [f.name for f in files]
        choice = st.selectbox("Select a file", options)
        path = safe_path(choice)
        try:
            content = path.read_text()
            st.markdown(f'<span class="badge">{human_size(path.stat().st_size)}</span>', unsafe_allow_html=True)
            st.text_area("File content", content, height=280, disabled=True)
            st.download_button("⬇️ Download file", content, file_name=choice)
        except Exception as err:
            st.error(f"An error occurred: {err}")

# ---------------- Update File ----------------
elif page == "✏️ Update File":
    st.subheader("✏️ Update a File")
    if not files:
        st.info("No files yet — create one first.")
    else:
        options = [f.name for f in files]
        choice = st.selectbox("Select a file", options)
        path = safe_path(choice)

        operation = st.radio(
            "What would you like to do?",
            ["Rename", "Append", "Overwrite"],
            horizontal=True,
        )

        if operation == "Rename":
            with st.form("rename_form"):
                new_name = st.text_input("New file name")
                submitted = st.form_submit_button("Rename")
            if submitted:
                try:
                    new_path = safe_path(new_name.strip())
                    if not new_name.strip():
                        st.error("Please enter a new file name.")
                    elif new_path.exists():
                        st.error(f"❌ A file named **{new_name}** already exists.")
                    else:
                        path.rename(new_path)
                        st.success(f"✅ Renamed **{choice}** → **{new_name}**.")
                        st.rerun()
                except Exception as err:
                    st.error(f"An error occurred: {err}")

        elif operation == "Append":
            with st.form("append_form", clear_on_submit=True):
                data = st.text_area("Text to append", height=140)
                submitted = st.form_submit_button("Append")
            if submitted:
                try:
                    with open(path, "a") as fs:
                        fs.write("\n" + data)
                    st.success(f"✅ Appended to **{choice}**.")
                except Exception as err:
                    st.error(f"An error occurred: {err}")

        elif operation == "Overwrite":
            current = path.read_text() if path.exists() else ""
            with st.form("overwrite_form"):
                data = st.text_area("New content (replaces everything)", value=current, height=200)
                submitted = st.form_submit_button("Overwrite")
            if submitted:
                try:
                    path.write_text(data)
                    st.success(f"✅ Overwrote **{choice}**.")
                except Exception as err:
                    st.error(f"An error occurred: {err}")

# ---------------- Delete File ----------------
elif page == "🗑️ Delete File":
    st.subheader("🗑️ Delete a File")
    if not files:
        st.info("No files yet — nothing to delete.")
    else:
        options = [f.name for f in files]
        choice = st.selectbox("Select a file to delete", options)
        confirm = st.checkbox(f"I understand this will permanently delete **{choice}**.")
        if st.button("Delete File", type="secondary", disabled=not confirm):
            try:
                safe_path(choice).unlink()
                st.success(f"🗑️ Deleted **{choice}**.")
                st.rerun()
            except Exception as err:
                st.error(f"An error occurred: {err}")