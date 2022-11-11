import io
import json


def calc_general_value():

    print('Calculating general value...')

    character_data = open('genshin-data/characters.json')
    characters = json.load(character_data)

    team_data = open('teams.json')
    teams = json.load(team_data)

    settings_data = open('settings.json')
    settings = json.load(settings_data)

    result = []

    for c in characters:

        result.append({'name': c['name'], 'rating': 0})

        factor = 1
        for t in teams:
            if c['name'] in t['char_names']:
                result[len(result)-1]['rating'] += factor * t['dps']
                factor *= settings['diminishing_factor']

    result = sorted(result, key=lambda d: d['rating'], reverse=True)

    with io.open('general_result.txt', 'w', encoding='utf-8') as f:
        f.write(pretty_print_results(result))

    return result


def calc_adjusted_value():
    general_value = calc_general_value()
    print('Calculating adjusted value...')

    team_data = open('teams.json')
    teams = json.load(team_data)

    settings_data = open('settings.json')
    settings = json.load(settings_data)

    result = []

    for c in general_value:

        result.append({'name': c['name'], 'rating': 0})

        factor = 1
        for t in teams:
            if c['name'] in t['char_names']:
                total_score = 0
                contribution = 0
                for name in t['char_names']:
                    c_contribution = next((item for item in general_value if item['name'] == name), None)['rating']
                    total_score += c_contribution
                    if name == c['name']:
                        contribution += c_contribution
                result[len(result) - 1]['rating'] += factor * t['dps'] * (contribution/total_score)
                factor *= settings['diminishing_factor']

        result = sorted(result, key=lambda d: d['rating'], reverse=True)

    with io.open('adjusted_result.txt', 'w', encoding='utf-8') as f:
        f.write(pretty_print_results(result))

    return result


def pretty_print_results(value):
    result = ''
    for c in value:
        result += f'{c["name"]}: {round(1000 * (c["rating"] / value[0]["rating"]))}\n'
    return result
