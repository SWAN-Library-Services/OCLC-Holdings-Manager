import cli_ui
import glob
from ohm_settings import OhmSettings
from ohm_database import OhmDatabase
from ohm_marc import OhmMarc
from ohm_oclc import OhmOclc



cli_ui.info_1("Welcome to OCLC Holdings Manager")

# Read in the settings
settings_files = glob.glob('settings*.json')
settings_file = cli_ui.ask_choice("Which settings file should I use?", choices=settings_files, sort=True)
settings = OhmSettings(settings_file)

# load sqlite3 database
database = OhmDatabase(settings.database)

# get list of tables
tables = database.list_tables()

menu_items = ("Parse MARC extract", "Compare changes", "Send to OCLC", "Test OCLC WSKey", "Exit")

while True:
    menu_choice = cli_ui.ask_choice("OHM Main Menu", choices=menu_items, sort=False)

    if menu_choice == "Parse MARC extract":
        extracts_files = glob.glob(f'extracts/{settings.extract_naming_scheme}')
        extracts_files.sort()

        extract_file = cli_ui.ask_choice("Which extract file should I use?", choices=extracts_files)
        print(f'Using {extract_file}')

        table_name = cli_ui.ask_string("What should I name the table?", extract_file)

        parse_marc = OhmMarc(database, settings, extract_file, table_name)
        parse_marc.parse_marc_file()

    elif menu_choice == "Compare changes":
        current_data = cli_ui.ask_choice("Which is the latest data?", choices=tables, sort=False)
        tables.remove(current_data)
        previous_data = cli_ui.ask_choice("Which is the last run's data?", choices=tables, sort=False)

        print(f'Comparing {current_data} to {previous_data}')

        adds = database.compare_tables(current_data, previous_data)
        deletes = database.compare_tables(previous_data, current_data)

        print(f'{len(adds)} Adds, {len(deletes)} Deletes')

    elif menu_choice == "Send to OCLC":
        print("Placeholder for full OCLC functionality")

    elif menu_choice == "Test OCLC WSKey":
        oclc_conn = OhmOclc(settings.oclc_credentials)
        failed_symbols = oclc_conn.test_wskey(settings.holding_map)

        if len(failed_symbols) > 0:
            print("The following symbols are misconfigured for this WSKey:")
            for symbol in failed_symbols:
                print(f'{symbol}: {failed_symbols[symbol]}')
        else:
            print("OCLC WSKey configured properly for all symbols.")

    elif menu_choice == "Exit":
        break
    