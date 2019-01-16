#!/bin/python3
# -*- coding: utf-8 -*-
#Copyright (c) 2019 WAHED Shah Mohsin
#This code is under MIT licence, you can find the complete file here: https://github.com/shahwahed/SwitchConfigMaker/blob/master/LICENSE

import yaml
import json
import sys
import os
from jinja2 import Environment, FileSystemLoader
from pprint import pprint
#from gettext import gettext as _
import gettext
import locale
#en = gettext.translation('make_switch_config', localedir='locale', languages=['en_GB'])
#en.install()

current_locale, encoding = locale.getdefaultlocale()
print(current_locale)

locale_path = 'locale/'
language = gettext.translation('make_switch_config', locale_path, [current_locale], fallback=True )
#language = gettext.translation()
#language = gettext.translation ('make_switch_config', locale_path)
language.install()

#script variable
#TODO : input variable?
#template_file = 'cisco2960-cg.template.ios'
template_file = 'cisco2960.template.ios'

jinja_dir = 'jinja_templates'
vlan_json_file = 'json/vlan_example.json'
switch_description_json_file = 'json/switch_port_config_example.json'
switch_model_definition_file = 'json/switch_model.json'

def main_menu(menuItem):
    os.system('clear')
    while True:
        try :
            print(_('Liste des configuration de switch disponible :'))
            for menuValue in menuItem:
                print(str(menuItem.index(menuValue)) + " - " + menuValue)
            print(_(" Ctrl + D pour quitter"))
            choice = int(input("  >>  "))
            return menuItem[int(choice)]
        except ValueError:
                print(_("ce n'est pas un chiffre"))
        except IndexError:
                print(_("Valeur non disponble"))


#script path
script_dir = os.path.dirname(os.path.realpath(__file__))

#jinja template dir
jinja_template_dir = os.path.join(script_dir,jinja_dir)

# vlan json
# todo : make this variable may be?
vlanfile = os.path.join(script_dir,vlan_json_file)

# switch configuration json file
# todo : make this variable may be?
switchjsonfile = os.path.join(script_dir,switch_description_json_file)

# switch model json file
# todo : make this variable may be?
switchmodeljsonfile = os.path.join(script_dir,switch_model_definition_file)


#create Jinja2 environment object and refer to templates directory
env = Environment(loader=FileSystemLoader(jinja_template_dir))

# jinja template
# todo : may be retrive this from switch config file
#create Jinja2 template object based off of template named 'switch_ios'
template = env.get_template(template_file)

#portDict dictionary containing portname based on switchs models
portDict = {}
switchNameList = []

#json file loading

#vlanconfig => containing vlan definition, to keep every switch consitent
vlanconfig = json.loads(open(vlanfile).read())

#json file for switch models definition
switchmodeldb = json.loads(open(switchmodeljsonfile).read())

#json file configuration of the switch, take from command line
configjson = json.loads(open(switchjsonfile).read())

#json file loading end

for switch in configjson:
    switchNameList.append(switch)

switchname = main_menu(sorted(switchNameList))

configOutPutFile = script_dir + "/output/" + switchname + ".ios"

hostname = configjson[switchname]['hostname']
vlan_domain = configjson[switchname]['vlan_domain']
vlans = vlanconfig[vlan_domain]['vlans']
vlandict = { vlan["name"]: vlan["id"] for vlan in vlans}

#creation of a dict of port using by your config
modulePortconfig = switchmodeldb.get(configjson[switchname]['model']).get('access_port')
for modPort in modulePortconfig.keys():
    portStart = modulePortconfig[modPort]['start']
    portEnd = modulePortconfig[modPort]['end']
    portName = modulePortconfig[modPort]['name']

    for portID in range(portStart, portEnd +1):
        portDict[str(portID)] = portName + str(portID)
if switchmodeldb.get(configjson[switchname]['model']).get('management_port').get('embedded'):
    mgntFlag = True
    mgntPort = switchmodeldb.get(configjson[switchname]['model']).get('management_port').get('name')
else:
    mgntFlag = False
    mgntPort = 'None'

# we create emptyPortDict variable, to shutdown everyport you're not using
emptyPortDict = { emptyPort['port']: "null" for emptyPort in configjson[switchname].get('interfacephy') }
emptyPortDict = portDict.keys() - emptyPortDict.keys()
# uggly hack to sort correctly the dictonary, cause 10 goes before 1 in string sort, so we send jinja2 int, sorted correctly
# then in jinja2 convert them to string to join them properly with correct name
emptyPortDict = {int(x) for x in emptyPortDict}
emptyPortDict = sorted(emptyPortDict)


#uncomment next line for debug
#pprint(ma_var)
#sys.exit()

# json variable send to jinja template

ciscoConfigTemplateVariable =   {"vlans": vlans,
                                "hostname": hostname,
                                "configjson": configjson[switchname],
                                "vlandict": vlandict,
                                "portdict": portDict,
                                "emptyportdict": emptyPortDict,
                                "mgntflag": mgntFlag,
                                "mgntport": mgntPort
                                }

ciscoConfigGenerate = template.render(ciscoConfigTemplateVariable)
print(ciscoConfigGenerate, file=open(configOutPutFile,"w"))
print(_("fichier de configuration généré %s") % (configOutPutFile))




