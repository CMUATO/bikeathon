import venmo, json

def config_venmo():
    if not venmo.auth.configure():
        print("Venmo configuration failed.")
        return

    access_token = venmo.auth.get_access_token()

    config = open("config.json", "r").read()
    configDict = json.loads(config)
    configDict['venmo_token'] = access_token
    configjson = json.dumps(configDict)
    open("config.json", "w").write(configjson)

    return access_token

if __name__ == '__main__':
    print(config_venmo())
