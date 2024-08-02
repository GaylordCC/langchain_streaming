# Create the virtual enviroment
python3 -m venv venv

# Active the virtual enviroment
source venv/bin/activate

# Python version of the project
Python 3.12.1

# Install the dependicies
pip install -r requirements.txt

# Run python project
python3 main.py
python3 main_streaming.py

# Run the server for each endpoint file:
uvicorn main_streaming_endpoint:app --reload
uvicorn chatopenai_streaming_endpoint:app --reload
uvicorn azureopenai_streaming_endpoint:app --reload

# Open the project in the browser
    localhost:8000
    localhost:8000/docs