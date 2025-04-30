# CodeFiesta Notebooks
A repository for [Jupyter Notebooks](https://jupyter.org/) and Machine Learning.

### Getting Started

Run the following commands to install needed python modules and run a local Jupyter server:

```shell
# On MacOS, unless you are running Anaconda you will most likely need to alias python3 + pip3
echo 'alias python='/usr/bin/python3'' >> ~/.zprofile
echo 'alias pip='/usr/bin/pip3'' >> ~/.zprofile

# Create a virtual environment (if you haven't already)
python -m venv .venv

# Activate the environment
source .venv/bin/activate

# Intall the module dependencies 
pip install -r requirements.txt

# For Spacy modules you will most likely need to download trained pipelines
python -m spacy download en_core_web_trf
python -m spacy download en_core_web_lg
python -m spacy download en_core_web_sm

# Run the local Jupyter server
python -m notebook

# Once finished, you can exit the virtual environment
deactivate

```
