import json
import os
import subprocess
import streamlit as st

st.title("Lean Backtesting Interface")

# Paths and algorithm details
algo_type = st.text_input("Algorithm Id", value="BinanceMovingAverageCrossover")
config_path = st.text_input("Config Path", value="Launcher/config.json")
launcher_dll = st.text_input("Launcher DLL", value="QuantConnect.Lean.Launcher.dll")

if 'process' not in st.session_state:
    st.session_state.process = None

start = st.button("Start Backtest")
stop = st.button("Stop Backtest")
load = st.button("Load Results")

if start:
    if st.session_state.process is None:
        cmd = ["dotnet", launcher_dll, "--config", config_path, "--algorithm-id", algo_type]
        st.session_state.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        st.success("Backtest started")
    else:
        st.warning("Backtest already running")

if stop:
    if st.session_state.process is not None:
        st.session_state.process.terminate()
        st.session_state.process.wait()
        st.session_state.process = None
        st.success("Backtest stopped")
    else:
        st.warning("No backtest running")

if st.session_state.process is not None:
    st.subheader("Live Output")
    for line in st.session_state.process.stdout:
        st.text(line)

if load:
    result_file = os.path.join(os.getcwd(), f"{algo_type}-summary.json")
    if os.path.exists(result_file):
        with open(result_file) as f:
            st.json(json.load(f))
    else:
        st.warning("Result file not found")
