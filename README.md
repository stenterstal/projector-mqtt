<div align="center">
    <h1>Projector-MQTT</h1>
    <p>Python based MQTT client for servicing a DLPDLCR2000EVM Projector with Homeassistant-MQTT<br>
    Includes a Flask management portal for configuration</p>
</div>

# Run dev environment
### 1. Create venv and install dependencies
```bash
sudo apt install python3-venv # If not installed

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```
### 2. Run the app
```bash
sudo python3 app.py
```
To only run the flask frontend;
```bash
# Run from root of the project, not inside the dashboard folder
flask run --host=0.0.0.0 --port=5000 --reload
```