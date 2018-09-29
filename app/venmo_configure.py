import venmo, json

def config_venmo():
    if not venmo.auth.configure():
        print("Venmo configuration failed.")
        return

    access_token = venmo.auth.get_access_token()

    with open("config.json", "r") as file:
        config = file.read()
        configDict = json.loads(config)
        configDict['venmo_token'] = access_token
        configjson = json.dumps(configDict, indent=4, sort_keys=True)

    with open("config.json", "w") as file:
        file.write(configjson)

    return access_token

if __name__ == '__main__':
    print(config_venmo())
