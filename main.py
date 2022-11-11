import os
import importer
import rating

gcsim_url = 'https://gcsim.app/api/db/'


def main_menu():
    os.system('cls')

    print("**********************************************")
    print("***            Genshin Rankings            ***")
    print("**********************************************\n")

    print(f'[1] Calculate rankings\n')
    print(f'[2] Import gcsim database\n')
    print(f'[3] Settings\n')
    print(f'[4] Exit\n')

    choice = input('')

    match choice:
        case '1':
            calc_menu()
        case '2':
            import_menu()
        case '3':
            settings_menu()
        case '4':
            os.system('cls')
            return
        case '5':
            build_menu()


def calc_menu():
    os.system('cls')
    print(f'[1] Calculate general score\n')
    print(f'[2] Calculate adjusted score\n')
    print(f'[3] Back\n')
    choice = input('')

    match choice:
        case '1':
            os.system('cls')
            rating.calc_general_value()
            input('Finished! Press enter to continue')
            main_menu()
        case '2':
            os.system('cls')
            rating.calc_adjusted_value()
            input('Finished! Press enter to continue')
            main_menu()
        case '3':
            os.system('cls')
            main_menu()


def import_menu():
    os.system('cls')

    choice = input('Are you sure? (existing data will be overwritten) [y/(n)] ')

    match choice:
        case 'y':
            importer.import_gcsim_char_list(gcsim_url)
            importer.import_total_team_data(gcsim_url)
            unique_teams = importer.get_full_sim_list()
            importer.export_teams(unique_teams)
            input('Finished! Press enter to continue')

    main_menu()


def settings_menu():
    os.system('cls')
    input('')
    main_menu()


def build_menu():
    os.system('cls')
    choice = input('Are you sure? (existing data will be overwritten) [y/(n)] ')
    match choice:
        case 'y':
            unique_teams = importer.get_full_sim_list()
            importer.build_data(unique_teams)
    main_menu()


if __name__ == '__main__':
    main_menu()
