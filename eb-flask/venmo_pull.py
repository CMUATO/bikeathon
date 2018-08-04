import venmo, requests, json

def fetch_venmo_balance():
    config = open("config.json").read()
    configDict = json.loads(config)
    access_token = configDict['venmo_token']

    data = {'access_token': access_token}
    response = requests.get('https://api.venmo.com/v1/me', json=data)

    try:
        return float(response.json()['data']['balance'])
    except KeyError:
        print("Access token has expired. Please reauthorize by running "
              "venmo_configure.py. Returning None.")
        return None

if __name__ == '__main__':
    print("Venmo balance: $%s" % fetch_venmo_balance())
