# Phishing URL Detector Using Machine Learning

This is a Flask-based web application that uses machine learning to detect phishing URLs. The app takes a URL as input, analyzes its features, and predicts whether it is legitimate or phishing.

## Features

- User-friendly web interface for entering URLs
- Machine learning model to predict phishing URLs
- Real-time results with prediction probability
- Visualizations for feature importance and model performance

## Installation

### Prerequisites

- Python 3.6 or above
- pip (Python package installer)
- Virtual environment (optional but recommended)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/phishing-url-detector.git
   cd phishing-url-detector
2.Create a virtual environment (optional but recommended):
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3.Install the required packages:
pip install -r requirements.txt
4.Download or generate the dataset and place it in the data directory.
