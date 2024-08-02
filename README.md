# Create the virtual enviroment
python3 -m venv venv

# Active the virtual enviroment
source venv/bin/activate

# Python version of the project
Python 3.12.1

# Install the dependicies
pip install -r requirements.txt

# Run the uvicorn's server:
uvicorn langchain_streaming.streaming:app --reload

# Open the project in the browser
    localhost:8000
    localhost:8000/docs



# Run python file: main_documentation.py
python3 main_documentation.py