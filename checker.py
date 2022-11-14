import json
import numpy as np


def check_stats(raw_team, artifact_stats, debug=False):
    metadata = json.loads(raw_team['metadata'])
    for char in metadata['char_details']:
        if any(x in list(char['sets'].keys()) for x in ['theexile', 'instructor']):
            continue
        current_result, msg = step_main(np.asarray(char['stats'], dtype=float), artifact_stats)
        if not current_result:
            print(f'{char["name"]} has invalid stats! {msg}')
            if debug:
                print(raw_team['simulation_key'])
                step_main(np.asarray(char['stats'], dtype=float), artifact_stats, debug=True)
            return False
    return True


def step_main(stat_array, artifact_stats, debug=False):

    if debug: print(stat_array)

    mains = np.asarray(list(artifact_stats['mains'].values()))
    subs = np.asarray(list(artifact_stats['subs'].values()))
    stat_names = list(artifact_stats['mains'].keys())
    universal_mains = ['hp%', 'atk%', 'def%', 'em']
    circlet_mains = ['cr', 'cd', 'heal']
    sands_mains = ['er']
    goblet_mains = ["pyro%", "hydro%", "cryo%", "electro%", "anemo%", "geo%", "phys%", "dendro%"]

    max_pot_subs = stat_array - mains
    stat_array -= (2 * subs)

    possible_mains = []

    for i in range(len(stat_array)):
        if debug and stat_names[i] == "dendro%":
            print(mains[i])
            print(max_pot_subs[i])
        if mains[i] > 0 and max_pot_subs[i] >= 0:
            possible_mains.append(stat_names[i])
            if stat_names[i] in universal_mains:
                if max_pot_subs[i] - (2 * mains[i]) >= 0:
                    possible_mains.append(stat_names[i])
                    possible_mains.append(stat_names[i])
                elif max_pot_subs[i] - mains[i] >= 0:
                    possible_mains.append(stat_names[i])

    if debug: print(possible_mains)

    if 'hp' in possible_mains: possible_mains.remove('hp')
    if 'atk' in possible_mains: possible_mains.remove('atk')

    possible_main_combs = []

    for circlet in circlet_mains + universal_mains:
        for sands in sands_mains + universal_mains:
            for goblet in goblet_mains + universal_mains:
                if circlet in possible_mains:
                    t1 = possible_mains.copy()
                    t1.remove(circlet)
                    if sands in t1:
                        t2 = t1.copy()
                        t2.remove(sands)
                        if goblet in t2:
                            comb = sorted([circlet, sands, goblet])
                            if comb not in possible_main_combs: possible_main_combs.append(comb)

    if debug: print(possible_main_combs)

    if len(possible_main_combs) == 0:
        return False, "No possible main stat combination."

    diagnostic_info = []

    for comb in possible_main_combs:
        if debug: print(comb)
        max_subs = 20
        current = stat_array.copy()
        if debug: print(current)
        for main in comb:
            stat_index = stat_names.index(main)
            if subs[stat_index] > 0:
                max_subs += 2
                current[stat_index] -= mains[stat_index]
                current[stat_index] += 2 * subs[stat_index]

        current[stat_names.index('hp')] -= mains[stat_names.index('hp')]
        current[stat_names.index('atk')] -= mains[stat_names.index('atk')]

        with np.errstate(divide='ignore'):
            with np.errstate(invalid='ignore'):
                current /= subs

        if debug: print(current)
        if debug: print(max_subs)
        for stat in current:
            if not np.isnan(stat) and not np.isinf(stat) and stat > 0:
                max_subs -= np.ceil(stat-0.01)
        if debug: print(max_subs)
        if max_subs >= 0:
            return True, None

        diagnostic_info.append({
            'main_stat_comb': comb,
            'required_substats': current,
            'substat_deficit': -1 * max_subs
        })

    diagnostic_info = sorted(diagnostic_info, key=lambda d: d['substat_deficit'])

    if diagnostic_info[0]['substat_deficit'] > 3:
        return False, f"Allocated too many substats ({int(diagnostic_info[0]['substat_deficit'])})."

    for i, stat in enumerate(diagnostic_info[0]['required_substats']):
        if stat > 0 and 0.01 < stat % np.floor(stat) < 0.9:
            return False, f"Allocated too many substats. ({int(diagnostic_info[0]['substat_deficit'])}). Maybe there is a typo at \"{stat_names[i]}\"?"
    return False, "Check Manually."


def check_weapons(raw_team):
    metadata = json.loads(raw_team['metadata'])
    for char in metadata['char_details']:
        if not char['weapon']['level'] == 90:
            print(f'{char["name"]} has an invalid weapon!')
            return False
    return True
