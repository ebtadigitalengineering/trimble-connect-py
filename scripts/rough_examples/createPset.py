from TrimblePy.common.auth import Authentication
from TrimblePy.connect.file_api import TrimbleFileApi
from TrimblePy.org.org_api import OrgApi
from TrimblePy.pset.pset_api import PsetApi
from multiprocessing import Pool
import pandas as pd
from tqdm import tqdm

auth = Authentication(sql_available=True, token_retrieval_method="env")
access_token, refresh_token = auth.get_token()

# access_token, refresh_token = auth.get_token()
file_api = TrimbleFileApi(authentication=auth)
projects = file_api.get_projects()
project_id = projects[0]["id"]
org_api = OrgApi(authentication=auth, project_id=project_id)
pset_api = PsetApi(authentication=auth, project_id=project_id)
forestId = f"project:{project_id}:data"  # frn notation for project data forest
discovery_trees = org_api.get_discovery_trees(forestId)
treeId = discovery_trees["items"][0]["id"]
nodes = org_api.get_nodes(forestId, treeId)
nodeId = nodes["items"][0]["id"]
node = org_api.get_node(forestId, treeId, nodeId)

# The shortcute to this is forestId, 'ProjectContext', 'PSetLibs'
node = org_api.get_node(f"project:{project_id}:data", "ProjectContext", "PSetLibs")


data = {
    "name": "Cost Codes",
    "types": [],
    "i18n": {},
    "schema": {
        "open": True,
        "props": {
            "CostRef": {
                "type": "string",
                "description": "Name of element in cost planning system",
            },
            "CostMaterial": {
                "type": "string",
                "description": "Material described in cost planning system",
            },
            "CostElements": {
                "type": "string",
                "description": "Cost elements in cost planning system",
            },
        },
    },
}

data = {
    "schema" : {
        "open": True,
        "props": {}
    }
}

lib = pset_api.create_library(data)
lib_defs = pset_api.get_lib_defs(lib['id'])
pset = pset_api.create_pset(data,lib['id'])

data_element = {
    "props": {
        "CostRef": "Abutment Pile Cap-South Abutment -  -",
        "CostMaterial": "butment Pile 40 MPa Concrete",
        "CostElements": "eXAMPLE1,EXAMPLE2,EXAMPLE3",
    }
}

guid = "2sANVLFdHnSVhEdM$G2mvF"
model_id = "qTWkQ-M52Fw"

update = pset_api.update_pset(data_element,lib['id'],pset['id'],guid,modelId=model_id,new=True)