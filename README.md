# NAMA M1 Diagnostic Assistant

A guided customer-service diagnostic app based on the supplied NAMA M1 troubleshooting flowchart.

## What to install

1. Install Python 3.10 or newer from <https://www.python.org/downloads/>.
2. Open Terminal (macOS) or Command Prompt/PowerShell (Windows) in this folder.
3. Create and activate a virtual environment (recommended):

   **Windows PowerShell**

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **macOS / Linux**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install the app dependency:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Run the app

```bash
python -m streamlit run app.py
```

The app opens in your default browser. It normally uses `http://localhost:8501`.

## Using the diagnostic

- Select the customer's answer from each dropdown and click **Next**.
- Complete each yellow action, then click **Action completed — continue**.
- Use **Back** to correct the last entry or **Restart diagnosis** to begin again.
- A red panel gives the resolution. A lighter red panel gives any required AU-team follow-up.

## Important implementation note

The flowchart's error-message diamonds were implemented as dropdowns containing the labels shown on their outgoing branches. For the SPIN path, these are THERM ERROR, SPIN ERROR, ACCELL ERROR, and no error message. For the BLEND path, these are BLEND ERROR, THERM ERROR, and no error message.
