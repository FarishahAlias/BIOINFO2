#FARISHAH AINZATUL HUSNA BINTI ALIAS 
# #A22EC0160
import requests
import pandas as pd
import networkx as nx
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

def retrieve_ppi_biogrid(target_protein):
    biogrid_url = "https://webservice.thebiogrid.org/interactions"
    params = {
        "accessKey": "c376bd6dcedfb9c1edb48006d35c939d",
        "format": "json",
        "searchNames": True,
        "geneList": target_protein,
        "organism": 9606,
        "searchbiogridids": True,
        "includeInteractors": True
    }
    response = requests.get(biogrid_url, params=params)
    network = response.json()
    
    # Convert the JSON data to DataFrame
    network_df = pd.DataFrame.from_dict(network, orient='index')
    network_df['OFFICIAL_SYMBOL_A'] = network_df['OFFICIAL_SYMBOL_A'].str.upper()
    network_df['OFFICIAL_SYMBOL_B'] = network_df['OFFICIAL_SYMBOL_B'].str.upper()
    
    return network_df


def retrieve_ppi_string(target_protein):
    string_url = "https://string-db.org/api/json/network"
    params = {
        "identifiers": target_protein,
        "species": 9606
    }
    response = requests.get(string_url, params=params)
    network = response.json()
    
    # Convert the JSON data to DataFrame
    network_df = pd.json_normalize(network)
    network_df['preferredName_A'] = network_df['preferredName_A'].str.upper()
    network_df['preferredName_B'] = network_df['preferredName_B'].str.upper()
    
    return network_df

def generate_network(dataframe):
    # Check if required columns are present in the DataFrame
    if 'OFFICIAL_SYMBOL_A' in dataframe.columns and 'OFFICIAL_SYMBOL_B' in dataframe.columns:
        network_graph = nx.from_pandas_edgelist(dataframe, "OFFICIAL_SYMBOL_A", "OFFICIAL_SYMBOL_B")
    elif 'preferredName_A' in dataframe.columns and 'preferredName_B' in dataframe.columns:
        network_graph = nx.from_pandas_edgelist(dataframe, "preferredName_A", "preferredName_B")
    else:
        # If columns for edges are not found, show an error message in Streamlit
        st.error("Column names for edges not found in DataFrame.")
        return None, {}

    # Extract graph details
    graph_details = {
        "Number of edges": network_graph.number_of_edges(),
        "Number of nodes": network_graph.number_of_nodes()
    }

    return network_graph, graph_details

def get_centralities(network_graph):
    # Calculate various centrality measures
    degree_centrality = nx.degree_centrality(network_graph)
    betweenness_centrality = nx.betweenness_centrality(network_graph)
    closeness_centrality = nx.closeness_centrality(network_graph)
    eigenvector_centrality = nx.eigenvector_centrality(network_graph)
    page_rank_centrality = nx.pagerank(network_graph)
    
    # Return all centrality measures in a dictionary
    centralities = {
        'Degree Centrality': degree_centrality,
        'Betweenness Centrality': betweenness_centrality,
        'Closeness Centrality': closeness_centrality,
        'Eigenvector Centrality': eigenvector_centrality,
        'PageRank Centrality': page_rank_centrality
    }
    
    return centralities

import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx


st.title("Protein-Protein Interaction Network Analysis")

# User input for protein ID and database selection
target_protein = st.text_input("Enter Protein ID (e.g., TP53):")
database = st.radio("Select Database:", ("BioGRID", "STRING"))

if st.button("Retrieve PPI Data"):
    if target_protein:
        # Retrieve PPI data based on the selected database
        if database == "BioGRID":
            ppi_data = retrieve_ppi_biogrid(target_protein)
        elif database == "STRING":
            ppi_data = retrieve_ppi_string(target_protein)
        
        # Display PPI data
        st.subheader("PPI Data Information")
        st.write(ppi_data)
        
        # Generate network graph and details
        network_graph, graph_details = generate_network(ppi_data)
        
       
        if network_graph:
            # Display network details
            st.write(f"Number of Edges: {graph_details['Number of edges']}")
            st.write(f"Number of Nodes: {graph_details['Number of nodes']}")
            
            # Network visualization
            st.subheader("Network Visualization")
            plt.figure(figsize=(10, 10))
            nx.draw(network_graph, with_labels=True, node_size=50, node_color='lightblue')
            plt.title(f"Protein Interaction Network for {target_protein}")
            st.pyplot()

            # Calculate centralities
            centralities = get_centralities(network_graph)

            # Display centralities
            st.subheader("Centrality Measures")
            for measure, values in centralities.items():
                st.write(f"{measure}:")
                st.write(values)

        else:
            st.error("Failed to generate network graph.")
    else:
        st.error("Please enter a protein ID.")