<br />
<p align="center">
  <a href="https://github.com/shahwahed/SwitchConfigMaker">
  </a>

  <h3 align="center">SwitchConfigMaker</h3>

  <p align="center">
    A simple python script to create switch config based on jinja2 template and json config file
    <br />
    <a href="https://github.com/shahwahed/SwitchConfigMaker/issues">Report Bug</a>
    ·
    <a href="https://github.com/shahwahed/SwitchConfigMaker/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li><a href="#Disclaimer">Disclaimer</a></li>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built with</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#configuration">Configuration</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- Disclaimer -->
## Disclaimer
Be mindful that some of these software might contain bugs or be harmful.
Use these scripts at your own risk.

DO NOT USE THIS SCRIPT FOR PRODUCTION USE! if you want to use it on production, review each template to fit with your need and review security configuration, test configuration.

<!-- ABOUT THE PROJECT -->
## About The Project

This project was just a simple script to create IOS and NXOS configuration using jinja2 template and json file for lab environment. You can do other switchs using your own jinja2 template.

### Built With

* [python 3.x]
* [jinja2]



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

python 3.x

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/shahwahed/SwitchConfigMaker.git
   ```


<!-- USAGE EXAMPLES -->
## Usage

Just run the script after configure vlan and switch configuration file.

   ```sh
   python3 make_switch_config.py
   ```

<!-- Configuration EXAMPLES -->
## Configuration

You need to edit three files to get your switch config :

* [json/vlan.json] : vlan configuration
* [json/switch_port_config.json] switch configuration
* [jinja_templates/*] any template your use to change password and ssh key


* vlan.json file :
```
{
	"admin": {
		"vlans": [
            {
                "name": "NATIVE", 
                "description": "Native", 
                "id": "777"
            },             {
                "name": "QUARANTINE", 
                "description": "Quarantine vlan", 
                "id": "666"
            },             {
                "name": "WKS_ZA", 
                "description": "Admin workstation", 
                "id": "100"
            }, 
            {
                "name": "ADM01", 
                "description": "Administration vlan 01", 
                "id": "101"
            },
            {
                "name": "ADM02", 
                "description": "Administration vlan 02", 
                "id": "102"
            },
            {
                "name": "OOB01", 
                "description": "Out of Band vlan 01", 
                "id": "103"
            }
        ]

    },
    "prod": {
        "vlans": [
            {
                "name": "NATIVE", 
                "description": "Native vlan", 
                "id": "777"
            },             {
                "name": "QUARANTINE", 
                "description": "Quarantine vllan", 
                "id": "666"
            },
            {
                "name": "PROD01", 
                "description": "Production vlan 01", 
                "id": "201"
            }, 
            {
                "name": "STK01", 
                "description": "Storage vlan 01", 
                "id": "202"
            }
		]
    }
}
```
Vlan definition is simple, a domain to separate, admin, prod, preprod
a name (useful for cisco config), a description to remember the need of the vlan and an ID.


* switch_port_config.json file:
```
{
	"switch01": {
		"hostname": "switch01",
		"vlan_domain": "admin",
		"mgntportuse": true,
		"model": "WS-C2960S-48TD-L",
		"interfacemgnt": [
			{
			"port": "Fastethernet0",
			"description": "administration ip",
			"ip": "192.168.1.21 255.255.255.0"
			}
		],
        "interfacephy": [
			{
				"port": "1", 
				"description": "Admin ESX01 - port1", 
				"profile": "trunk", 
				"vlans": "ADM01, ADM02"
			}, 
			{
				"port": "2", 
				"description": "OOB ESX01 - idrac", 
				"profile": "access", 
				"vlans": "OOB01"
			}
		]

	},
	"switch02": {
		"hostname": "switch02",
		"vlan_domain": "prod",
		"mgntportuse": true,
		"model": "WS-C2960X-48-FPS-L",
		"interfacemgnt": [
			{
			"port": "Fastethernet0",
			"description": "interface IP d'administration",
			"ip": "192.168.1.2 255.255.255.0"
			}
		],
        "interfacephy": [
			{
				"port": "3",
				"description": "ESX PROD 01 - port 2",
				"profile": "trunk",
				"vlans": "PROD01, STK01"
			},
			{
				"port": "4",
				"description": "ESX PROD 02 - port 2",
				"profile": "trunk",
				"vlans": "PROD01, STK01"
			},
      			{
				"port": "5",
				"description": "STK SRV 01 - port 2",
				"profile": "trunkchannel",
				"vlans": "PROD01, STK01",
        "portchannel": "50"
			},
			{
				"port": "6",
				"description": "STK SRV 01 - port 3",
				"profile": "trunkchannel",
				"vlans": "PROD01, STK01",
        "portchannel": "50"
			}
		]

	}
}
```
to define a switch you have to define a switchname node with the following :
hostname
vlan_domain
mgntportuse: true or false (to configure management port on cisco)
		"model": "WS-C2960S-48TD-L" use to define port name and number based on switch model
		"interfacemgnt": use for setup management interface could be phyical or vlan for cisco switch
			{
			"port": "Fastethernet0",
			"description": "administration ip",
			"ip": "192.168.1.21 255.255.255.0"
			}
		],
        "interfacephy" : to define all interface your use, not use will be shutdown
			{
				"port": "1", 
				"description": "Admin ESX01 - port1", 
				"profile": "trunk", 
				"vlans": "ADM01, ADM02"with 
			},

port profile could be access, trunk, accesschannel, trunkchannel, shutdown, your could define your custom profile according to your needs in cisco_macros.j2 (for Cisco IOS switch and ciscoNX_macros.j2 for Cisco NXOS switch)

By default, none configured ports will be put in shutdown profile

*channel, is for configuring portchannel, you have to put sevreal port with the same portchannel number

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/shahwahed/SwitchConfigMaker/issues) for a list of proposed features (and known issues).

* add json file or hashicorp vault support to store password and ssh key

* cleanup template file

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact


Project Link: [https://github.com/shahwahed/SwitchConfigMaker](https://github.com/shahwahed/SwitchConfigMaker)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* []()
* []()
* []()





<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/shahwahed/SwitchConfigMaker.svg?style=for-the-badge
[contributors-url]: https://github.com/shahwahed/SwitchConfigMaker/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/shahwahed/SwitchConfigMaker.svg?style=for-the-badge
[forks-url]: https://github.com/shahwahed/SwitchConfigMaker/network/members
[stars-shield]: https://img.shields.io/github/stars/shahwahed/SwitchConfigMaker.svg?style=for-the-badge
[stars-url]: https://github.com/shahwahed/SwitchConfigMaker/stargazers
[issues-shield]: https://img.shields.io/github/issues/shahwahed/SwitchConfigMaker.svg?style=for-the-badge
[issues-url]: https://github.com/shahwahed/SwitchConfigMaker/issues
[license-shield]: https://img.shields.io/github/license/shahwahed/SwitchConfigMaker.svg?style=for-the-badge
[license-url]: https://github.com/shahwahed/SwitchConfigMaker/blob/master/LICENSE.txt





