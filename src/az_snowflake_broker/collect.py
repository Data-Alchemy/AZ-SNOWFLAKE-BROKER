PYTHONDONTWRITEBYTECODE=1



from tqdm import tqdm
import pandas as pd
import subprocess
import datetime
import chardet
import json 
import sys
import os

sys.path.append('config')
sys.path.insert(0, './src/az_cli_snowflake/connectors')

from Snowpark import Snowpipe




###########################################################################


pd.set_option('display.max_rows'        , None)
pd.set_option('display.max_columns'     , None)
pd.set_option('display.width'           , None)
pd.set_option('display.max_colwidth'    , None)

###########################################################################

# import credentials #


_client_id          = os.getenv('service_principal')
_client_secret      = os.getenv('client_secret')
_tenant             = os.getenv('tenant')
_subscription       = os.getenv("subscription")
_environment        = os.getenv("environment")

# import default terminal



###########################################################################
class az_methods:
    '''
    This class is used to compile code and data for snowpark functions
    '''

    def __init__(self, exec:str,environment:str =environment , pdf:pd.DataFrame= None, file_path:str = None):
       self.pdf         = pdf
       self.file_path   = file_path
       self.environment = environment
       self.exec        = exec

    def az_tst(self):
        return  f"az login --output none --service-principal -u {_client_id} -p {_client_secret} --tenant {_tenant} --only-show-errors"

    def az_cli_exec(self,*x)->bool:

        for i in x:

            try:
                subprocess.check_output([fr"{self.exec}","-c",i],stderr=subprocess.DEVNULL)
                return True

            except Exception as e:
                #print('command : ', i , '\n failed due to error :\n ',e)
                return False


    def az_cli_return(self,*x):
        for i in x:

            try:
                proc = subprocess.check_output([fr"{self.exec}","-c", i],stderr=subprocess.DEVNULL)
                encoding = chardet.detect(proc)['encoding']
                decoded_data = proc.decode(encoding)
                json_data = json.dumps(json.loads(decoded_data))
                return json_data

            except Exception as e:
                #print('command : ', i , '\n failed due to error :\n ',e)
                return None


    
    def az_collect_resource(self, limit:int =None)->pd.DataFrame:
        """
        Runs azure cli to collect information about resources in a given tenant
        Returns:
            Pandas Dataframe with output of CLI (From Json)
        """

        tqdm.pandas(desc='Az Collect Resources')

        desired_columns = ["createdTime","id","name","location","type","tags","resourceGroup","PROPERTIES"]
        col_mapping = {'createdTime':'RESOURCE_CREATION_TS','id':'RESOURCE_ID','name':'RESOURCE_NAME','location':'LOCATION','type':'TYPE','tags':'TAGS','resourceGroup':'RESOURCE_GROUP'}

        az_collect = f"""
        az resource list --output json
        """

        
        #proc = subprocess.check_output([fr'{self.exec}', az_collect])
        #encoding = chardet.detect(proc)['encoding']
        #decoded_data = proc.decode(encoding)
        decoded_data = self.az_cli_return(az_collect)
        df = pd.read_json(decoded_data)
        df = df.head(limit)

        try:
            df['PROPERTIES']      = df.progress_apply(lambda x: self.az_cli_return(f"az resource show --id '{x['id']}'"), axis = 1)
        except:
            None

        df                      = df[desired_columns]
        df                      = df.reset_index(drop=True) 
        df.rename( columns = col_mapping, inplace= True)
        df['CLOUD_PROVIDER']    = 'AZURE'
        df['DESCRIPTION']       = None
        df['ETL_MODIFIED_TS']   = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        df['MOD_ACTION_TYPE']   = 'U'
        df['ENVIRONMENT']       = self.environment
        return df

    def build_tags_cli(self,dict_input):
        listoftags= []


        if dict_input is not None:
            if type(dict_input) == str:
                dict_input= json.loads(dict_input)
            else:
                dict_input = dict_input
                
            for item in dict_input.items():
                listoftags.append(f'"{item[0]}"="{item[1]}"')
            return " ".join(listoftags)

        else:
            return ""



    def az_deploy_tags(self, limit:int=None)->pd.DataFrame:    
        """
        Runs azure cli to push tags to a specified resource by reading a snowflake table
        Inputs:
            pandas dataframe
        Returns:
            pandas dataframe
        """

        tqdm.pandas(desc='Deploy Tags')
        self.tag_df = self.pdf
        self.tag_df.head(limit)

        self.tag_df                         =   self.pdf
        self.tag_df['USER_DEFINED_TAGS']    =   self.tag_df['USER_DEFINED_TAGS'].apply(lambda x: x)
        self.tag_df['CLI_TAGS']             =   self.tag_df.apply(lambda x: f"az resource tag --tags {self.build_tags_cli(x['USER_DEFINED_TAGS'])} --ids '{x['RESOURCE_ID']}'",axis =1 )
        self.tag_df['Deploy_Tags']          =   self.tag_df.progress_apply(lambda x: self.az_cli_exec(f"{x['CLI_TAGS']}"), axis = 1)
        return self.tag_df

  


"""# Sample Usage
# limit is optional param used for testing or demos #
# exec is automatically determined from the config.py but can also be overwritten #
spdf = az_methods(exec='powershell' , environment=environment).az_collect_resource(limit= 10)
#print(spdf)
tags= az_methods(exec='powershell' , environment=environment,pdf=spdf).az_deploy_tags(limit=10)
print(tags)
"""