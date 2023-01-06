
# AZ-SNOWFLAKE-BROKER


# Setup Instructions (Non Docker)

## Introduction
> *This application is packaged using poetry which is a dependency management library in python.*

This application acts as a broker between Azure and Snowflake allowing you to manage your azure resources from Snowflake by means of Snowflake tables.
## 1- Install python 
 ### windows (via chocolatey)

      Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
      choco install -y python --version=3.8.0

  ### Linux & Mac

      sudo apt-get install python3.8.0

   
## 2- Install Poetry

 ### Universal install using pip
> #*Not recommended unless running inside docker or isolated environment*#

      pip install poetry
      config virtualenvs.in-project true
 ### Windows install

      Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
      config virtualenvs.in-project true
 ### Linux, macOS, Windows (WSL) install

      curl -sSL https://install.python-poetry.org | python3 -
      config virtualenvs.in-project true


## 3- Setup VENV

 - install virtualenv `pip install virtualenv`
   - Check installed python versions `py --list`

## 4- Setup ide
[Configure PyCharm interpreter][config pycharm interpreter] or [Configure VS Code interpreter][config vscode interpreter] to use the previously created Python virtual environment.
#
### Tool usage (non docker)
1. Clone repo (`git clone`)
2. Go to project directory (`cd ./AZ-CLI-SNOWFLAKE`)
3. Create venv in your project (`virtualenv .venv -p python3.8`) 
   > if you don't have virtualenv installed run (`pip install virtualenv`)
4. Install python dependencies (`poetry install`)
5. Create your feature branch (`git checkout -b feature/fooBar`)
6. Add your snowflake.json and az.env file to the env folder (its part of the gitignore so if you commit back to repo will be excluded) 

    > When this runs from azure devops the az.env and the snowflake.json will be create by the build/release pipeline as they do not get commited to the repo for security reasons.

    az.env example:
    ```
    service_principal 	= "guid"
    client_secret 	= "pwd"
    tenant 		= "guid"
    subscription 	= "guid"
    environment 	= "string" 
    ```

    snowflake.json example:
    ```
    {
    "account": "",
    "user": "",
    "password": "",
    "database": "",
    "schema":"",
    "warehouse": "",
    "role": ""
    }
    ```

7. Add file to your git environment (`git add *`) 
8. Commit your changes (`git commit -am 'What i am planning to execute and why'`)
9. Run script (`poetry run python __main__.py`)




#
### Snowpark Overview

The Snowpark library provides an intuitive API for querying and processing data in a data pipeline. Using this library, you can build applications that process data in Snowflake without moving data to the system where your application code runs. Snowpark has several features that distinguish it from other client libraries

Snowpark operations are executed lazily on the server, which reduces the amount of data transferred between your client and the Snowflake database.

> Please note that the base snowpark library only allows one sql statement execution over session.sql so `use database ` and ` use schema` statements must be passed instead via the connection on snowflake.json file. There are ways around this using the snowflake python connector (execute_string) but are not part of this application az-snowflake-broker.

[Snowpark Documentation](https://docs.snowflake.com/en/developer-guide/snowpark/index.html)

#


### Az cli Overview

The Azure command-line interface (Azure CLI) is a set of commands used to create and manage Azure resources. The Azure CLI is available across Azure services and is designed to get you working quickly with Azure, with an emphasis on automation.

`az cli` comes with several built-in commands. 
More information can be found about this tool on the following 

[Microsoft az cli documentation link](https://learn.microsoft.com/en-us/cli/azure/resource?view=azure-cli-latest#az-resource-create)

[Microsoft adf cli documentation link](https://learn.microsoft.com/en-us/cli/azure/datafactory?view=azure-cli-latest)

### Basic Syntax 
az cli
```
az resource create
Create a resource.

az resource delete
Delete a resource.

az resource invoke-action
Invoke an action on the resource.

az resource link
Manage links between resources.

az resource link create
Create a new link between resources.

az resource link delete
Delete a link between resources.

az resource link list
List resource links.

az resource link show
Gets a resource link with the specified ID.

az resource link update
Update link between resources.

az resource list
List resources.

az resource lock
Manage Azure resource level locks.

az resource lock create
Create a resource-level lock.

az resource lock delete
Delete a resource-level lock.

az resource lock list
List lock information in the resource-level.

az resource lock show
Show the details of a resource-level lock.

az resource lock update
Update a resource-level lock.

az resource move
Moves resources from one resource group to another(can be under different subscription).

az resource show
Get the details of a resource.

az resource tag
Tag a resource.

az resource update
Update a resource.

az resource wait
Place the CLI in a waiting state until a condition of a resources is met.
   ```

   adf cli

   ```
az datafactory activity-run	
Manage activity run with datafactory.

az datafactory activity-run query-by-pipeline-run	
Query activity runs based on input filter conditions.

az datafactory configure-factory-repo	
Updates a factory's repo information.

az datafactory create	
Create a factory.

az datafactory data-flow	
Managing and configuring Data Flows in Azure Data Factory.

az datafactory data-flow create	
Creates a data flow within a factory.

az datafactory data-flow delete	
Delete a specific data flow in a given factory.

az datafactory data-flow list	
List data flows within a provided factory.

az datafactory data-flow show	
Show information about the specified data flow.

az datafactory data-flow update	
Updates a specified data flow within a factory.

az datafactory dataset	
Manage dataset with datafactory.

az datafactory dataset create	
Create a dataset.

az datafactory dataset delete	
Deletes a dataset.

az datafactory dataset list	
Lists datasets.

az datafactory dataset show	
Gets a dataset.

az datafactory dataset update	
Update a dataset.

az datafactory delete	
Deletes a factory.

az datafactory get-data-plane-access	
Get Data Plane access.

az datafactory get-git-hub-access-token	
Get GitHub Access Token.

az datafactory integration-runtime	
Manage integration runtime with datafactory.

az datafactory integration-runtime delete	
Deletes an integration runtime.

az datafactory integration-runtime get-connection-info	
Gets the on-premises integration runtime connection information for encrypting the on-premises data source credentials.

az datafactory integration-runtime get-monitoring-data	
Get the integration runtime monitoring data, which includes the monitor data for all the nodes under this integration runtime.

az datafactory integration-runtime get-status	
Gets detailed status information for an integration runtime.

az datafactory integration-runtime linked-integration-runtime	
Manage integration runtime with datafactory sub group linked-integration-runtime.

az datafactory integration-runtime linked-integration-runtime create	
Create a linked integration runtime entry in a shared integration runtime.

az datafactory integration-runtime list	
Lists integration runtimes.

az datafactory integration-runtime list-auth-key	
Retrieves the authentication keys for an integration runtime.

az datafactory integration-runtime managed	
Manage integration runtime with datafactory sub group managed.

az datafactory integration-runtime managed create	
Create an integration runtime.

az datafactory integration-runtime regenerate-auth-key	
Regenerates the authentication key for an integration runtime.

az datafactory integration-runtime remove-link	
Remove all linked integration runtimes under specific data factory in a self-hosted integration runtime.

az datafactory integration-runtime self-hosted	
Manage integration runtime with datafactory sub group self-hosted.

az datafactory integration-runtime self-hosted create	
Create an integration runtime.

az datafactory integration-runtime show	
Gets an integration runtime.

az datafactory integration-runtime start	
Starts a ManagedReserved type integration runtime.

az datafactory integration-runtime stop	
Stops a ManagedReserved type integration runtime.

az datafactory integration-runtime sync-credentials	
Force the integration runtime to synchronize credentials across integration runtime nodes, and this will override the credentials across all worker nodes with those available on the dispatcher node. If you already have the latest credential backup file, you should manually import it (preferred) on any self-hosted integration runtime node than using this API directly.

az datafactory integration-runtime update	
Updates an integration runtime.

az datafactory integration-runtime upgrade	
Upgrade self-hosted integration runtime to latest version if availability.

az datafactory integration-runtime wait	
Place the CLI in a waiting state until a condition of the datafactory integration-runtime is met.

az datafactory integration-runtime-node	
Manage integration runtime node with datafactory.

az datafactory integration-runtime-node delete	
Deletes a self-hosted integration runtime node.

az datafactory integration-runtime-node get-ip-address	
Get the IP address of self-hosted integration runtime node.

az datafactory integration-runtime-node show	
Gets a self-hosted integration runtime node.

az datafactory integration-runtime-node update	
Updates a self-hosted integration runtime node.

az datafactory linked-service	
Manage linked service with datafactory.

az datafactory linked-service create	
Create a linked service.

az datafactory linked-service delete	
Deletes a linked service.

az datafactory linked-service list	
Lists linked services.

az datafactory linked-service show	
Gets a linked service.

az datafactory linked-service update	
Update a linked service.

az datafactory list	
Lists factories. And Lists factories under the specified subscription.

az datafactory managed-private-endpoint	
Manage managed private endpoint with datafactory.

az datafactory managed-private-endpoint create	
Create a managed private endpoint.

az datafactory managed-private-endpoint delete	
Deletes a managed private endpoint.

az datafactory managed-private-endpoint list	
Lists managed private endpoints.

az datafactory managed-private-endpoint show	
Gets a managed private endpoint.

az datafactory managed-private-endpoint update	
Update a managed private endpoint.

az datafactory managed-virtual-network	
Manage managed virtual network with datafactory.

az datafactory managed-virtual-network create	
Create a managed Virtual Network.

az datafactory managed-virtual-network list	
Lists managed Virtual Networks.

az datafactory managed-virtual-network show	
Gets a managed Virtual Network.

az datafactory managed-virtual-network update	
Update a managed Virtual Network.

az datafactory pipeline	
Manage pipeline with datafactory.

az datafactory pipeline create	
Create a pipeline.

az datafactory pipeline create-run	
Creates a run of a pipeline.

az datafactory pipeline delete	
Deletes a pipeline.

az datafactory pipeline list	
Lists pipelines.

az datafactory pipeline show	
Gets a pipeline.

az datafactory pipeline update	
Update a pipeline.

az datafactory pipeline-run	
Manage pipeline run with datafactory.

az datafactory pipeline-run cancel	
Cancel a pipeline run by its run ID.

az datafactory pipeline-run query-by-factory	
Query pipeline runs in the factory based on input filter conditions.

az datafactory pipeline-run show	
Get a pipeline run by its run ID.

az datafactory show	
Gets a factory.

az datafactory trigger	
Manage trigger with datafactory.

az datafactory trigger create	
Create a trigger.

az datafactory trigger delete	
Deletes a trigger.

az datafactory trigger get-event-subscription-status	
Get a trigger's event subscription status.

az datafactory trigger list	
Lists triggers.

az datafactory trigger query-by-factory	
Query triggers.

az datafactory trigger show	
Gets a trigger.

az datafactory trigger start	
Starts a trigger.

az datafactory trigger stop	
Stops a trigger.

az datafactory trigger subscribe-to-event	
Subscribe event trigger to events.

az datafactory trigger unsubscribe-from-event	
Unsubscribe event trigger from events.

az datafactory trigger update	
Update a trigger.

az datafactory trigger wait	
Place the CLI in a waiting state until a condition of the datafactory trigger is met.

az datafactory trigger-run	
Manage trigger run with datafactory.

az datafactory trigger-run cancel	
Cancel a single trigger instance by runId.

az datafactory trigger-run query-by-factory	
Query trigger runs.

az datafactory trigger-run rerun	
Rerun single trigger instance by runId.

az datafactory update	
Updates a factory.
   ```

[deployment-diagram]: https://lucid.app/publicSegments/view/2d06c63f-a0ef-445f-a0e7-f9cde79ccfcb/image.png
[config pycharm interpreter]: https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html
[config vscode interpreter]: https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter
[tool usage]: https://lucid.app/publicSegments/view/f2af4d2e-a7f1-4af3-9920-7036113b1036/image.png
