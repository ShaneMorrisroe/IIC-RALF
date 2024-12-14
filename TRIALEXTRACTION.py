import re
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def parse_sky130_spice(file_path):
    nodes = {}
    components = []
    connections = defaultdict(list)

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('N'):  # Parse nodes
                match = re.match(r"N (\S+) (\S+) (\S+) (\S+) \{lab=(\S+)\}", line)
                if match:
                    x1, y1, x2, y2, label = match.groups()
                    nodes[label] = ((x1, y1), (x2, y2))  # Store node with label
            
            elif line.startswith('C'):  # Parse components
                match = re.match(
                    r"C \{([\w/.\-]+)\} (\S+) (\S+) (\S+) (\S+) \{(.+?)\}",
                    line
                )
                if match:
                    symbol, x, y, orientation, mirror, attributes = match.groups()
                    attr_dict = dict(
                        item.split('=') for item in attributes.split() if '=' in item
                    )
                    components.append({
                        "symbol": symbol,
                        "position": (x, y),
                        "orientation": orientation,
                        "mirror": mirror,
                        **attr_dict
                    })
                    # Map nodes to components if lab is present
                    if 'lab' in attr_dict:
                        connections[attr_dict['lab']].append(attr_dict['name'])

    return nodes, components, connections

def plot_schematic_with_layout(nodes, components, connections, output_file="schematic.png"):
    import networkx as nx
    import matplotlib.pyplot as plt

    # Create a NetworkX graph
    G = nx.Graph()

    # Add nodes to the graph
    for label, coords in nodes.items():
        G.add_node(label, type='node', coords=coords)

    # Add components to the graph
    for comp in components:
        G.add_node(comp['name'], type='component', symbol=comp['symbol'])

    # Add missing nodes from connections
    for label in connections:
        if label not in G:
            G.add_node(label, type='node')

    # Add connections as edges
    for label, comps in connections.items():
        for comp in comps:
            if label in G and comp in G:
                G.add_edge(label, comp)

    # Debug output
    print("Graph nodes:", G.nodes(data=True))
    print("Graph edges:", G.edges())

    # Generate a layout automatically
    pos = nx.spring_layout(G, seed=42)  # Use spring layout for automatic positioning

    # Draw the schematic
    plt.figure(figsize=(12, 10))

    # Draw edges first (to avoid overlap with nodes)
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7, edge_color="black")

    # Draw nodes
    node_positions = {n: pos[n] for n, d in G.nodes(data=True) if d.get('type', '') == 'node'}
    nx.draw_networkx_nodes(G, pos, nodelist=node_positions.keys(), node_size=500, node_color="skyblue", label="Nodes")
    nx.draw_networkx_labels(G, pos, labels={n: n for n in node_positions.keys()}, font_size=10)

    # Draw components
    component_positions = {n: pos[n] for n, d in G.nodes(data=True) if d.get('type', '') == 'component'}
    nx.draw_networkx_nodes(G, pos, nodelist=component_positions.keys(), node_size=800, node_color="lightgreen", label="Components")
    nx.draw_networkx_labels(G, pos, labels={n: n for n in component_positions.keys()}, font_size=8)

    # Add legend
    plt.legend(scatterpoints=1, loc="upper left", frameon=False)
    plt.title("Schematic Diagram")
    plt.axis("off")

    # Save the output
    plt.savefig(output_file, dpi=300)
    #plt.show()





# Example usage
if __name__ == "__main__":
    # Parse the SPICE file
    spice_file = "Circuits/Examples/InvAmp/InvAmp.sch"  # Replace with your SPICE file path
    nodes, components, connections = parse_sky130_spice(spice_file)

    # Plot and save the schematic
    plot_schematic_with_layout(nodes, components, connections, output_file="schematic.png")
