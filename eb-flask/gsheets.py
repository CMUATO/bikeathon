import pygsheets


def init_gsheet():
    gc = pygsheets.authorize('gsheets_secret.json', no_cache=True)
    sh = gc.open_by_key('11xzeI8xs3hntJv-oB6hQ2T4LIrl5zK8VcDza-SiFNgU')
    wks = sh.worksheet_by_title('Data')
    return wks


def fetch_gsheet_total(wks):
    df = wks.get_as_df().set_index('Method')
    cash_total = float(df.at['Cash', 'Total'])
    misc_total = float(df.at['Misc', 'Total'])
    return cash_total, misc_total


if __name__ == "__main__":
    wks = init_gsheet()
    print("Cash: %d, Misc: %d" % fetch_gsheet_total(wks))
