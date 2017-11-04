import pygsheets


def main():
    gc = pygsheets.authorize('keys/client_secret.json', no_cache=True)

    sh = gc.open_by_key('1VdSFlW9t2RS47tlfCfXQkzspByOuMVI3kFnx49XZlrU')

    wks = sh.worksheet_by_title('Data')

    df = wks.get_as_df()

    print(df)


if __name__ == "__main__":
    main()
