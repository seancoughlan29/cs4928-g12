### "Towards Automated Detection of Inline Code Comment Smells"

#### Project Overview
This project is aimed at identifying and analyzing inline code comments to detect "smells"—patterns that may indicate deeper issues such as vague comments, beautification, tasks. The detection is automated through a series of Python scripts and Jupyter notebooks that utilize machine learning models and heuristics.

#### Repository Structure
- `dataset.json`: Contains the dataset adopted from a previous research.
- `augmented_dataset.json`: Contains the augmented version of the adopted dataset including code-comment pairs.
- `models.ipynb`: Contains the training and evaluation of seven machine learning models used in comment smell detection.
- `OpenAI.py`: Python script integrating OpenAI's API for processing and analyzing comments in the adopted dataset.
- `OpenAI_augmented.py`: Enhanced version of the OpenAI integration for processing the augmented dataset.
- `requirements.txt`: Lists all Python dependencies required to run the scripts and notebooks.

#### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab to run `.ipynb` files
- API keys for OpenAI, if applicable

#### Setup and Installation
1. Clone the repository to your local machine.
2. Install the necessary Python packages:
   ```
   pip install -r requirements.txt
   ```
3. If using OpenAI scripts, ensure your API keys are set in your environment variables.

#### Running the Notebooks
- Open the notebook (`models.ipynb`).
- Execute the cells in order to perform the analysis or training described in each notebook.

#### Running the Scripts
- To run the OpenAI integration scripts, use:
  ```
  python OpenAI.py
  ```
  or
  ```
  python OpenAI_augmented.py
  ```
  These scripts will interface with the OpenAI API to analyze comment smells using the provided models and heuristics.


### Note:
Ensure you have configured all necessary API keys and dependencies before running the scripts or notebooks. For detailed analysis and custom configurations, refer to the specific notebook or script documentation within the files.