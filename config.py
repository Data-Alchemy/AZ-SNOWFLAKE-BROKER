PYTHONDONTWRITEBYTECODE=1

from dotenv import load_dotenv
import subprocess
import platform
import json
import sys
import os


os_type = platform.system()
sys.path.insert(0, 'src/az_cli_snowflake/connectors')



class global_settings():
    '''
    This class contains global settings for this package, detecting the operating system that the package is being executed on and installing the azure cli if not already installed. This check will run everytime the class is called and will return True or False
    '''

    def __init__(self,os:str = os_type):
        self.os  = os
    
    @property
    def terminal_exec_app(self):
        '''
        base executable for a given os 
        '''
        os_exe_map = {
        'Windows':'powershell',
        'Linux':'/bin/bash',
        'Darwin':'/bin/bash'
        }
        self.exe = os_exe_map[self.os]
        return self.exe

    @property
    def install_az_cli(self):
        '''
        os specific install command for az cli
        '''
        os_exe_map = {
        'Windows':"$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; rm .\AzureCLI.msi",
        'Linux':'curl -L https://aka.ms/InstallAzureCli | bash',
        'Darwin':'NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)";brew update && brew install azure-cli'
        }
        return os_exe_map[self.os]

    @property
    def check_for_az_cli(self):
        '''
        check for presence of az cli and install it if not
        '''
        try: 
            subprocess.check_output([f"{self.terminal_exec_app}","az --version"])
            return True
        except:

            try:
                print(f'installing azure cli for {self.terminal_exec_app}')
                subprocess.check_output([f"{self.terminal_exec_app}", f"{self.install_az_cli}"])
                return True

            except Exception as e:
                print(( 'Unable to setup azure cli \n error is :', e))
                return False

    @property
    def login_az_cli(self):
        '''
        login az cli and install it if not
        '''
        az_conn             = self.get_az_credentials

        _client_id          = os.getenv('lll_service_principal')
        _client_secret      = os.getenv('lll_client_secret')
        _tenant             = os.getenv('lll_tenant')
        _subscription       = os.getenv("lll_subscription")
        try: 
            subprocess.check_output([f"{self.terminal_exec_app}",f"az login --output none --service-principal -u {_client_id} -p {_client_secret} --tenant {_tenant} --only-show-errors"])
            return True
        except:
            raise IOError ('unable to login to azure cli please verify credentials provided are correct and have proper access to specified environment')

    @property
    def test_az_cli(self):
        subprocess.check_output([f"{self.terminal_exec_app}","-c",f"az --version"])


    @property
    def get_az_credentials(self):
        azcli_env = os.path.abspath(r'env/az.env')
        return load_dotenv(azcli_env)

    @property
    def get_snowflake_credentials(self):
        conn_file = open(r'env/snowflake.json')
        _connection_parameters = json.load(conn_file)
        return _connection_parameters



#############################################################################
# import credentials #
az_conn             = global_settings().get_az_credentials
snowflake_conn      = global_settings().get_snowflake_credentials

_client_id          = os.getenv('service_principal')
_client_secret      = os.getenv('client_secret')
_tenant             = os.getenv('tenant')
_subscription       = os.getenv("subscription")
environment         = os.getenv("environment")

os.environ['Default_Terminal'] = global_settings().terminal_exec_app
############################################################################
#test az cli #
#snowflake_conn      = print(global_settings().test_az_cli)
