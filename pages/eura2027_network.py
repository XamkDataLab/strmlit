import streamlit as st
import pandas as pd
import networkx as nx
import textwrap
import json  
from pyvis.network import Network
import streamlit.components.v1 as components
from queries import fetch_collaboration_data

data = fetch_eura2027_collab()
