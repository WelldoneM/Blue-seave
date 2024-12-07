# Budget Tracker Client Application

## Overview
The Budget Tracker Client Application allows users to:
- Sign up and log in.
- Add expenses with auto-categorization using SageMaker/OpenAI.
- Fetch user spending summaries (budget vs. actual spending).
- Retrieve notifications for exceeded budgets.
- A sample user (username: `newuser`, password: `password123`) is included to help with testing. This client interacts with a preconfigured server that handles all backend processing.

## System Requirements
- Python 3.7+
- Required Python libraries:
  - `requests`
  - `matplotlib`
  - `configparser`
- Install dependencies using:

## How to Run
1. Save the client script to a file, e.g., `client.py`.
2. Open a terminal in the script directory.
3. Run the program using:

## Step-by-Step Flow
### Sign Up
1. Choose option 1 (Sign Up).
2. Enter a new username, email, and password to register.
3. A confirmation message will be displayed if registration is successful.

### Log In
1. Choose option 2 (Log In).
2. Enter your username and password.
3. Successful login will save the session token in a configuration file for future use.

### Fetch User Data
1. Choose option 3 (Fetch User Data).
2. This retrieves your spending data, including actual spending and budgets.
3. A bar chart visualizing your data (`budget_vs_spending.png`) will also be saved in the current directory.

### Fetch Alerts
1. Choose option 4 (Fetch Alerts).
2. This retrieves and displays notifications for budgets exceeded.

### Add Expense
1. Choose option 5 (Add Expense).
2. Enter a description and amount for the expense.
3. The system categorizes the expense (using SageMaker/OpenAI) and adds it to your records.

## Sample User
- **Username**: newuser
- **Password**: password123

## Brief Command Description
- **Sign Up**: Registers a new user with a username, email, and password.
- **Log In**: Authenticates the user and stores their session token.
- **Fetch User Data**: Retrieves and visualizes user expenses vs. budgets.
- **Fetch Alerts**: Displays notifications for exceeded budgets.
- **Add Expense**: Adds a new expense with auto-categorization.

