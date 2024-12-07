import requests
import logging
import sys
import pathlib
import json
from configparser import ConfigParser
import matplotlib.pyplot as plt

############################################################
# Helper Functions
############################################################

def web_service_post(url, payload):
    try:
        response = requests.post(url, json=payload)
        if response.status_code in [200, 400, 401, 500]:
            return response
        else:
            return None
    except Exception as e:
        logging.error(f"Error in web_service_post: {str(e)}")
        return None

# def web_service_get(url):
#     try:
#         response = requests.get(url)
#         if response.status_code in [200, 400, 401, 500]:
#             return response
#         else:
#             return None
#     except Exception as e:
#         logging.error(f"Error in web_service_get: {str(e)}")
#         return None
def web_service_get(url):
    try:
        response = requests.get(url)
        return response
    except Exception as e:
        logging.error(f"Error in web_service_get: {str(e)}")
        return None
def visualize_and_save_user_data(data, filename='budget_vs_spending.png'):
    categories = [item["CategoryName"] for item in data]
    spent = [item["TotalAmount"] for item in data]
    budget = [item["BudgetAmount"] for item in data]

    x = range(len(categories))  # the label locations

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, budget, width=0.4, label='Budget', align='center')
    ax.bar(x, spent, width=0.4, label='Spent', align='edge')

    ax.set_xlabel('Category')
    ax.set_ylabel('Amount')
    ax.set_title('Budget vs. Actual Spending by Category')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()



def prompt():
    print("\n>> Choose a command:")
    print("   0 => Exit")
    print("   1 => Sign Up")
    print("   2 => Log In")
    print("   3 => Fetch User Data")
    print("   4 => Fetch Alerts")
    return input("Enter your choice: ").strip()

############################################################
# Command Functions
############################################################

def sign_up(baseurl):
    try:
        print("Enter your username: ")
        username = input().strip()
        print("Enter your email: ")
        email = input().strip()  # Add email field
        print("Enter your password: ")
        password = input().strip()

        payload = {
            "username": username,
            "email": email,  # Include email
            "password": password
        }

        url = f"{baseurl}/signup"
        print("Signing up...")

        # Send request
        response = web_service_post(url, payload)

        if response:
            print(f"Response Status: {response.status_code}")
            print(f"Response Body: {response.json()}")  # Log response
        else:
            print("\nFailed to contact server. Please try again.")

        # Handle response
        if response and response.status_code == 200:
            print("\nSign-up successful! Please log in to continue.")
        else:
            print(f"\nSign-up failed: {response.json()}")
    except Exception as e:
        logging.error(f"Error in sign_up: {str(e)}")


def log_in(baseurl):
    global current_token
    try:
        print("\nLogging in...")  # Cleaner message
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        payload = {
            "username": username,
            "password": password
        }

        url = f"{baseurl}/login"
        response = web_service_post(url, payload)
        if response and response.status_code == 200:
            data = response.json()
            current_token = data["token"]  # Save token in memory
            print("\nLog-in successful! Your session token has been stored.")

            # Save to user-specific config file
            config_file = f"blueseave-{username}-config.ini"
            config = ConfigParser()
            config["client"] = {
                "webservice": baseurl,
                "token": current_token
            }
            with open(config_file, "w") as configfile:
                config.write(configfile)
                print(f"Token saved to {config_file}")
        else:
            print(f"\nLog-in failed: {response.json()}")
    except Exception as e:
        logging.error(f"Error in log_in: {str(e)}")

def fetch_user_data(baseurl, token):
    try:
        print("\nFetching user data...")
        url = f"{baseurl}/fetch-user-data?token={token}"
        response = requests.get(url)  # Assuming web_service_get is similar to requests.get
        print("Response: ", response)

        if response is None:
            print("Error: Failed to fetch user data. Please check your internet connection or try again later.")
            return

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            # Parse the JSON response
            response_data = response.json()

            # Check if 'message' key exists indicating no data
            
            # Proceed with data processing
            data = response_data.get("body", "[]")
            data = json.loads(data) if isinstance(data, str) else data

            if 'message' in data and data['message'] == "No data available for this user.":
                print(data['message'])
                return

            print("Data: ", data)

            if not data:
                print("No data available for this user.")
                return

            print("\nUser Data:")
            for item in data:
                category = item.get("CategoryName", "Unknown")
                total_amount = item.get("TotalAmount", 0)
                budget = item.get("BudgetAmount", 0)
                print(f"- {category}: Spent {total_amount}, Budget {budget}")

            # Call visualization function if data is present
            visualize_and_save_user_data(data)
        else:
            print(f"Error: {response.status_code}")
            if response.headers.get("Content-Type") == "application/json":
                print(response.json())
    except json.JSONDecodeError:
        logging.error("Error decoding JSON response.")
    except requests.RequestException as e:
        logging.error(f"Request error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error in fetch_user_data: {str(e)}")


def fetch_alerts(baseurl, token):
    """
    Fetch budget alerts from the /retrieve-notifications endpoint.
    """
    try:
        print("\nLoading notifications...")  # Cleaner user experience
        url = f"{baseurl}/notifications?token={token}"  # Correct endpoint
        response = web_service_get(url)

        if response and response.status_code == 200:
            # Debugging print statement for full response (optional)
            logging.info(f"Full Response: {response.json()}")

            data = response.json().get("body", [])

            # Check if data is empty
            if not data:
                print("\nNo notifications available.")  # Message for no alerts
                return

            print("\nNotifications:")
            for item in data:
                # Extract and display message and timestamp
                message = item.get("Message", "No message provided.")
                created_at = item.get("CreatedAt", "Unknown timestamp")
                print(f"- {message} (Created at: {created_at})")
        else:
            print(f"Error: {response.status_code}, {response.json()}")
    except Exception as e:
        logging.error(f"Error in fetch_alerts: {str(e)}")

############################################################
# Main Function
############################################################

def main():
    global current_token
    current_token = None  # Token stored in memory during the session
    try:
        print("** Welcome to Budget Tracker Client **")
        config_file = 'blueseave-app-client-config.ini'

        # Load configuration
        if not pathlib.Path(config_file).is_file():
            print("No config file found. Please sign up or log in.")
            baseurl = input("Enter the base URL for your API: ").strip()
        else:
            configur = ConfigParser()
            configur.read(config_file)
            baseurl = configur.get('client', 'webservice')

        # Main loop
        while True:
            cmd = prompt()
            if cmd == "0":
                print("\nExiting Budget Tracker Client. Goodbye!")
                break
            elif cmd == "1":
                sign_up(baseurl)
            elif cmd == "2":
                log_in(baseurl)
            elif cmd == "3":
                if not current_token:
                    print("You must log in first!")
                else:
                    fetch_user_data(baseurl, current_token)
            elif cmd == "4":
                if not current_token:
                    print("You must log in first!")
                else:
                    fetch_alerts(baseurl, current_token)
            else:
                print("\n** Invalid command, please try again.")
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        sys.exit(0)
if __name__ == "__main__":
    main()
 
