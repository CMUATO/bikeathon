import venmo, requests, json
from app_manager import app

def fetch_venmo_balance():
    access_token = app.config["VENMO_TOKEN"]

    data = {"access_token": access_token}
    response = requests.get("https://venmo.com/api/v5/me", params=data)

    try:
        return float(response.json()["balance"])
    except KeyError:
        print("Access token has expired. Please reauthorize by running "
              "venmo_configure.py. Returning None.")
        return None

if __name__ == "__main__":
    print("Venmo balance: $%s" % fetch_venmo_balance())
