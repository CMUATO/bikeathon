import pygsheets, json

def init_gsheet():
    config = open("config.json").read()
    configDict = json.loads(config)
    gsheets_key = configDict["gsheets_key"]

    gc = pygsheets.authorize("gsheets_secret.json")
    sh = gc.open_by_key(gsheets_key)
    wks = sh.worksheet_by_title("Data")
    return wks

def fetch_gsheet_total(wks):
    df = wks.get_as_df().set_index("Method")
    cash_total = float(df.loc["Cash", "Total"])
    misc_total = float(df.loc["Misc", "Total"])
    return cash_total, misc_total

if __name__ == "__main__":
    wks = init_gsheet()
    print("Cash: %d, Misc: %d" % fetch_gsheet_total(wks))
