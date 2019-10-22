import configparser
import json
import database as db
import os



config = configparser.ConfigParser()
config.read('config.ini')

plugins_name ={'Androbugs'}

plugins_name_sorted={'DroidStatX'}

jsonResultsLocation = config['SCANNER']['jsonResultsLocation']

resultsFeedback = './json_results/Final_Output/feedback/'

resultsFeedbackLevels = './json_results/Final_Output/feedback_levels/'

resultsFeedbackVulnerabilityLevels = './json_results/Final_Output/feedback_vulnerability_levels/'

dictionaryAndrobugs = './dictionaries/androbugs_dict.json'


def startEngine(md5):
    feedback(md5)
    feedback_levels(md5)
    feedback_vulnerability_levels(md5)

def feedback(md5):
    data={}
    owasp_category = ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10']
    for o in owasp_category:
       data[o]= []
    for name in plugins_name:
        with open(jsonResultsLocation + '/' + name + '/' + md5 + '.json') as plugin_output:
            read_data = json.load(plugin_output)
        with open(dictionaryAndrobugs, 'r') as d:
            dict = json.load(d)
        for x in read_data['results']:
             for z in owasp_category:
                 for y in dict['results']:

                    if y['category'] == z:

                        if y['name'] == x['vulnerability']:
                            #category = y['category']
                            data[z].append({
                                'vulnerability': x['vulnerability'],
                                'details': x['details'],
                                'severity': x['severity'],
                                'detectedby': 'Androbugs',
                                'feedback': [{ "url": "Nothing to show"},
                                     {"video": "Nothing to show"},
                                     {"book": "Nothing to show"},
                                     {"other": "Nothing to show"}]
                            })
                            break;
    for name in plugins_name_sorted:
        with open(jsonResultsLocation + '/' + name + '/' + md5 + '.json') as plugin_output:
            read_data = json.load(plugin_output)
        for category in owasp_category:
            for x in read_data[category]:
                data[category].append({
                                    'vulnerability': x['vulnerability'],
                                    'details': x['details'],
                                    'severity': x['severity'],
                                    'detectedby': 'DroidStatX',
                                    'feedback': [{ "url": x['link']},
                                         {"video": "Nothing to show"},
                                         {"book": "Nothing to show"},
                                         {"other": "Nothing to show"}]
                                })
    if not os.path.exists(resultsFeedback):
            os.system("mkdir " + resultsFeedback)
    with open('./json_results/Final_Output/feedback/'+md5+'.json', 'w') as f:
        json.dump(data, f)
    db.insert_final_results(md5, './json_results/Final_Output/feedback/' + md5 + ".json", 0, "NOT YET IN THE FINAL FORMAT")


def feedback_levels(md5):
    with open(resultsFeedback + md5 + ".json", "r") as json_file:
        read_content = json.load(json_file)
    data_apk_levels = {}
    data_apk_levels['levelsForApk'] = []

    info = 0
    notice = 0
    warning = 0
    critical = 0

    category = ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10']
    for c in category:
        for x in read_content[c]:
            if 'Info' in x['severity']:
                info += 1
            if 'Notice' in x['severity']:
                notice += 1
            if 'Warning' in x['severity']:
                warning += 1
            if 'Critical' in x['severity']:
                critical += 1

    data_apk_levels['levelsForApk']=({
        'Info':info,
        'Notice': notice,
        'Warning': warning,
        'Critical': critical
    })
    if not os.path.exists(resultsFeedbackLevels):
            os.system("mkdir " + resultsFeedbackLevels)
    with open(resultsFeedbackLevels + md5 + ".json", "a") as save_file:
        json.dump(data_apk_levels, save_file)
    db.insert_results_levels(md5, resultsFeedbackLevels + md5 + ".json", 0, "NOT YET IN THE FINAL FORMAT")

def feedback_vulnerability_levels(md5):
    with open(resultsFeedback + md5 + ".json", "r") as json_file:
        read_content = json.load(json_file)
    data_vuln_level ={}
    data_vuln_level['vulnerabilities'] = []

    category = ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10']

    for c in category:
        for x in read_content[c]:
            data_vuln_level['vulnerabilities'].append({
                'vulnerability': x['vulnerability'],
                'severity': x['severity'],
            })

    if not os.path.exists(resultsFeedbackVulnerabilityLevels):
            os.system("mkdir " + resultsFeedbackVulnerabilityLevels)
    with open(resultsFeedbackVulnerabilityLevels + md5 + ".json", "a") as save_file:
        json.dump(data_vuln_level, save_file)
    db.insert_results_vulnerabilitylevel(md5, resultsFeedbackVulnerabilityLevels + md5 + ".json", 0, "NOT YET IN THE FINAL FORMAT")