PYTHONDONTWRITEBYTECODE=1


from tqdm import tqdm
import pandas as pd
import datetime
import sys


# custom libs #
from config import *
sys.path.insert(0, './src/az_cli_snowflake/connectors')
from Snowpark import Snowpipe

sys.path.append('./src/az_cli_snowflake')
from collect import az_methods

#############################################################################

# import credentials and login#

az_conn             = global_settings().get_az_credentials
snowflake_conn      = global_settings().get_snowflake_credentials


_client_id          = os.getenv('service_principal')
_client_secret      = os.getenv('client_secret')
_tenant             = os.getenv('tenant')
_subscription       = os.getenv("subscription")
environment         = os.getenv("environment")


#global_settings().login_az_cli

# import default terminal

exe = global_settings().terminal_exec_app
MY_DB =''
MY_SCHEMA =''
############################################################################


# start
starttime = datetime.datetime.now()


###########################################################################

# set limit for testing #
set_limit = None

###########################################################################
print("____-main-_____")
print('Running on : ', os_type)
print('default terminal is : ',exe)
print('started time : ',starttime)


# build target table if not exists
print('Building Target Table if not present')
build_table_sql = open('src/az_cli_snowflake/queries/build_resource_table.sql','r').read()
exec_build = Snowpipe(connection_parameters=snowflake_conn).execute_query(build_table_sql).collect()
print(exec_build)


# Update TAGS in Azure using UDT's in Snowflake
sw_tag_df           = Snowpipe(connection_parameters=snowflake_conn).get_pdf(f"Select RESOURCE_ID, User_Defined_Tags from {MY_DB}.{MY_SCHEMA}.T_RESOURCE_INFO_FACT where not is_null_value(USER_DEFINED_TAGS)")

record_count = sw_tag_df.shape[0]
if record_count < 1 or record_count == None:
    print('No Tags to update')
else:
    deploy_tags         = az_methods(exec=exe , environment=environment,pdf=sw_tag_df).az_deploy_tags(limit=set_limit)
    print(deploy_tags)


# Generate Data from Azure Environment #
# Send Data to Snowflake Control Table#
pdf = az_methods(exec=exe , environment= environment).az_collect_resource(limit= set_limit)
swdf = Snowpipe(connection_parameters=snowflake_conn).to_Snowpark_DF(tmptable_name= "AZURE_RESOURCES",pdf= pdf)
snow_merge= Snowpipe(connection_parameters=snowflake_conn).az_merge_into(source_df= swdf, target_table =f'{MY_DB}.{MY_SCHEMA}.T_RESOURCE_INFO_FACT',source_key = "RESOURCE_ID",target_key = "RESOURCE_ID")
print(snow_merge)


print('end time : ', datetime.datetime.now())
