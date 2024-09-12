import plotly.graph_objects as go
import plotly.express as px
import networkx as nx

def create_source_distribution_chart(source_distribution):
    """
    Create a bar chart of intelligence source distribution.
    """
    fig = px.bar(
        x=list(source_distribution.keys()),
        y=list(source_distribution.values()),
        labels={'x': 'Intelligence Source', 'y': 'Count'},
        title='Distribution of Intelligence Sources'
    )
    return fig

def create_confidence_radar_chart(confidence_by_source):
    """
    Create a radar chart of confidence levels by intelligence source.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=list(confidence_by_source.values()),
        theta=list(confidence_by_source.keys()),
        fill='toself',
        name='Confidence Level'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3]
            )),
        showlegend=False,
        title='Average Confidence Level by Intelligence Source'
    )
    return fig

def create_importance_heatmap(importance_by_region):
    """
    Create a heatmap of importance levels by region.
    """
    fig = go.Figure(data=go.Heatmap(
        z=[list(importance_by_region.values())],
        x=list(importance_by_region.keys()),
        y=['Importance'],
        colorscale='Viridis'
    ))

    fig.update_layout(
        title='Average Importance by Region',
        xaxis_nticks=36
    )
    return fig

def create_intelligence_network():
    """
    Create a network graph of intelligence sources and their relationships.
    """
    G = nx.Graph()
    
    # Add nodes
    sources = ['OSINT', 'HUMINT', 'SIGINT', 'GEOINT', 'MASINT']
    G.add_nodes_from(sources)
    
    # Add edges (connections between sources)
    G.add_edge('OSINT', 'HUMINT', weight=0.7)
    G.add_edge('OSINT', 'GEOINT', weight=0.8)
    G.add_edge('HUMINT', 'SIGINT', weight=0.6)
    G.add_edge('SIGINT', 'GEOINT', weight=0.7)
    G.add_edge('GEOINT', 'MASINT', weight=0.5)
    G.add_edge('MASINT', 'SIGINT', weight=0.6)
    
    # Calculate node positions
    pos = nx.spring_layout(G)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create node trace
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=list(G.nodes()),
        textposition='top center',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=20,
            color=[],
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    # Color node points by the number of connections
    node_adjacencies = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))

    node_trace.marker.color = node_adjacencies

    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Network of Intelligence Sources',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig

if __name__ == "__main__":
    # Test visualization functions
    sample_source_distribution = {'OSINT': 30, 'HUMINT': 25, 'SIGINT': 20, 'GEOINT': 15, 'MASINT': 10}
    sample_confidence_by_source = {'OSINT': 2.1, 'HUMINT': 2.5, 'SIGINT': 2.3, 'GEOINT': 2.2, 'MASINT': 2.0}
    sample_importance_by_region = {'North America': 7, 'South America': 5, 'Europe': 8, 'Africa': 6, 'Asia': 9, 'Middle East': 8}

    create_source_distribution_chart(sample_source_distribution)
    create_confidence_radar_chart(sample_confidence_by_source)
    create_importance_heatmap(sample_importance_by_region)
    create_intelligence_network()
