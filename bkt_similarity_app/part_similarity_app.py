import pandas as pd
import streamlit as st
# import matplotlib.pyplot as plt
import plotly.express as px
from scipy.spatial.distance import cdist

import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def find_closest_parts(df, selected_part, top_n=5):
    selected_coords = df[df['PART_NO'] == selected_part][['PC1', 'PC2']].values

    distances = cdist(selected_coords, df[['PC1', 'PC2']].values, metric='euclidean')[0]
    df['Distance'] = distances

    closest_parts = df[df['PART_NO'] != selected_part].nsmallest(top_n, 'Distance')
    return closest_parts

# def plot_map(df, selected_part=None, closest_parts=None):
#     plt.figure(figsize=(10, 10))
#     plt.scatter(df['PC1'], df['PC2'], alpha=0.6, label='Parts')

#     if selected_part:
#         selected_coords = df[df['PART_NO'] == selected_part][['PC1', 'PC2']].values[0]
#         plt.scatter(*selected_coords, color='red', label=f'Selected Part: {selected_part}', s=200, marker='X')

#         for _, part in closest_parts.iterrows():
#             plain_part_no = part['PART_NO'].split(">")[-2].split("<")[0]  # Extract the plain part number
#             plt.scatter(part['PC1'], part['PC2'], color='green', label=f"Similar: {plain_part_no}", s=150)
            

#     plt.title('Part Map (PCA Reduced)')
#     # plt.xlabel('PC1')
#     # plt.ylabel('PC2')
#     plt.legend()
#     st.pyplot(plt.gcf())

def plot_map(df, selected_part=None, closest_parts=None):
    # Create the scatter plot with only the part number in the tooltip
    fig = px.scatter(
        df, 
        x='PC1', 
        y='PC2', 
        hover_name='PART_NO',  # Use hover_name to show only the part number
        title='Part Map (PCA Reduced)',
        width=800, 
        height=800,
        opacity=0.3
    )

    # Customize the layout to hide axis titles and tick labels
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        xaxis_showticklabels=False,
        yaxis_showticklabels=False
    )

    if selected_part:
        selected_coords = df[df['PART_NO'] == selected_part][['PC1', 'PC2']].values[0]
        fig.add_scatter(
            x=[selected_coords[0]], 
            y=[selected_coords[1]], 
            mode='markers',
            marker=dict(size=20, color='red',symbol='x'), 
            name=f'Selected: {selected_part}',
            hovertext=selected_part,
            opacity=1.0
        )

        for _, part in closest_parts.iterrows():
            fig.add_scatter(
                x=[part['PC1']], 
                y=[part['PC2']], 
                mode='markers', 
                marker=dict(size=12, color='green', symbol='circle'), 
                name=f'Similar: {part["PART_NO"]}', 
                hovertext=part['PART_NO']
            )
        
        # Automatically adjust zoom to the selected part
        padding = 0.8  # Adjust padding as needed
        x_min = selected_coords[0] - padding
        x_max = selected_coords[0] + padding
        y_min = selected_coords[1] - padding
        y_max = selected_coords[1] + padding
        fig.update_xaxes(range=[x_min, x_max])
        fig.update_yaxes(range=[y_min, y_max])

    # Update traces to only show the part number on hover
    fig.update_traces(hovertemplate="%{hovertext}")

    st.plotly_chart(fig)

def make_link(part_no):
    url = f"{part_no}"
    return f'<a href="{url}" target="_blank">{part_no}</a>'

def main():
    st.title("Bracket Similarity Map")

    dataset_options = {
        "All predictors": "model.csv",
        "Only Area & Volume": "model2.csv"
    }
    selected_label = st.selectbox("Select model to use:", list(dataset_options.keys()))
    selected_file = dataset_options[selected_label]

    uploaded_file = resource_path(selected_file)
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        selected_part = st.selectbox("Select a part to find similar ones:", ["Select a part"] + list(df['PART_NO'].unique()), index=0)
        top_n = st.slider("Number of similar parts to show:", 1, 20, 5)
        
        if selected_part != "Select a part":

            closest_parts = find_closest_parts(df, selected_part, top_n)

            selected_part_df = df[df['PART_NO'] == selected_part]
            # selected_part_df['PART_NO'] = selected_part_df['PART_NO'].apply(make_link)
            st.markdown(selected_part_df[[col for col in df.columns if col not in ['PC1', 'PC2','Distance']]].to_html(escape=False, index=False), unsafe_allow_html=True)

            # closest_parts['PART_NO'] = closest_parts['PART_NO'].apply(make_link)
            st.write(f"Top {top_n} similar parts to {selected_part}:")

            st.markdown(closest_parts[[col for col in df.columns if col not in ['PC1', 'PC2']]].to_html(escape=False, index=False), unsafe_allow_html=True)

            plot_map(df, selected_part, closest_parts)


if __name__ == "__main__":
    main()

