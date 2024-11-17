from Bio import Entrez, SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import streamlit as st

# Set up Entrez email
Entrez.email = "farishahainzatulhusna@graduate.utm.my"

# Function to retrieve protein data based on Uniprot ID
def retrieve_data(protein_id):
    try:
        # Fetch data from Entrez
        handle = Entrez.efetch(db='protein', id=protein_id, rettype='fasta', retmode='text')
        record = SeqIO.read(handle, 'fasta')
        return record
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to analyze protein sequence
def get_basic_analysis(sequence):
    seq_analysis = ProteinAnalysis(str(sequence))
    amino_acid_composition = seq_analysis.count_amino_acids()
    molecular_weight = seq_analysis.molecular_weight()
    isoelectric_point = seq_analysis.isoelectric_point()
    return {
        "length": len(sequence),
        "amino_acid_composition": amino_acid_composition,
        "molecular_weight": molecular_weight,
        "isoelectric_point": isoelectric_point,
    }

# Streamlit Interface
st.title('Lab 1 - FARISHAH AINZATUL HUSNA BINTI ALIAS')

# Input field and button for Uniprot ID
protein_id = st.text_input('Enter Uniprot ID')
retrieve = st.button('Retrieve')

# Actions when 'Retrieve' is clicked
if retrieve:
    if protein_id:
        # Fetch protein data
        protein_record = retrieve_data(protein_id)
        
        if protein_record:
            # Display basic information about the protein
            st.write("### Protein Information")
            st.write(f"**Description:** {protein_record.description}")
            st.write(f"**Name:** {protein_record.name}")
            st.write(f"**Protein Sequence (first 60 characters):** {protein_record.seq[:60]}...")
            st.write(f"**Sequence Length:** {len(protein_record.seq)}")

            # Perform analysis
            analysis = get_basic_analysis(protein_record.seq)

            # Display analysis results
            st.write("### Protein Analysis")
            st.write("**Amino Acid Composition:**")
            st.write(analysis["amino_acid_composition"])
            st.write(f"**Molecular Weight:** {analysis['molecular_weight']:.2f}")
            st.write(f"**Isoelectric Point:** {analysis['isoelectric_point']:.2f}")
    else:
        st.warning('Please enter a Uniprot ID')
