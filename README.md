# CNN-Based Intrusion Detection System

This project implements a Convolutional Neural Network (CNN) for detecting various types of network attacks. The application is built using Streamlit, allowing users to interact with the model and analyze network traffic data.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Model Architecture](#model-architecture)
- [Database Management](#database-management)

## Project Overview

This project provides an interface for a CNN-based Intrusion Detection System (IDS). It enables users to load datasets, pre-process data, train models, and test the model's performance. The system can identify various network attacks, including Denial of Service (DoS), User to Root (U2R), Probe, and Root to Local (R2L) attacks.

## Features

- **User Authentication**: Sign up, log in, and manage user profiles.
- **Dataset Loading and Pre-processing**: Load the NSL-KDD dataset, view feature sets, and inspect pre-processed data.
- **Model Training and Testing**: Train the CNN model on pre-processed data, analyze the training phase, and test the model with attack samples.
- **Real-Time Attack Detection**: Upload CSV files for real-time attack detection using the trained model.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kirti9510/CNN-IDS.git
   cd CNN-IDS
   ```

2. **Create and activate a virtual environment (optional but recommended)**:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: `env\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download and prepare the datasets**:
   - Download the NSL-KDD dataset from [here](https://www.unb.ca/cic/datasets/nsl.html).
   - Place the dataset in the `Samples and Details` folder.

## Usage

1. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Interact with the app**:
   - **Home**: Introduction and navigation to other sections.
   - **Login**: Log in with your username and password.
   - **Sign Up**: Create a new account.
   - **Profiles**: View registered users.
   - **Dataset details and Pre-processed output**: View the dataset and pre-processed features.
   - **Analyze Training Phase**: Analyze the model training process.
   - **Result Analysis**: View model performance metrics.
   - **Test the Model**: Test the model with attack or normal samples.

## Model Architecture

The CNN model used in this project is designed to process network traffic data, and it consists of the following layers:

- Convolutional layers with ReLU activation
- MaxPooling layers
- Flattening layer
- Fully connected Dense layers with Dropout for regularization
- Softmax output layer for multi-class classification

## Database Management

SQLite is used for managing user credentials:

- **create_usertable()**: Creates the user table.
- **add_userdata()**: Adds new user data.
- **login_user()**: Authenticates users.
- **view_all_users()**: Retrieves all user data.

---
