#!/bin/python3
# -*- coding: utf-8 -*-

import yaml
import json
import sys
import os
import pathlib
from jinja2 import Environment, FileSystemLoader
from pprint import pprint


def ensure_folder(folderTest):
    """[Check if folder exist and create it]

    Args:
        folderTest (string): [folder to test existance]
    """    
    file = pathlib.Path(folderTest)
    if not file.exists ():
        print ("File "+ folderTest +" not exist, creating it")
        pathlib.Path(folderTest).mkdir(parents=True, exist_ok=True) 

def main_menu(menuItem):
    """Main menu

    Args:
        menuItem ([list]): [Switch available in your json file]

    Returns:
        Just display list of switch
    """    
    os.system('clear')
    while True:
        try :
            print('List of switch configuration available in your json file :')
            for menuValue in menuItem:
                print(str(menuItem.index(menuValue)) + " - " + menuValue)
            print(" Ctrl + D to quit")
            choice = int(input("  >>  "))
            return menuItem[int(choice)]
        except ValueError:
                print("Value is not a number")
        except IndexError:
                print("Value not available")

# Variables statiques



jinja_dir = 'jinja_templates'
vlan_json_file = 'json/vlan.json'
switch_description_json_file = 'json/switch_port_config.json'
switch_model_definition_file = 'json/switch_model.json'

#script path
script_dir = os.path.dirname(os.path.realpath(__file__))
#jinja template dir
jinja_template_dir = os.path.join(script_dir,jinja_dir)

# vlan json
# todo : make this variable may be?
vlanfile = os.path.join(script_dir,vlan_json_file)
#vlanfile = os.path.join(script_dir,'json/huawei.vlan.json')

# switch configuration json file
# todo : make this variable may be?
switchjsonfile = os.path.join(script_dir,switch_description_json_file)
#switchjsonfile = os.path.join(script_dir,'json/huawei.interfaces.json')

# switch model json file
# todo : make this variable may be?
switchmodeljsonfile = os.path.join(script_dir,switch_model_definition_file)


#create Jinja2 environment object and refer to templates directory
env = Environment(loader=FileSystemLoader(jinja_template_dir))

#portDict dictionaire qui contient le nommages des ports du switchs en fonction du modèle
portDict = {}
switchNameList = []

##changement des fichiers json

#fichier de la config des vlan
vlanconfig = json.loads(open(vlanfile).read())

#fichier db des switchs
switchmodeldb = json.loads(open(switchmodeljsonfile).read())

#fichier de la config des switch
configjson = json.loads(open(switchjsonfile).read())

#fin changement des fichiers json

#creation du menu deroulant pour la liste des switchs
for switch in configjson:
    switchNameList.append(switch)

switchname = main_menu(sorted(switchNameList))

#check du folder puis creation du fichier de conf de sortie
ensure_folder(script_dir + "/output/")
configOutPutFile = script_dir + "/output/" + switchname + ".ios"

##initialisation des variables pour cree le fichier de config

#template pour crée le fichier de conf
template_file = configjson[switchname]['template']
template = env.get_template(template_file)

#hostname du switch
hostname = configjson[switchname]['hostname']

#domaine vlan utiliser par le switch
vlan_domain = configjson[switchname]['vlan_domain']

#vlans du domaine
vlans = vlanconfig[vlan_domain]['vlans']

#mgnt = configjson[switchname]["interfacemgnt"]
#dictionnaire des vlans
vlandict = { vlan["name"]: vlan["id"] for vlan in vlans}

#création du dictionnaire de description des ports qui compose le switchs
modulePortconfig = switchmodeldb.get(configjson[switchname]['model']).get('access_port')
for modPort in modulePortconfig.keys():
    portStart = modulePortconfig[modPort]['start']
    portEnd = modulePortconfig[modPort]['end']
    portName = modulePortconfig[modPort]['name']
    for portID in range(portStart, portEnd +1):
        portDict[str(portID)] = portName + str(portID)

#config du port de management
if switchmodeldb.get(configjson[switchname]['model']).get('management_port').get('embedded'):
    mgntFlag = True
    mgntPort = switchmodeldb.get(configjson[switchname]['model']).get('management_port').get('name')
else:
    mgntFlag = False
    mgntPort = 'None'

# on crée la variable emptyPortDict qui va contenir les ports non configurés sur le switch pour les passer a shutdown
emptyPortDict = { emptyPort['port']: "null" for emptyPort in configjson[switchname].get('interfacephy') }
emptyPortDict = portDict.keys() - emptyPortDict.keys()
#hack sordide pour que les ports soit dans le bon ordre 10 avant 1, on les converti en int pour les envoyer a jinja2, pour etre dans le bon
# ordre, puis dans le template jinja2 cast en string
emptyPortDict = {int(x) for x in emptyPortDict}
emptyPortDict = sorted(emptyPortDict)
#emptyPortDict = {}

#uncomment next line for debug
#pprint(ma_var)
#sys.exit()

#on crée un json qui décrit les variables envoyés à Jinja

switchConfigTemplateVariable =   {"vlans": vlans,
                                "hostname": hostname,
                                "configjson": configjson[switchname],
                                "vlandict": vlandict,
                                "portdict": portDict,
                                "emptyportdict": emptyPortDict,
                                "mgntflag": mgntFlag,
                                "mgntport": mgntPort
                                }

switchConfigGenerate = template.render(switchConfigTemplateVariable)
print(switchConfigGenerate, file=open(configOutPutFile,"w"))
print("config file created in : "+configOutPutFile)

