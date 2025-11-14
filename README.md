# NetOps-Enhanced
![Python Version](https://img.shields.io/badge/python-3.11-blue)
![Ansible](https://img.shields.io/badge/ansible-automation-red)
![License](https://img.shields.io/github/license/gwill1337/NetOps-Enhanced)

## About
**NetOps-Enhanced** this enhanced version of **NetOps** project. This project provides an automated network validation CI/CD pipeline powered by Batfish, Ansible, and GitHub Actions. It supports customizable configuration tests, ensuring that all network configs are validated, verified, and safely backed up. The project also supports generating device configurations using Jinja2 templates.  




## Set Up
1. Create repository secrets named **TG_CHAT_ID**, **TG_BOT_TOKEN** - for notifications in Telegram. And **GH_PAT** for backups into repository. *Guide how create tokens are below*.
2. Create config for tests. In folder **./tests/config/** create **config.yaml** via **[config_guide.md](https://github.com/gwill1337/NetOps-Enhanced/blob/main/tests/config/config_guide.md)**.
3. Create config for Nornir. In folder **./inventory** configure nornir at least **hosts.yaml**.
4. Configure your configs for validation. 
   * For manual configs -> paste configs into folder **./snapshots/ci_net/configs/manual/**
   * For auto version with jinja2 -> paste configs into folder **./snapshots/ci_net/device-yaml/**    [config guide](https://github.com/gwill1337/NetOps-Enhanced/blob/main/snapshots%20%20/ci_net/device-yaml/Device_yaml_guide.md)   

## Customize
You can customize -> jinja2 templates, tests, configs and etc. for nornir. Project map are below. 

## Security
For security in the CI workflow, use Ruff lint to validate all Python scripts, including tests.
The test suite also includes validation tests and security tests, which rely on the [test configuration](https://github.com/gwill1337/NetOps-Enhanced/blob/main/tests/config/config_guide.md).

## Tests and Validation
> ⚠️ **Note:** This project includes a basic default test, but for the best results you should create and customize your own validation tests.
## Deploy Nornir
> ⚠️ **Note:** This project includes a basic Nornir config only for connection test, for the best results you should create and customize your own Nornir configs.


## Execution CI/CD

On config push, the CI/CD pipeline steps:   
1. Sets up Python 3.11
2. Install requirements
3. Quick lint all python scripts with ruff
4. Downloads and starts Batfish in Docker
5. Prepares Batfish directories
6. Generates configs from YAML (if present)
7. Ensure Batfish snapshot folder exists (Ansible)
8. Runs PyTest validation
9. Notify in Telegram Success or Failure
10. Creates backup of generated configs (on success)
11. Commits and pushes backups to the repo (on success)
12. Deploy configs (Nornir)
13. Notify in telegram that Deploy Successfuly or not

## Support vendors
Out of the box, the project supports generating configs from YAML for Cisco, Juniper, and Palo Alto Networks.
In fact, the project supports [**all vendors supported by batfish**](https://batfish.readthedocs.io/en/latest/supported_devices.html) but configuration generation is manual except for the three vendors mentioned above.
But you can create your own jinja2 template for config generation.


## Repository structure/map
This project includes many directories, structured as illustrated below:
```
NetOps-Enhanced/
├── .github/
│    └── workflows/
│        ├── CI_Validation.yml
│        └── CD_Deploy.yml
│
├── backup/       <-- Backup storage for validated configs    
│   └── *.cfg
│
├── inventory   <-- Inventory for nornir
│   ├── defaults.yaml
│   ├── groups.yaml
│   └── hosts.yaml
│
├── requirements
│   ├── ci_requirements.txt
│   └── cd_requirements.txt
│
├── ansible/   
│   ├── hosts     
│   └── playbook.yml                  
│   
├── snapshots/   
│   └── ci_net/      
│       ├── configs/   
│       │   ├── manual/
│       │   │   └── *.cfg
│       │   └──generated/
│       │      └── *.cfg     
│       └── device-yaml/
│           ├── Device_yaml_guide.md
│           └── *.yaml               
│   
├── tests/    
│   ├── security/
│   │   └── test_security.py
│   ├── validation/
│   │   └── test_validation.py
│   └── config/
│       └── config_guide.md        
│   
├── tools/
│   ├── templates/
│   │   └── *.j2   
│   ├── conf-generator.py
│   ├── deploy_connect.py                    
│   └── render_config.py               
│           
├── config.yaml  <-- Config for nornir   
├── README.md   
└── LICENSE   
 ```

## Repository Secrets Guide
1. **GitHub Personal Access Token (GH_PAT)**
   * Go to **GitHub** -> **Settings** -> **Developer settings** -> **Personal access tokens** -> **Tokens (classic)** -> **Generate new token**.
   * Select scopes: **repo** (for repository access) and **workflow** (for GitHub Actions).
   * Copy the token.
   * Go to your repository -> **Settings** -> **Secrets** -> **Actions** -> **New repository secret**.
   * Name it **GH_PAT** and paste the token. 
  
2. **Telegram Bot Token (TG_BOT_TOKEN)**
   * Open Telegram and search for **BotFather**.
   * Create new bot.
   * Copy the **API token** given by BotFather.
   * Go to your repository -> **Settings** -> **Secrets** -> **New repository secret**.
   * Name it **TG_BOT_TOKEN** and paste the token.
3. **Telegram Chat ID (TG_CHAT_ID)**
   * Open Telegram and search for **@userinfobot**.
   * Start the bot and send **/start**.
   * The bot will reply with your chat ID.
   * Go to repository secrets -> **New secret** -> Name it **TG_CHAT_ID** and paste the ID.
