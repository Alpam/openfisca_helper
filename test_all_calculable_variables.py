import requests
import json
import sys

def test_calculables_variables(url,year,month):
    rep_all_v = requests.get(url+'/variables')
    variables = rep_all_v.json()
    
    p_month = month
    p_year  = year
    p_eternity = "ETERNITY"

    json_err = {}
    
    nb_var = len(list(variables.keys()))
    print('have to test : '+str(nb_var)+' variables')
    i=1
    for variable in variables.keys():
        sys.stdout.write('                                                                                               \r')
        sys.stdout.flush()
        sys.stdout.write('  '+str(i)+'/'+str(nb_var)+' :: '+variable+'\r')
        sys.stdout.flush()

        i=i+1
        to_send={"foyers_fiscaux":{
                        "f_f1":{
                            "declarants":["Ricarda","Bill"],
                            "personnes_a_charge":["Janet"]
                        }
                    },
                    "familles":{
                        "f1":{
                            "parents":["Ricarda","Bill"],
                            "enfants":["Janet"]
                        }
                    },
                    "individus":{
                        "Ricarda":{},
                        "Bill": {},
                        "Janet": {}
                    },
                    "menages":{
                        "m1":{
                            "personne_de_reference": ["Ricarda","Bill"],
                            "enfants":["Janet"]
                        }
                    }
                }
        rep_var = requests.get(url+'/variable/'+variable)
        focus = rep_var.json()
        var_cal = {}
        try :
            focus['formulas']
            if focus['definitionPeriod']=='YEAR':
                var_cal[p_year]=None
            elif focus['definitionPeriod']=='MONTH':
                var_cal[p_month]=None
            elif focus['definitionPeriod']=='ETERNITY':
                var_cal[p_eternity]=None
            else:
                print('deinitionPeriod unknow, critical error')
                return
            if focus['entity']=='individu':
                for ind in to_send['individus'].keys():
                    to_send['individus'][ind][variable]=var_cal
            elif focus['entity']=='famille':
                to_send['familles']['f1'][variable]=var_cal
            elif focus['entity']=='foyer_fiscal':
                to_send['foyers_fiscaux']['f_f1'][variable]=var_cal
            elif focus['entity']=='menage':
                to_send['menages']['m1'][variable]=var_cal
            else:
                print('entity unknow, critical error')
                return
            rep_focus = requests.post(url+'/calculate',json=to_send)
            focus = rep_focus.json()
        except KeyError:
            continue
        try:
            focus['error'] 
        except KeyError:
            continue
        try:
            json_err[focus['error']].append(variable)
            continue
        except KeyError:
            json_err[focus['error']]=list()
            json_err[focus['error']].append(variable)
            continue
    f = open('rapport_err.log','w')
    f.write(json.dumps(json_err, indent=4))
    f.close()
    print(json.dumps(json_err, indent=4))
    return

if __name__ == '__main__':
    y="2018"
    m="2018-08"
    test_calculables_variables('http://localhost:6000',y,m)