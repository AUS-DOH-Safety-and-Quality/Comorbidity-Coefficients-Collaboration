# Comorbidity-Coefficients-Collaboration
Source code for computing comorbidity scores and predictive performance of the Charlson, MACSS, and Elixhauser comorbidity models.

## Prerequisites

- Python installed on your system

## Setup and Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AUS-DOH-Safety-and-Quality/Comorbidity-Coefficients-Collaboration.git

   cd Comorbidity-Coefficients-Collaboration
   ```

2. **Install uv**
   This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   Alternatively, you can install it via pip: `pip install uv`.

   For further detail, visit https://docs.astral.sh/uv/getting-started/installation/

3. **Install dependencies**
   Run the following command to create a virtual environment and install dependencies defined in `pyproject.toml`:
   ```bash
   uv sync
   ```

4. **Activate the environment**
   ```bash
   # Windows
   .venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

## Data Preparation

The project expects data files to be in the `datasets/` directory. Currently, the `datasets/` directory contains example files to demonstrate the expected structure and columns that should be present in your own datasets. The naming of the files should match the examples. However, you decide to use different names for your data files, then you will need to change the details in the `config.yaml` file.

If you provide the training and testing files e.g. `charlson_training.csv` and `charlson_testing.csv`, you can use the `create_scored_datasets.py` file to create the `charlson_training_scored.csv` and `charlson_testing_scored.csv` files respectively. However, the creation of these files is optional for your own exploratory purposes. 

```bash
python create_scored_datasets.py
```

The comparison notebook uses `original_weights.json` to calculate scores for the original Charlson and Elixhauser methods on-the-fly, so no pre-processing step is required to use `method_comparison.ipynb`

## Running the Analysis

The analysis is divided into training specific models and then comparing their performance.

### 1. Train Models

Navigate to the `MORT/` (Mortality) or `LOS/` (Length of Stay) directories and run the respective notebooks to train the models.

**Mortality Models (`MORT/`):**

- `MORT_charlson.ipynb`: Trains the Charlson models, In hospital mortality (DEATH), one-year mortality (ONE_YEAR_MORT), thirty-day mortality (THIRTY_DAY_MORT), and five-year mortality (FIVE_YEAR_MORT).
- `MORT_elix.ipynb`: Trains the Elixhauser models, In hospital mortality (DEATH), one-year mortality (ONE_YEAR_MORT), thirty-day mortality (THIRTY_DAY_MORT), and five-year mortality (FIVE_YEAR_MORT).
- `MORT_macss.ipynb`: Trains the MACSS models, In hospital mortality (DEATH), one-year mortality (ONE_YEAR_MORT), thirty-day mortality (THIRTY_DAY_MORT), and five-year mortality (FIVE_YEAR_MORT).

**Length of Stay Models (`LOS/`):**

- `LOS_charlson.ipynb`: Trains a linear regression model with charlson comorbidities for length of stay prediction. Note that the length of stay has been log transformed (LOG_LOSS).
- `LOS_elix.ipynb`: Trains a linear regression model with elixhauser comorbidities for length of stay prediction. Note that the length of stay has been log transformed (LOG_LOSS).
- `LOS_macss.ipynb`:Trains a linear regression model with MACSS comorbidities for length of stay prediction. Note that the length of stay has been log transformed (LOG_LOSS).

*Note: Running these notebooks will save the trained models to the `models/` directory with the target name included (e.g., `models/mort_elix_DEATH.joblib`).*

### 2. Compare Performance

Once the models are trained, you can compare the performance.

- Open and run `PERFORMANCE_COMPARISON/method_comparison.ipynb`.
- This notebook will:
  - Iterate through multiple targets (e.g., `DEATH`,`THIRTY_DAY_MORT`,`ONE_YEAR_MORT`,`FIVE_YEAR_MORT`,`LOG_LOS`).
  - Load the trained models from the `models/` directory.
  - Calculate scores using the original weights from `original_weights.json`.
  - Calculate performance metrics (AUC for classification, R2 for regression).
  - Display comparison tables for each target.

## Project Structure

- `datasets/`: Contains CSV data files.
- `models/`: Stores trained model files (`.joblib`).
- `MORT/`: Notebooks for mortality prediction models.
- `LOS/`: Notebooks for length of stay prediction models.
- `PERFORMANCE_COMPARISON/`: Notebooks for comparing model results.
- `config.yml`: Configuration file for model parameters and file paths.
- `create_scored_datasets.py`: Script to generate datasets with original weight scores.
- `original_weights.json`: JSON file containing the original weights for Charlson and Elixhauser.

## ICD Codes

The `ICD_codes/` folder contains three csv files, `charlson_comorbidities.csv`, `elixhauser_comorbidities.csv`, and `MACSS_comorbidities.csv`. Each file contains the ICD codes and their matching group that maps to the columns in the training and testing files. For example, `CHARLSON_GROUP` `CVD` in `charlson_comorbidities.csv` maps to `C_CVD` in `charlson_training.csv` and `charlson_testing.csv`
