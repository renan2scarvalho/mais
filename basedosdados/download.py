import pandas_gbq
from pathlib import Path
import pydata_google_auth
from google.cloud import bigquery

from basedosdados.exceptions import BaseDosDadosException
from pandas_gbq.gbq import GenericGBQException


def credentials(reauth=False):

    SCOPES = [
        "https://www.googleapis.com/auth/cloud-platform",
    ]

    if reauth:
        return pydata_google_auth.get_user_credentials(
            SCOPES, credentials_cache=pydata_google_auth.cache.REAUTH
        )
    else:
        return pydata_google_auth.get_user_credentials(
            SCOPES,
        )
        
    
def download(
    savepath,
    query=None,
    dataset_id=None,
    table_id=None,
    query_project_id="basedosdados",
    billing_project_id=None,
    limit=None,
    reauth=False,
    **pandas_kwargs,
):
    """Download table or query result from basedosdados BigQuery (or other).

    * Using a **query**:

        `download('select * from `basedosdados.br_suporte.diretorio_municipios` limit 10')`

    * Using **dataset_id & table_id**:

        `download(dataset_id='br_suporte', table_id='diretorio_municipios')`

    You can also add arguments to modify save parameters:

    `download(dataset_id='br_suporte', table_id='diretorio_municipios', index=False, sep='|')`


    Args:
        savepath (str, pathlib.PosixPath):
            If savepath is a folder, it saves a file as `savepath / table_id.csv` or
            `savepath / query_result.csv` if table_id not available.
            If savepath is a file, saves data to file.
        query (str): Optional.
            Valid SQL Standard Query to basedosdados. If query is available,
            dataset_id and table_id are not required.
        dataset_id (str): Optional.
            Dataset id available in basedosdados. It should always come with table_id.
        table_id (str): Optional.
            Table id available in basedosdados.dataset_id.
            It should always come with dataset_id.
        query_project_id (str): Optional.
            Which project the table lives. You can change this you want to query different projects.
        billing_project_id (str): Optional.
            Project that will be billed. Find your Project ID here https://console.cloud.google.com/projectselector2/home/dashboard
        limit (int): Optional
            Number of rows.
        reauth (boolean): Optional.
            Re-authorize Google Cloud Project in case you need to change user or reset configurations.
        pandas_kwargs ():
            Extra arguments accepted by [pandas.to_csv](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html)

    Raises:
        Exception: If either table_id or dataset_id were are empty.
    """

    savepath = Path(savepath)

    if (dataset_id is not None) and (table_id is not None):
        table = read_table(
            dataset_id,
            table_id,
            query_project_id=query_project_id,
            billing_project_id=billing_project_id,
            limit=limit,
            reauth=reauth,
        )

    elif query is not None:

        query += f" limit {limit}" if limit is not None else ""

        table = read_sql(query, billing_project_id=billing_project_id, reauth=reauth)

    elif query is None:
        raise BaseDosDadosException(
            "Either table_id, dataset_id or query should be filled."
        )

    if savepath.is_dir():
        if table_id is not None:
            savepath = savepath / (table_id + ".csv")
        else:
            savepath = savepath / ("query_result.csv")

    table.to_csv(savepath, **pandas_kwargs)


def read_sql(query, billing_project_id=None, reauth=False):
    """Load data from BigQuery using a query. Just a wrapper around pandas.read_gbq

    Args:
        query (sql):
            Valid SQL Standard Query to basedosdados
        billing_project_id (str): Optional.
            Project that will be billed. Find your Project ID here https://console.cloud.google.com/projectselector2/home/dashboard
        reauth (boolean): Optional.
            Re-authorize Google Cloud Project in case you need to change user or reset configurations.

    Returns:
        pd.DataFrame:
            Query result
    """

    try:
        return pandas_gbq.read_gbq(
            query,
            credentials=credentials(reauth=reauth),
            project_id=billing_project_id,
        )
    except (OSError, ValueError):
        raise BaseDosDadosException(
            "\nWe are not sure which Google Cloud project should be billed.\n"
            "First, you should make sure that you have a Google Cloud project.\n"
            "If you don't have one, set one up following these steps: \n"
            "\t1. Go to this link https://console.cloud.google.com/projectselector2/home/dashboard\n"
            "\t2. Agree with Terms of Service if asked\n"
            "\t3. Click in Create Project\n"
            "\t4. Put a cool name in your project\n"
            "\t5. Hit create\n"
            ""
            "Copy the Project ID, (notice that it is not the Project Name)\n"
            "Now, you have two options:\n"
            "1. Add an argument to your function poiting to the billing project id.\n"
            "   Like `bd.read_table('br_ibge_pib', 'municipios', billing_project_id=<YOUR_PROJECT_ID>)`\n"
            "2. You can set a project_id in the environment by running the following command in your terminal: `gcloud config set project <YOUR_PROJECT_ID>`."
            "   Bear in mind that you need `gcloud` installed."
        )
    except GenericGBQException as e:
        if "Reason: 403" in str(e):
            raise BaseDosDadosException(
                "\nYou still don't have a Google Cloud Project.\n"
                "Set one up following these steps: \n"
                "1. Go to this link https://console.cloud.google.com/projectselector2/home/dashboard\n"
                "2. Agree with Terms of Service if asked\n"
                "3. Click in Create Project\n"
                "4. Put a cool name in your project\n"
                "5. Hit create\n"
                "6. Rerun this command with the flag `reauth=True`. \n"
                "   Like `read_table('br_ibge_pib', 'municipios', reauth=True)`"
            )
        else:
            raise e


def read_table(
    dataset_id,
    table_id,
    query_project_id="basedosdados",
    billing_project_id=None,
    limit=None,
    reauth=False,
):
    """Load data from BigQuery using dataset_id and table_id.

    Args:
        dataset_id (str): Optional.
            Dataset id available in basedosdados. It should always come with table_id.
        table_id (str): Optional.
            Table id available in basedosdados.dataset_id.
            It should always come with dataset_id.
        query_project_id (str): Optional.
            Which project the table lives. You can change this you want to query different projects.
        billing_project_id (str): Optional.
            Project that will be billed. Find your Project ID here https://console.cloud.google.com/projectselector2/home/dashboard
        reauth (boolean): Optional.
            Re-authorize Google Cloud Project in case you need to change user or reset configurations.
        limit (int): Optional.
            Number of rows to read from table.

    Returns:
        pd.DataFrame:
            Query result
    """

    if (dataset_id is not None) and (table_id is not None):
        query = f"""
        SELECT * 
        FROM `{query_project_id}.{dataset_id}.{table_id}`"""

        if limit is not None:

            query += f" LIMIT {limit}"
    else:
        raise BaseDosDadosException("Both table_id and dataset_id should be filled.")

    return read_sql(query, billing_project_id=billing_project_id, reauth=reauth)


def list_datasets(
    project_id='basedosdados', 
    filter_by=None, 
    with_description=False
):
    
    client = bigquery.Client(credentials=credentials(), project=project_id)
    
    datasets = list(client.list_datasets())
    
    datasets_list = pd.DataFrame([dataset.dataset_id for dataset in datasets], columns=['dataset_id'])
    
    
    if filter_by:
        
        datasets_list = datasets_list.loc[datasets_list['dataset_id'].str.contains(filter_by)]
    
    if with_description:
        
        indexes = list(datasets_list.index)
        
        datasets_list['description'] = [client.get_dataset(datasets_list.at[index, 'dataset_id']).description
                                       for index in indexes]
    
    #FOR THE FULL TABLE DESCRIPTION ONE CAN USE  
    
    return datasets_list


def list_dataset_tables(
    dataset_id, 
    project_id='basedosdados',
    filter_by=None,
    with_description=False
):
    
    client = bigquery.Client(credentials=credentials(), project=project_id)
    
    dataset = client.get_dataset(dataset_id)
    
    tables = list(client.list_tables(dataset))
    
    tables_list = pd.DataFrame(
        [table.table_id for table in tables], 
        columns=['table_id'])
    
    if filter_by:
      
        tables_list = tables_list.loc[tables_list['table_id'].str.contains(filter_by)]
        
    if with_description:
        
        indexes = list(tables_list.index)
        
        tables_list['description'] = [client.get_table
                                      (f"{project_id}.{dataset_id}.{tables_list.at[index,'table_id']}"
                                      ).description for index in indexes]
        
        
    return tables_list

def get_dataset_description(
    dataset_id=None, 
    project_id = 'basedosdados'
):
    client =  bigquery.Client(credentials=credentials(), project=project_id)
    
    dataset = client.get_dataset(dataset_id)
    
    print(dataset.description)
    
    return None

def get_table_description(
    dataset_id = None, 
    table_id = None, 
    project_id='basedosdados'
):
    client = bigquery.Client(credentials = credentials(), project = project_id)
    
    table = client.get_table(f'{dataset_id}.{table_id}')
    
    print(table.description)
    
    return None

def get_table_columns(
    dataset_id=None, 
    table_id=None, 
    project_id='basedosdados'
):
    client = bigquery.Client(credentials = credentials(), project = project_id)
    
    table_ref = client.get_table(f'{project_id}.{dataset_id}.{table_id}')
    
    columns = [(field.name, field.field_type, field.description) for field in table_ref.schema]
    
    description = pd.DataFrame(columns, columns=['name','field_type','description'])
    
    return description

def get_table_size(
    dataset_id, 
    table_id, 
    billing_project_id, 
    project_id='basedosdados',
    info=False
):
    
    
    base_client = bigquery.Client(credentials=credentials(), project=project_id)
    
    user_client = bigquery.Client(credentials=credentials(), project=billing_project_id)
    
    table = base_client.get_table(f'{project_id}.{dataset_id}.{table_id}')
    
    
     
    query = f"""SELECT COUNT(*) FROM {project_id}.{dataset_id}.{table_id}"""
    
    job = user_client.query(query, location='US')
    
    num_rows = job.to_dataframe().loc[0,"f0_"]
    
    size_mb = round(job.total_bytes_processed/1024/1024, 2)
    
    
    
    table_data = pd.DataFrame([project_id], columns = ['project_id'])
    
    table_data['dataset_id'] = table.dataset_id
    
    table_data['table_id'] = table.table_id
    
    table_data['created_date'] = table.created.date()
    
    table_data['num_rows']=num_rows 
    
    table_data['size_mb' ]= size_mb

 
    return table_data
    
