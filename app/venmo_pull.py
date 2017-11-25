import venmo, requests


def fetch_venmo_balance():
    access_token = venmo.auth.get_access_token()

    if not access_token:
        print('No access token. Configuring ...')
        if not venmo.auth.configure():
            return
        access_token = venmo.auth.get_access_token()

    data = {'access_token': access_token}
    response = requests.get('https://api.venmo.com/v1/me', json=data)

    try:
        return float(response.json()['data']['balance'])
    except KeyError:
        print("Access token has expired. Please reauthorize with command "
              "'venmo configure'. Returning None.")
        return None


if __name__ == '__main__':
    print("Venmo balance: $%s" % fetch_venmo_balance())
