import venmo, requests, json

def fetch_venmo_balance():
    with open("config.json", "r") as file:
        config = file.read()

    configDict = json.loads(config)
    access_token = configDict["venmo_token"]

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
