#To activate environment

conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env

#From within the virtual environment, install the required packages specified in the "requirements.txt" file you created:

pip install -r requirements.txt
pip install pytest # (only if you'll be writing tests)

#From within the virtual environment, demonstrate your ability to run the Python script from the command-line:

python robo_advisor.py