import yaml
import os
import copy
import time
import json

defaultSettings = {}
with open("network.bck.yaml", 'r') as file:
    defaultSettings = yaml.safe_load(file)

def create_conf_file(network_config):
    with open('network.yaml', 'w') as file:
        yaml.dump(network_config, file)


def write_results(results, name):
    with open(f'{name}.json', 'w') as file:
        json.dump(results, file)

def create_conf_settings(
        alice_settings=None,
        bob_settings=None,
        link_settings=None
):
    conf = copy.deepcopy(defaultSettings)
    if alice_settings is not None:
        conf['nodes'][1]['gate_fidelity'] = alice_settings['fidelity']
    if bob_settings is not None:
        conf['nodes'][0]['gate_fidelity'] = bob_settings['fidelity']
    if link_settings is not None:
        conf['links'][0]['fidelity'] = link_settings['fidelity']
    return conf


## Do smt
def map_results(string_array):
    success = None
    fidelity = None
    fidelityI = None
    fidelity2 = None
    fidelityZ = None
    fidelity2Z = None
    or_fidelity1 = None
    or_fidelity2 = None
    for s in string_array:
        split_s = s.split(':')
        if split_s[0] == 'Success':
            success = split_s[1]
        elif split_s[0] == 'Fidelity':
            fidelity = split_s[1]
        elif split_s[0] == 'FidelityI':
            fidelityI = split_s[1]
        elif split_s[0] == 'Fidelity2':
            fidelity2 = split_s[1]
        elif split_s[0] == 'FidelityZ':
            fidelityZ = split_s[1]
        elif split_s[0] == 'Fidelity2Z':
            fidelity2Z = split_s[1]
        elif split_s[0] == 'OriginalFidelity1':
            or_fidelity1 = split_s[1]
        elif split_s[0] == 'OriginalFidelity2':
            or_fidelity2 = split_s[1]

    return (success, fidelity, fidelityI, fidelity2, fidelityZ, fidelity2Z, or_fidelity1, or_fidelity2)


def run_simulation(conf):
    create_conf_file(conf)
    result = os.popen("netqasm simulate --formalism=dm").read()
    print(result)
    f_results = [s for s in result.split('\n') if s]
    return map_results(f_results)

results = []
#Link tests
if False:
    for i in range(6):

        fidelity = 1 - (i/10)
        print(f"Starting with fidelity {fidelity}")
        conf = create_conf_settings(link_settings={'fidelity': fidelity})
        success_f = []
        failed_f = []
        for j in range(100):
            success, fidelity, fidelityI, fidelity2, fidelityZ, fidelity2Z = run_simulation(conf)
            if success == 'True':
                success_f.append({
                    "fidelity": float(fidelity),
                    "fidelityI": float(fidelityI),
                    "fidelity2": float(fidelity2),
                    "fidelityZ": float(fidelityZ),
                    "fidelity2Z": float(fidelity2Z)
                })
            else:
                failed_f.append({
                    "fidelity": float(fidelity),
                    "fidelityI": float(fidelityI),
                    "fidelity2": float(fidelity2),
                    "fidelityZ": float(fidelityZ),
                    "fidelity2Z": float(fidelity2Z)
                })
            time.sleep(1)
        results.append({
            'conf': conf,
            'success_f': success_f,
            'failed_f': failed_f,
        })

    write_results(results, 'link_only3')

if False:
    for i in range(6):
        fidelity = 1 - (i/10)
        print(f"Starting with fidelity {fidelity}")
        conf = create_conf_settings(alice_settings={'fidelity': fidelity})
        success_f = []
        failed_f = []
        for j in range(100):
            success, fidelity, fidelityI, fidelity2, fidelityZ, fidelity2Z = run_simulation(conf)
            if success == 'True':
                success_f.append({
                    "fidelity": float(fidelity),
                    "fidelityI": float(fidelityI),
                    "fidelity2": float(fidelity2),
                    "fidelityZ": float(fidelityZ),
                    "fidelity2Z": float(fidelity2Z)
                })
            else:
                failed_f.append({
                    "fidelity": float(fidelity),
                    "fidelityI": float(fidelityI),
                    "fidelity2": float(fidelity2),
                    "fidelityZ": float(fidelityZ),
                    "fidelity2Z": float(fidelity2Z)
                })
            time.sleep(1)
        results.append({
            'conf': conf,
            'success_f': success_f,
            'failed_f': failed_f,
        })

    write_results(results, 'alice_only4')

if False:
    for i in range(6):
        fidelity = 1 - (i/10)
        print(f"Starting with fidelity {fidelity}")
        conf = create_conf_settings(bob_settings={'fidelity': fidelity})
        success_f = []
        failed_f = []
        for j in range(100):
            success, fidelity, fidelityI, fidelity2, fidelityZ, fidelity2Z = run_simulation(conf)
            if success == 'True':
                success_f.append({
                    "fidelity": float(fidelity),
                    "fidelityI": float(fidelityI),
                    "fidelity2": float(fidelity2),
                    "fidelityZ": float(fidelityZ),
                    "fidelity2Z": float(fidelity2Z)
                })
            else:
                failed_f.append({
                    "fidelity": float(fidelity),
                    "fidelityI": float(fidelityI),
                    "fidelity2": float(fidelity2),
                    "fidelityZ": float(fidelityZ),
                    "fidelity2Z": float(fidelity2Z)
                })
                time.sleep(1)
        results.append({
            'conf': conf,
            'success_f': success_f,
            'failed_f': failed_f,
        })

    write_results(results, 'bob_only4')

if True:
    for i in range(10):
        for h in range(6):
            fidelity1 = 1 - (i/100)
            fidelity3 = 1 - (h/10)
            print(f"Starting with fidelity {fidelity1} {fidelity3}")
            conf = create_conf_settings(
                alice_settings={'fidelity': fidelity1},
                bob_settings={'fidelity': fidelity1},
                link_settings={'fidelity': fidelity3}
            )
            success_f = []
            failed_f = []
            for j in range(100):
                success, fidelity, fidelityI, fidelity2, fidelityZ, fidelity2Z, or_fidelity1, or_fidelity2 = run_simulation(conf)
                if success == 'True':
                    success_f.append({
                        "fidelity": float(fidelity),
                        "fidelityI": float(fidelityI),
                        "fidelity2": float(fidelity2),
                        "fidelityZ": float(fidelityZ),
                        "fidelity2Z": float(fidelity2Z),
                        "or_fidelity1": float(or_fidelity1),
                        "or_fidelity2": float(or_fidelity2)
                    })
                else:
                    failed_f.append({
                        "fidelity": float(fidelity),
                        "fidelityI": float(fidelityI),
                        "fidelity2": float(fidelity2),
                        "fidelityZ": float(fidelityZ),
                        "fidelity2Z": float(fidelity2Z),
                        "or_fidelity1": float(or_fidelity1),
                        "or_fidelity2": float(or_fidelity2)
                    })
                time.sleep(1)
            results.append({
                'conf': conf,
                'success_f': success_f,
                'failed_f': failed_f,
            })

    write_results(results, 'total_combined_fidelityf')