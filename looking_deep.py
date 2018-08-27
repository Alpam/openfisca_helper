import requests
import json
import sys
import re

def find_first(json,pattern,i):
    p1=pattern.search(json)
    if p1 == None:
        return i
    p2=p1.span()
    if i[0] == None or p2[0]<i[0] :
        return p2[0],p2[1]-p2[0]
    else:
        return i

def formulas_reader(json):
    finds=[]
    patterns = [
        re.compile(r"famille(\.[a-zA-Z]+)?\('"),
        re.compile(r"foyer_fiscal(\.[a-zA-Z]+)?\('"),
        re.compile(r"individu(\.[a-zA-Z]+)?\('"),
        re.compile(r"menage(\.[a-zA-Z]+)?\('")]
    while(True):
        k=[None,0]
        for pat in patterns:
            k=list(find_first(json,pat,k))
        i=k[0]
        length=k[1]
        if i == None :
            return finds
        else:
            json=json[i+length:]
            j=0
            find=""
            try:
                while(json[j]!="'"):
                    find+=json[j]
                    j+=1
            except IndexError:
                return []
            finds.append(find)

def search_for_dependencies(variable,know,flg_calculable):
    dependencies=[]
    var_dscrpt = requests.get('http://localhost:6000/variable/'+variable)
    var_json   = var_dscrpt.json()
    found_dep  = formulas_reader(str(var_json['formulas']))
    for kn in know:
        if kn in found_dep:
            found_dep.remove(kn)
    know+=found_dep
    for vard in found_dep:
        vard_dscrpt = requests.get('http://localhost:6000/variable/'+vard)
        vard_json = vard_dscrpt.json()
        try :
            vard_json['formulas']
            if flg_calculable:
                dependencies.append(vard)
            dependencies+=search_for_dependencies(vard,know,flg_calculable)
        except KeyError:
            dependencies.append(vard)
    return dependencies

if __name__ == '__main__':
    mots = ['acs_montant',
        'ada',
        'aeeh',
        'aefa',
        'af',
        'aide_logement',
        'alf',
        'als',
        'ape',
        'cmu_c',
        'api',
        'apje',
        'ars',
        'asf',
        'asi',
        'aspa',
        'ass',
        'bourse_college',
        'bourse_lycee',
        'cf',
        'crds_pfam',
        'paje',
        'ppa',
        'prestations_familiales',
        'prestations_sociales',
        'psa',
        'rmi',
        'rsa',
        'aah',
        'allocations_temporaires_invalidite',
        'caah',
        'chomage_net',
        'gipa',
        'indemnite_fin_contrat',
        'indemnite_residence',
        'indemnites_journalieres',
        'jeunes_ind',
        'pensions',
        'primes_fonction_publique',
        'remboursement_transport',
        'ppe']
    flg_calculable=False
    all_var=[]
    var_by_var={}
    for mot in mots:
        print("start with "+ mot)
        o=search_for_dependencies(mot,[],flg_calculable)
        for variable in o:
            var_dscrpt = requests.get('http://localhost:6000/variable/'+variable)
            try:
                var_dscrpt.json()['formulas']
                print(mot+': fail')
                break
            except KeyError:
                continue
        print(mot +': good')
        all_var = all_var + o
        o.sort()
        var_by_var[mot]=o
    
    all_var = list(set(all_var))
    all_var.sort()
    f = open('var_by_var.log','w')
    f.write(json.dumps(var_by_var, indent=4))
    f.close()
    string=""
    for av in all_var:
        string += (av +" , ")
    f = open('all_var.log','w')
    f.write(string)
    f.close()
"""Bonjour,

@benjello Je vous remercie, j'avoue que je n'avais pas vraiment de questions et que c'était plus à titre d'information que je partageais ce rapport d'erreurs.

@guillett j'ai finis de mettre en place mon mappage + l'écriture d'un petit scripte qui permet de connaitre l'intégralité des variables non calculables nécessaires au calcule d'une variable calculable. Pour faire plus simple je vous transmet un dépôt avec mes scriptes.
"""