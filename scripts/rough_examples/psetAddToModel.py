from TrimblePy.common.auth import Authentication
from TrimblePy.connect.file_api import TrimbleFileApi
from TrimblePy.org.org_api import OrgApi
from TrimblePy.pset.pset_api import PsetApi
from multiprocessing import Pool
import pandas as pd
from tqdm import tqdm

auth = Authentication(sql_available=True, token_retrieval_method="web")
access_token, refresh_token = auth.get_token()

# access_token, refresh_token = auth.get_token()
file_api = TrimbleFileApi(authentication=auth)
projects = file_api.get_projects()
project_id = projects[0]["id"]
org_api = OrgApi(authentication=auth, project_id=project_id)
forestId = f"project:{project_id}:data" # frn notation for project data forest

discovery_trees = org_api.get_discovery_trees(forestId)

treeId = discovery_trees["items"][0]["id"]

# OPTIONAL - get the tree
# tree = org_api.get_discovery_tree(forestId, treeId)

nodes = org_api.get_nodes(forestId, treeId)

nodeId = nodes["items"][0]["id"]

node = org_api.get_node(forestId, treeId, nodeId)

libIds = node["links"]
libIds = [libId.split(":")[2] for libId in libIds]

pset_api = PsetApi(authentication=auth, project_id=project_id)

lib_defs = pset_api.get_lib_defs(libIds[1])

# model : muNzZTCddJc
#  frn:tcfile:muNzZTCddJc
encoded = pset_api.encoder("frn:tcfile:10JE00DN")

df = pset_api.prop_set_table(lib_defs)
df['ref_name'] = ['SOL_Volume','NEL_Volume','TRIM_Volume','vol_flag']



table_name = "Geometry_Consolidated"
geo = auth.get_sql_table(table_name)
vol = geo[
    [
        "GUID",
        "idx",
        "ifc_type",
        "name",
        "versionId",
        "model_name",
        "model_id",
        "NEL_Volume",
        "TRIM_Volume",
        "SOL_Volume",
        "vol_flag",
    ]
]

vol = vol[vol.model_name.str.contains('BDT')]

def convert_to_float(x):
    try:
        return float(x)
    except:
        return None

def null_to_negative_9999999(x):
    if x is None:
        return -99999.999
    else:
        return x

vol[['NEL_Volume','TRIM_Volume','SOL_Volume']] = vol[['NEL_Volume','TRIM_Volume','SOL_Volume']].applymap(convert_to_float)
vol[['NEL_Volume','TRIM_Volume','SOL_Volume']] = vol[['NEL_Volume','TRIM_Volume','SOL_Volume']].applymap(null_to_negative_9999999)

# vol flag is red if - (NEL_Volume - TRIM_Volume)/NEL_Volume > 0.01, or if NEL_Volume is null
vol['vol_flag'] = vol.apply(lambda x: 'r' if (x['NEL_Volume'] is None or (x['NEL_Volume'] - x['TRIM_Volume'])/x['NEL_Volume'] > 0.01) else 'g', axis=1)

defs = lib_defs['items'][0].get('i18n').get('en-US').get('props')

vol.rename(columns={'SOL_Volume':'Solibri Volume','NEL_Volume':'NEL_Volume','TRIM_Volume':'Trimble Volume', 'vol_flag':'Flag'}, inplace=True)
vol['Flag'] = vol['Flag'].apply(lambda x: True if x == 'r' else False)

vol.rename(columns={v:k for k,v in defs.items()}, inplace=True)


vol.reset_index(drop=True,inplace=True)
one = vol.loc[0]
props = one[[x for x in one.index if x in defs.keys()]].to_dict()

model_id = one['model_id']
version_id = one['versionId']
object_id = one['GUID']
libid = libIds[1]
defId = lib_defs['items'][0]['id']

pset_update_object = {
    "props": props,
}

update = pset_api.update_pset(pset_update_object, libid, defId, object_id, new=True)