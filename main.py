import io
import json
import numbers
import os
import importer
import rating
import checker


def main_menu():
    os.system('cls')

    print("**********************************************")
    print("***            Genshin Rankings            ***")
    print("**********************************************\n")

    print(f'[1] Calculate rankings\n')
    print(f'[2] Import/Update gcsim database\n')
    print(f'[3] Settings\n')
    print(f'[4] Export teams\n')
    print(f'[5] Filter Testing\n')
    print(f'[6] Exit\n')

    choice = input('')

    match choice:
        case '1':
            calc_menu()
        case '2':
            import_menu()
        case '3':
            settings_menu()
        case '4':
            export_menu()
        case '5':
            filter_menu()
        case '6':
            os.system('cls')
            quit()
        case '7':
            build_menu()
    main_menu()


def calc_menu():
    os.system('cls')
    print(f'\n[1] Calculate general score\n')
    print(f'[2] Calculate adjusted score\n')
    print(f'[3] Back\n')
    choice = input('')

    match choice:
        case '1':
            os.system('cls')
            rating.calc_general_value()
            input('Finished! Press enter to continue...')
            main_menu()
        case '2':
            os.system('cls')
            rating.calc_adjusted_value()
            input('Finished! Press enter to continue...')
            main_menu()
        case '3':
            os.system('cls')
            main_menu()


def import_menu():
    os.system('cls')

    choice = input('\nAre you sure? (existing data will be overwritten) [y/(n)] ')

    match choice:
        case 'y':
            settings_data = open('settings.json')
            settings = json.load(settings_data)

            importer.import_gcsim_char_list(settings['gcsim_api_url'])
            importer.import_total_team_data(settings['gcsim_api_url'])
            unique_teams = importer.get_full_sim_list()
            importer.export_teams(unique_teams)
            input('Finished! Press enter to continue...')

    main_menu()


def settings_menu():
    os.system('cls')

    settings_data = open('settings.json')
    settings = json.load(settings_data)

    changeable_settings = []

    i = 1

    for s in settings:
        if isinstance(settings[s], numbers.Number):
            changeable_settings.append(s)
            print(f'\n[{i}] {s}: {settings[s]}')
            i += 1

    choice = input('\nSelect setting to change: ')

    if choice.isdigit() and 0 < int(choice) <= len(changeable_settings):
        new_val = input('\nEnter new value: ')
        settings[changeable_settings[int(choice)-1]] = float(new_val)
        with io.open('settings.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(settings, ensure_ascii=False, indent=4))
        input('\nSetting changed successfully! Press enter to continue...')
    else:
        input('\nInvalid input! Press enter to continue...')

    main_menu()


def export_menu():
    os.system('cls')

    choice = input('\nAre you sure? (existing data will be overwritten) [y/(n)] ')
    match choice:
        case 'y':
            importer.export_characters()
            input('Finished! Press enter to continue...')

    main_menu()


def filter_menu():
    os.system('cls')

    artifact_stats_data = open('genshin-data/artifact_stats.json')
    artifact_stats = json.load(artifact_stats_data)

    unique_teams_data = open('gcsim-data/unique_teams.json')
    unique_teams = json.load(unique_teams_data)

    print(f'Total amount of teams: {len(unique_teams)}\n')
    valid_teams = 0

    for team in unique_teams:
        if checker.check_stats(team, artifact_stats) and checker.check_weapons(team):
            valid_teams += 1
        else:
            print(f'{team["simulation_key"]}\n')

    print(f'Amount of valid teams: {valid_teams}\n')
    input('Finished! Press enter to continue...')


def build_menu():
    os.system('cls')
    choice = input('Are you sure? (YOU ARE PROBABLY NOT SUPPOSED TO BE HERE, WILL OVERWRITE IMPORTANT FILES) [y/(n)] ')
    match choice:
        case 'y':
            unique_teams = importer.get_full_sim_list()
            importer.build_data(unique_teams)
    main_menu()


if __name__ == '__main__':
    if not os.path.exists('settings.json'):
        init_settings = {
            'gcsim_api_url': 'https://gcsim.app/api/db/',
            'diminishing_factor': 2/3
        }
        with io.open('settings.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(init_settings, ensure_ascii=False, indent=4))
    main_menu()
