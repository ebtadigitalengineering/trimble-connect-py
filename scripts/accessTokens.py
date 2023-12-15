from TrimblePy.common.auth import Authentication
from TrimblePy.connect.file_api import TrimbleFileApi
from TrimblePy.connect.model_api import ModelApi
from TrimblePy.connect.model_api import Entity
from TrimblePy.topic.topics_api import TopicApi
import pandas as pd


auth = Authentication() # choose sql_available=True if you want to use ms sql server to store and retrieve tokens

auth.get_token()

df_tokens = auth.get_sql_tokens()