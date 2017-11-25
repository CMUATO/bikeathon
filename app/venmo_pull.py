import venmo, requests, logging


logger = logging.getLogger('venmo.payment')


def fetch_venmo_balance():
    access_token = venmo.auth.get_access_token()

    if not access_token:
        logger.warn('No access token. Configuring ...')
        if not venmo.auth.configure():
            return
        access_token = venmo.auth.get_access_token()

    data = {'access_token': access_token}
    response = requests.get('https://api.venmo.com/v1/me', json=data)

    return float(response.json()['data']['balance'])


if __name__ == '__main__':
    print("Venmo balance: $%s" % fetch_venmo_balance())
