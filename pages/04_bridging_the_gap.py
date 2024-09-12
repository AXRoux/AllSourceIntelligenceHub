import streamlit as st
from streamlit_extras.colored_header import colored_header
import networkx as nx
import plotly.graph_objects as go

st.set_page_config(page_title="Bridging the Gap", page_icon="🌉", layout="wide")

colored_header(
    label="Bridging the Gap: Analysts and Policymakers",
    description="Enhancing communication and understanding",
    color_name="violet-70"
)

st.markdown("""
One of the critical challenges in the intelligence community is effectively communicating complex analytical 
findings to policymakers. This page explores the barriers between analysts and policymakers and proposes 
strategies to bridge this gap.
""")

# Create a function to generate a network graph of communication challenges
def create_network_graph():
    G = nx.Graph()
    
    # Add nodes
    analysts = ["Intelligence Analyst", "Data Scientist", "OSINT Specialist", "HUMINT Officer", "SIGINT Analyst"]
    policymakers = ["Senior Policymaker", "Military Commander", "Diplomat", "Economic Advisor", "Security Advisor"]
    
    G.add_nodes_from(analysts, bipartite=0)
    G.add_nodes_from(policymakers, bipartite=1)
    
    # Add edges (connections)
    for analyst in analysts:
        for policymaker in policymakers:
            G.add_edge(analyst, policymaker)
    
    # Create positions for nodes
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
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            color=[],
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    # Color node points by number of connections
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f'{adjacencies[0]}<br># of connections: {len(adjacencies[1])}')

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Network of Analysts and Policymakers',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                            text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002 ) ],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig

st.plotly_chart(create_network_graph(), use_container_width=True)

st.markdown("""
The network graph above illustrates the complex web of communication between analysts and policymakers. 
Each node represents a role, and the connections show potential communication channels. The density of 
connections highlights the importance of effective information flow in the intelligence community.

### Key Challenges in Bridging the Gap:

1. **Technical Complexity**: Analysts often deal with highly technical information that may be difficult to 
   convey to non-specialists.

2. **Time Constraints**: Policymakers often need quick insights, while thorough analysis takes time.

3. **Different Priorities**: Analysts focus on accuracy and completeness, while policymakers need actionable insights.

4. **Communication Styles**: Analysts tend to be detail-oriented, while policymakers often prefer high-level summaries.

5. **Political Considerations**: Policymakers may have political considerations that influence how they interpret intelligence.

### Strategies for Improvement:

1. **Enhanced Training**: Provide analysts with training in effective communication and policymakers with 
   basic training in intelligence methodologies.

2. **Structured Analytical Techniques**: Use techniques like Analysis of Competing Hypotheses (ACH) to present 
   information in a clear, logical manner.

3. **Regular Briefings**: Establish regular, face-to-face briefings to build relationships and trust.

4. **Tailored Reports**: Create intelligence products tailored to the specific needs and preferences of different policymakers.

5. **Feedback Loops**: Implement systems for policymakers to provide feedback on the utility and clarity of intelligence products.

6. **Visualization Tools**: Utilize data visualization and interactive tools to present complex information more intuitively.

7. **Embedded Analysts**: Consider embedding analysts within policymaking teams for direct, real-time support.

By implementing these strategies, the intelligence community can work towards more effective communication, 
ensuring that critical insights reach policymakers in a timely and actionable manner.
""")

if __name__ == "__main__":
    st.write("Bridging the Gap page loaded successfully.")
