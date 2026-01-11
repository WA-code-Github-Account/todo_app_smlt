"""Streamlit UI for the Todo CLI application - Modern Royal Blue Theme!"""

import streamlit as st
from todo.storage import storage
from todo.models import Task, TaskStatus
from todo.exceptions import EmptyTitleError
from todo.utils import validate_title

# Custom CSS - Royal Blue Modern Theme
st.markdown("""
<style>
    /* Main background - Deep Royal Blue */
    .stApp {
        background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 50%, #1e3a5f 100%);
    }

    /* Headers - White */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
    }

    /* All labels and text - WHITE */
    label, .stTextInput label, .stTextArea label, .stSelectbox label, .stCheckbox label {
        color: #ffffff !important;
        font-weight: bold !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1b2a 0%, #1b263b 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* Buttons - Royal Blue Gradient */
    .stButton > button {
        background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        font-size: 1rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #00b4d8 0%, #0077b6 100%);
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0, 180, 216, 0.4);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0, 119, 182, 0.3);
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        color: white !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%) !important;
        border-radius: 10px;
    }

    /* Input fields - White background, Dark text */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #ffffff !important;
        border: 3px solid #00b4d8 !important;
        border-radius: 12px !important;
        color: #000000 !important;
        font-weight: bold !important;
    }
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #666666 !important;
    }

    /* Select box */
    .stSelectbox > div > div > div {
        background: #ffffff !important;
        color: #000000 !important;
    }

    /* Select box text */
    .stSelectbox div[data-baseweb="select"] > div {
        color: #000000 !important;
    }

    /* Select box dropdown container */
    div[data-baseweb="select"] > div[data-testid="stPopover"] {
        background: #ffffff !important;
        border: 2px solid #00b4d8 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0, 180, 216, 0.4) !important;
    }

    /* Select box options */
    [data-baseweb="select"] [data-testid="stSelectbox"] [data-baseweb="option"] {
        color: #000000 !important;
        background: #ffffff !important;
        padding: 10px !important;
        border-radius: 5px !important;
        margin: 2px 0 !important;
    }

    /* Select box options hover state */
    [data-baseweb="select"] [data-testid="stSelectbox"] [data-baseweb="option"]:hover {
        background: #00b4d8 !important;
        color: #ffffff !important;
    }

    /* Checkbox */
    .stCheckbox > label {
        color: #ffffff !important;
    }

    /* Success messages */
    .stSuccess {
        background: linear-gradient(135deg, #00b4d8 0%, #00ff88 100%) !important;
        border-radius: 10px;
        color: white !important;
    }

    /* Error messages */
    .stError {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%) !important;
        border-radius: 10px;
        color: white !important;
    }

    /* Divider */
    hr {
        border-color: #00b4d8 !important;
    }

    /* All p text white */
    p, li {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Todo App", page_icon="✅", layout="wide", initial_sidebar_state="expanded")

    # Custom Title
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 0;">
            ✅ <span style="background: linear-gradient(135deg, #00d4ff, #0077b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Todo Master</span> ✅
        </h1>
        <p style="color: #ffffff; font-size: 1.2rem;">Your Ultimate Task Manager</p>
    </div>
    """, unsafe_allow_html=True)

    # Session state
    if 'task_to_edit' not in st.session_state:
        st.session_state.task_to_edit = None
    if 'show_edit_form' not in st.session_state:
        st.session_state.show_edit_form = False

    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h2 style="font-size: 2.5rem;">🎯</h2>
            <h3 style="color: #ffffff !important;">Task Manager</h3>
        </div>
        """, unsafe_allow_html=True)

        all_tasks = storage.get_all()
        complete_tasks = [t for t in all_tasks if t.status == TaskStatus.COMPLETE]
        incomplete_tasks = [t for t in all_tasks if t.status == TaskStatus.INCOMPLETE]

        st.divider()

        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", len(all_tasks))
        with col2:
            st.metric("Done", len(complete_tasks))
        with col3:
            st.metric("Pending", len(incomplete_tasks))

        # Progress bar
        if all_tasks:
            progress = len(complete_tasks) / len(all_tasks)
            st.markdown(f"""
            <div style="margin: 20px 0;">
                <p style="color: #ffffff; margin-bottom: 8px;">📊 Progress: {int(progress*100)}%</p>
                <div style="background: rgba(0, 180, 216, 0.3); height: 25px; border-radius: 15px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #0077b6, #00d4ff); width: {progress*100}%; height: 100%; border-radius: 15px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        if st.button("🗑️ Clear Completed", type="secondary", use_container_width=True):
            for task in complete_tasks:
                storage.delete(task.id)
            st.rerun()

        # Tips
        st.markdown("""
        <div style="background: rgba(0, 119, 182, 0.3); padding: 15px; border-radius: 15px; margin-top: 20px;">
            <p style="color: #ffffff; font-weight: bold; margin: 0;">💡 Quick Tips</p>
            <ul style="color: #ffffff; font-size: 0.9rem; margin-top: 10px;">
                <li>Use checkbox to complete</li>
                <li>Click Edit to modify</li>
                <li>Filter to find tasks</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Tabs - White text for visibility
    tab1, tab2 = st.tabs(["📋 View Tasks", "➕ Add Task"])

    # ============ TAB 1: View Tasks ============
    with tab1:
        st.subheader("📋 Your Tasks")

        # Filter
        col1, col2 = st.columns([1, 4])
        with col1:
            status_filter = st.selectbox("🔍 Filter", ["All", "Complete", "Incomplete"])

        if status_filter == "Complete":
            tasks = [t for t in all_tasks if t.status == TaskStatus.COMPLETE]
        elif status_filter == "Incomplete":
            tasks = [t for t in all_tasks if t.status == TaskStatus.INCOMPLETE]
        else:
            tasks = all_tasks

        if not tasks:
            st.markdown("""
            <div style="text-align: center; padding: 50px 0;">
                <p style="font-size: 4rem;">📭</p>
                <p style="color: #ffffff; font-size: 1.5rem;">No tasks found!</p>
                <p style="color: #ffffff;">Add a new task to get started.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            tasks.sort(key=lambda x: x.id)

            for task in tasks:
                with st.container():
                    c1, c2, c3, c4, c5, c6 = st.columns([0.7, 1, 5, 0.5, 1, 1])

                    with c1:
                        st.markdown(f"<div style='background: linear-gradient(135deg, #0077b6, #00b4d8); color: white; font-weight: bold; padding: 10px 15px; border-radius: 12px; text-align: center; font-size: 1.2rem; box-shadow: 0 4px 10px rgba(0, 180, 216, 0.3);'>#{task.id}</div>", unsafe_allow_html=True)

                    with c2:
                        new_val = st.checkbox(
                            "✓",
                            value=(task.status == TaskStatus.COMPLETE),
                            key=f"check_{task.id}",
                            label_visibility="collapsed"
                        )
                        if new_val != (task.status == TaskStatus.COMPLETE):
                            storage.toggle_status(task.id)
                            st.rerun()

                    with c3:
                        status_icon = "✅" if task.status == TaskStatus.COMPLETE else "⏳"
                        # White text for visibility
                        st.markdown(f"<span style='color: #ffffff; font-size: 1.3rem; font-weight: bold;'>{status_icon} {task.title}</span>", unsafe_allow_html=True)
                        if task.description:
                            st.markdown(f"<span style='color: #ffffff; font-size: 1rem;'>📝 {task.description}</span>", unsafe_allow_html=True)

                    with c4:
                        st.write("")

                    with c5:
                        if st.button("✏️ Edit", key=f"edit_{task.id}", use_container_width=True):
                            st.session_state.task_to_edit = task
                            st.session_state.show_edit_form = True
                            st.rerun()

                    with c6:
                        if st.button("🗑️", key=f"delete_{task.id}", type="secondary", use_container_width=True):
                            try:
                                storage.delete(task.id)
                                st.rerun()
                            except:
                                pass

                    # Edit form
                    if st.session_state.show_edit_form and st.session_state.task_to_edit and st.session_state.task_to_edit.id == task.id:
                        st.divider()
                        with st.form(f"edit_form_{task.id}"):
                            st.markdown(f"### ✏️ Editing Task #{task.id}")
                            new_title = st.text_input("Task Title", value=task.title, key="edit_title")
                            new_desc = st.text_area("Description", value=task.description, key="edit_desc")
                            c_btn1, c_btn2 = st.columns(2)
                            with c_btn1:
                                if st.form_submit_button("💾 Save", use_container_width=True):
                                    try:
                                        validated = validate_title(new_title)
                                        storage.update(task.id, title=validated, description=new_desc.strip())
                                        st.session_state.show_edit_form = False
                                        st.session_state.task_to_edit = None
                                        st.rerun()
                                    except EmptyTitleError:
                                        st.error("Title cannot be empty!")
                            with c_btn2:
                                if st.form_submit_button("❌ Cancel", use_container_width=True):
                                    st.session_state.show_edit_form = False
                                    st.session_state.task_to_edit = None
                                    st.rerun()
                    st.divider()

    # ============ TAB 2: Add Task ============
    with tab2:
        st.subheader("➕ Add New Task")

        with st.form("add_form", clear_on_submit=True):
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(0, 119, 182, 0.3), rgba(0, 180, 216, 0.2)); padding: 30px; border-radius: 20px; border: 2px solid #00b4d8;">
            """, unsafe_allow_html=True)

            title = st.text_input("📝 Task Title *", placeholder="Enter your task here...")

            desc = st.text_area("📄 Description", placeholder="Add more details (optional)", height=100)

            st.markdown("</div>", unsafe_allow_html=True)

            col_submit, col_space = st.columns([1, 4])
            with col_submit:
                submitted = st.form_submit_button("➕ Add Task", use_container_width=True)

            if submitted:
                if not title.strip():
                    st.error("❌ Title cannot be empty!")
                else:
                    try:
                        validated = validate_title(title)
                        new_task = Task(
                            id=0,
                            title=validated,
                            description=desc.strip(),
                            status=TaskStatus.INCOMPLETE
                        )
                        storage.add(new_task)
                        st.success("✅ Task added successfully!")
                        st.rerun()
                    except EmptyTitleError:
                        st.error("❌ Title cannot be empty!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

    # Footer
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0077b6, #00b4d8); padding: 30px; border-radius: 20px; margin-top: 50px; text-align: center; box-shadow: 0 4px 20px rgba(0, 180, 216, 0.4);">
        <p style="font-size: 1.5rem; color: white; margin: 0;">Made with ❤️ by <strong>A.Siddiqui®</strong></p>
        <p style="font-size: 1.1rem; color: #ffffff; margin-top: 10px;">🎓 GIAIC Student | 🆔 #200937</p>
        <p style="font-size: 1rem; color: rgba(255,255,255,0.8); margin-top: 15px;">✨ Todo Master v1.0</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
