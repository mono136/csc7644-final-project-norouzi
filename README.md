# csc7644-final-project-norouzi
# Battery State of Charge Insight and Diagnostic System for Multi-Condition Analysis

## Overview

This project presents an LLM-based diagnostic system for analyzing lithium-ion battery degradation under varying operating conditions. The system processes raw battery datasets, extracts cycle-level features, performs statistical analysis, and generates structured, human-readable engineering insights using a Large Language Model (LLM).

Unlike traditional methods that only provide numerical outputs, this system generates interpretable diagnostic insights that connect observed trends to battery physics.

This project is submitted as the final project for **CSC 7644: Applied LLM Development**.

---

## Key Features

- Load and process NASA Li-ion battery datasets (.mat files)
- Extract cycle-level features (capacity, current, temperature)
- Classify operating conditions (temperature, load type, load level)
- Perform degradation analysis using linear regression
- Identify fastest degradation conditions
- Generate structured LLM-based insights
- Detect anomalies in battery behavior
- Visualize degradation trends
- Support OpenAI and OpenRouter APIs

---

## Tech Stack and Architecture

### Technologies

- Python 3.10+
- NumPy, Pandas
- SciPy
- Matplotlib, Seaborn
- OpenAI / OpenRouter APIs
- python-dotenv

---

### System Architecture

- Data Loading (`src/loader.py`)                         --> Loads `.mat` battery datasets and extracts relevant variables 
- Preprocessing (`src/preprocessing.py`)                 --> Filters data and assigns condition-based labels
- Analysis (`src/analysis.py`)                           --> Computes degradation rates using linear regression and compares groups
- Visualization (`src/visualization.py`)                 --> Generates plots for group comparisons and single battery behavior
- LLM Reasoning (`src/prompts.py`, `src/llm_utils.py`)   --> Converts numerical results into structured explanations using prompts
- Main Application (`src/main.py`)                       --> Command-line interface for user interaction

---

## Setup Instructions and Run Application

### Prerequisites

- Python 3.10 or higher
- pip installed

---

### Installation

1. Download or clone the repository to your computer.
2. Open a terminal (Command Prompt, PowerShell, or Terminal) and navigate to the project root directory.
3. Install the required dependencies:
    pip install -r requirements.txt`

---

### Environment Setup

1. Copy the contents of `.env.example` into `.env`.
2. Add your API key(s):
   OPENROUTER_API_KEY=your_openrouter_key  
   OPENAI_API_KEY=your_openai_key  
3. Select ONE provider by uncommenting:
   #LLM_PROVIDER=openrouter  
   #LLM_PROVIDER=openai  
5. Save the file.

Note:
- You must have a valid API key for the selected provider.
- Do NOT upload your `.env` file to GitHub.

---

### Running the Application

After installing the dependencies and configuring the `.env` file:
1. Open a command-line interface on your system.
2. Navigate to the project root directory.
3. Run the following command:
    python src/main.py

---

## User Interaction

The application runs as a command-line interface (CLI). After launching, the user selects from a menu:
1. Temperature-based analysis  
2. Load type comparison  
3. Load level comparison  
4. Single battery analysis  

The system then:
- computes statistical summaries
- generates plots
- produces LLM-based diagnostic explanations

---

## Outputs

**Console**
- Statistical summaries
- LLM-generated explanations

**Plots**
- Degradation curves
- Group comparisons
- Single battery behavior

---

## Repository Organization

- `src/` – main application code  
  - `main.py` – CLI and workflow control  
  - `loader.py` – loads dataset  
  - `preprocessing.py` – cleans and labels data  
  - `analysis.py` – computes degradation metrics  
  - `visualization.py` – generates plots  
  - `prompts.py` – LLM prompt templates  
  - `llm_utils.py` – API calls 
- `data/` – battery dataset files  
- `evaluation/` – evaluation metrics  
- `outputs/` – generated plots and outputs  

---

## Methodology Summary

- Degradation estimated using linear regression (capacity vs cycle)
- Group comparisons based on slope
- Most negative slope indicates fastest degradation
- LLM explanations combine statistical results and battery physics

---

## Attributions

- NASA Li-ion Battery Dataset (Saha & Goebel, 2007)
- OpenAI API
- OpenRouter API
- SciPy, Matplotlib, Seaborn documentation

---

