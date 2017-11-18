import pygsheets


def fetch_as_df():
    gc = pygsheets.authorize('gsheets_secret.json', no_cache=True)
    sh = gc.open_by_key('1tTuWHk3c-JVvdOOSVVA1rIOjjz8eMf-Zyh1Fit5JwPc')
    wks = sh.worksheet_by_title('Data')
    df = wks.get_as_df().set_index('Method')
    return df


def fetch_gsheet_total():
    df = fetch_as_df()
    venmo_total = df.at['Venmo', 'Total']
    cash_total = df.at['Cash', 'Total']
    card_total = df.at['Card', 'Total']
    # Expecting Stripe API to calculate card total itself
    # Only report venmo and cash
    # Probably will end up deleting the card option on the Google form
    # Unless we implement donating towards certain brothers
    return venmo_total + cash_total


if __name__ == "__main__":
    print("Total money from Google Sheet: %d" % fetch_gsheet_total())
