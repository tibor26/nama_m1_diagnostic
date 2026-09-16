import streamlit as st


st.set_page_config(page_title="NAMA M1 Diagnostic Assistant", page_icon="🥛", layout="centered")


NODES = {
    "power_up": {
        "type": "question",
        "title": "Does the unit power up?",
        "options": {"Yes": "assemble_unit", "No": "power_switch"},
    },
    "power_switch": {
        "type": "question",
        "title": "Is the power switch ON?",
        "options": {"Yes": "check_power", "No": "switch_on"},
    },
    "switch_on": {
        "type": "action",
        "title": "Switch the power switch ON.",
        "next": "switch_result",
    },
    "switch_result": {
        "type": "question",
        "title": "Is the issue resolved?",
        "options": {"Yes": "no_fault", "No": "check_power"},
    },
    "check_power": {
        "type": "action",
        "title": "Check the power cable and wall plug.",
        "next": "power_result",
    },
    "power_result": {
        "type": "question",
        "title": "Is the issue resolved?",
        "options": {"Yes": "no_fault", "No": "replace_motor_followup"},
    },
    "assemble_unit": {
        "type": "action",
        "title": "Fit the fully assembled M1 jug onto the motor base, then close the lid and close the spout.",
        "next": "test_blend",
    },
    "test_blend": {
        "type": "action",
        "title": "Add 1 cup of almonds and 3 cups of water, then press Start.",
        "note": "Using almonds is essential for an accurate diagnosis.",
        "next": "blend_ok",
    },
    "blend_ok": {
        "type": "question",
        "title": "Does the BLEND cycle run correctly?",
        "help": "The motor should run at high speed and the almonds should be blended. The water should become milky.",
        "options": {"Yes": "prepare_spin", "No": "blend_error"},
    },
    "blend_error": {
        "type": "question",
        "title": "What error message is displayed?",
        "options": {
            "BLEND ERROR": "replace_blade_cage",
            "THERM ERROR": "wait_hour_blend",
            "No error message": "send_video",
        },
    },
    "wait_hour_blend": {
        "type": "action",
        "title": "Wait 1 hour.",
        "next": "therm_still_on",
    },
    "therm_still_on": {
        "type": "question",
        "title": "Is the THERM ERROR still displayed?",
        "options": {"Yes": "replace_motor_followup", "No": "no_fault"},
    },
    "prepare_spin": {
        "type": "action",
        "title": "Open the spout, drain the water, and wait 10 seconds for the SPIN cycle to start.",
        "next": "spin_ok",
    },
    "spin_ok": {
        "type": "question",
        "title": "Does the SPIN cycle run correctly?",
        "help": "Please note: when the SPIN cycle finishes, semi-dried pulp is deposited on the inner wall of the stainless steel basket.",
        "options": {"Yes": "no_fault", "No": "spin_error"},
    },
    "spin_error": {
        "type": "question",
        "title": "What error message is displayed?",
        "options": {
            "THERM ERROR": "wait_hour_blend",
            "SPIN ERROR": "replace_whole_followup",
            "ACCELL ERROR": "replace_motor",
            "No error message": "vibration",
        },
    },
    "vibration": {
        "type": "question",
        "title": "Is there excessive vibration?",
        "options": {"Yes": "replace_blade_cage", "No": "replace_motor"},
    },
    "no_fault": {
        "type": "resolution",
        "title": "Unit operates as intended; no faults found.",
        "tone": "success",
    },
    "replace_blade_cage": {
        "type": "resolution",
        "title": "Replace the blade cage assembly.",
        "tone": "error",
    },
    "replace_motor": {
        "type": "resolution",
        "title": "Replace the motor base.",
        "tone": "error",
    },
    "replace_motor_followup": {
        "type": "resolution",
        "title": "Replace the motor base.",
        "followup": "Check with the AU team whether this unit should be sent back for further checking.",
        "tone": "error",
    },
    "replace_whole_followup": {
        "type": "resolution",
        "title": "Replace the whole unit.",
        "followup": "Check with the AU team whether this unit should be sent back for further checking.",
        "tone": "error",
    },
    "send_video": {
        "type": "resolution",
        "title": "Send a video to the AU team so they can check which part needs to be replaced. Alternatively, replace the whole unit.",
        "tone": "error",
    },
}


def reset():
    st.session_state.node = "power_up"
    st.session_state.history = []


if "node" not in st.session_state:
    reset()

st.markdown(
    """
    <style>
    .block-container {max-width: 760px; padding-top: 2rem;}
    .diagnostic-card {border-radius: 14px; padding: 1.2rem 1.4rem; margin: 1rem 0;}
    .question {background: #e9f8ef; border-left: 7px solid #25b95b;}
    .action {background: #fff3cc; border-left: 7px solid #f5b700;}
    .resolution {background: #ffe4e4; border-left: 7px solid #e51c23;}
    .followup {background: #ffecec; border: 1px solid #ff9c9c; border-radius: 10px; padding: 1rem; margin-top: .8rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("NAMA M1 Diagnostic Assistant")
st.caption("Guide the customer through one step at a time. Complete each action before continuing.")

node_id = st.session_state.node
node = NODES[node_id]
step = len(st.session_state.history) + 1

if node["type"] == "question":
    st.markdown(
        f'<div class="diagnostic-card question"><strong>Question {step}</strong><br><h3>{node["title"]}</h3></div>',
        unsafe_allow_html=True,
    )
    if node.get("help"):
        st.info(node["help"])
    answer = st.selectbox("Select the customer's answer", ["Select an answer…", *node["options"].keys()])
    if st.button("Next", type="primary", disabled=answer == "Select an answer…", use_container_width=True):
        st.session_state.history.append((node_id, answer))
        st.session_state.node = node["options"][answer]
        st.rerun()

elif node["type"] == "action":
    st.markdown(
        f'<div class="diagnostic-card action"><strong>Action {step}</strong><br><h3>{node["title"]}</h3></div>',
        unsafe_allow_html=True,
    )
    if node.get("note"):
        st.warning(node["note"])
    if st.button("Action completed — continue", type="primary", use_container_width=True):
        st.session_state.history.append((node_id, "Completed"))
        st.session_state.node = node["next"]
        st.rerun()

else:
    st.markdown(
        f'<div class="diagnostic-card resolution"><strong>Resolution</strong><br><h2>{node["title"]}</h2></div>',
        unsafe_allow_html=True,
    )
    if node.get("followup"):
        st.markdown(f'<div class="followup"><strong>Follow-up:</strong> {node["followup"]}</div>', unsafe_allow_html=True)
    st.button("Start a new diagnosis", type="primary", on_click=reset, use_container_width=True)

if st.session_state.history and node["type"] != "resolution":
    if st.button("← Back"):
        previous_node, _ = st.session_state.history.pop()
        st.session_state.node = previous_node
        st.rerun()

with st.sidebar:
    st.header("Session")
    st.write(f"Steps completed: {len(st.session_state.history)}")
    if st.button("Restart diagnosis"):
        reset()
        st.rerun()
    st.divider()
    st.caption("Internal customer-service diagnostic guide for the NAMA M1 plant-based milk maker.")
