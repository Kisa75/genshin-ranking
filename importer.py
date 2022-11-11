import io
import json
import os
import urllib.request
from urllib.request import Request


def import_gcsim_char_list(gcsim_url):
    print('Importing gcsim character list...')

    if not os.path.exists('gcsim-data'):
        os.mkdir('gcsim-data')

    req = Request(url=gcsim_url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req).read()
    gcsim_char_list = json.loads(data)

    with io.open('gcsim-data/char_list.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(gcsim_char_list, ensure_ascii=False))

    print('Finished gcsim character list!')


def import_total_team_data(gcsim_url):
    data = open('gcsim-data/char_list.json')
    gcsim_char_list = json.load(data)
    for e in gcsim_char_list:
        import_team_data(gcsim_url, e['avatar_name'])


def import_team_data(gcsim_url, avatar_name):
    print(f'Importing {avatar_name}')

    req = Request(url=f'{gcsim_url}/{avatar_name}', headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req).read()
    current_list = json.loads(data)

    with io.open(f'gcsim-data/{avatar_name}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(current_list, ensure_ascii=False))


def get_full_sim_list():
    print('Removing duplicates...')

    result = []
    keys = []

    data = io.open('gcsim-data/char_list.json')
    gcsim_char_list = json.load(data)
    for e in gcsim_char_list:
        current_data = io.open(f'gcsim-data/{e["avatar_name"]}.json', errors="ignore")
        current_list = json.load(current_data)

        for team in current_list:
            if team['simulation_key'] not in keys:
                result.append(team)
                keys.append(team['simulation_key'])

    return result


def export_teams(unique_teams):
    print(f'Filtering {len(unique_teams)} teams...')

    unique_teams = check_for_standard(unique_teams)

    teams = []

    for sim in unique_teams:
        metadata = json.loads(sim['metadata'])

        team = {
            'char_names': sorted(metadata['char_names']),
            'dps': metadata['dps']['mean']
        }
        teams.append(team)

    teams = sorted(teams, key=lambda d: d['dps'], reverse=True)

    result = []

    for t in teams:
        flag = True
        for r in result:
            if t['char_names'] == r['char_names']:
                flag = False
        if flag:
            result.append(t)

    print(f'Exporting {len(result)} teams to teams.json...')

    with io.open('teams.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


def check_for_standard(unique_teams):
    result = []

    a_cons = {4: 6, 5: 0}
    a_refs = {4: 5, 5: 1}

    character_data = open('genshin-data/characters.json')
    characters = json.load(character_data)

    weapon_data = open('genshin-data/weapons.json')
    weapons = json.load(weapon_data)

    for sim in unique_teams:
        metadata = json.loads(sim['metadata'])
        flag = True

        # Check for amount of targets
        if metadata['num_targets'] == 1:
            for c in metadata['char_details']:
                # Check for existence of Characters and Weapons in genshin-data
                g_c = next((item for item in characters if item['name'] == c['name']), None)
                g_w = next((item for item in weapons if item['name'] == c['weapon']['name']), None)
                if g_c is None or g_w is None or c['cons'] > a_cons[g_c['rarity']] or c['weapon']['refine'] > a_refs[g_w['rarity']]:
                    flag = False
        else:
            flag = False
        if flag:
            result.append(sim)
    return result


def build_data(unique_teams):
    characters = []
    weapons = []

    for sim in unique_teams:
        metadata = json.loads(sim['metadata'])
        for c in metadata['char_details']:
            if c['name'] not in characters:
                characters.append(c['name'])
            if c['weapon']['name'] not in weapons:
                weapons.append(c['weapon']['name'])

    c_dicts = []
    w_dicts = []

    for char in characters:
        c_dicts.append({'name': char, 'rarity': 4})
    for weapon in weapons:
        w_dicts.append({'name': weapon, 'rarity': 4})

    with io.open('genshin-data/characters.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(c_dicts, ensure_ascii=False))
    with io.open('genshin-data/weapons.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(w_dicts, ensure_ascii=False))
