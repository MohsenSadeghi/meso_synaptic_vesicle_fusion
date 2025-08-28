import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import networkx as nx
import numpy as np


def hex_to_rgb(hex_color):
    """
    Convert a hex color string to an (R, G, B) tuple.

    Parameters:
        hex_color (str): Hex color string, e.g., '#FF5733' or 'FF5733'

    Returns:
        tuple: (R, G, B) where each component is in [0, 255]
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Hex color must be 6 characters long.")
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def draw_bezier_arrow(ax, start, end, angle_start_deg, angle_end_deg, radius=1.0, arrow=True, color='black', lw=2):
    """
    Draws a cubic Bezier curve between start and end, with control over tangents via angles and radius.
    """
    # Convert angles to radians
    angle_start = np.radians(angle_start_deg)
    angle_end = np.radians(angle_end_deg)

    # Compute control points
    ctrl1 = (
        start[0] + radius * np.cos(angle_start),
        start[1] + radius * np.sin(angle_start)
    )
    ctrl2 = (
        end[0] - radius * np.cos(angle_end),
        end[1] - radius * np.sin(angle_end)
    )

    # Define the path
    path_data = [
        (Path.MOVETO, start),
        (Path.CURVE4, ctrl1),
        (Path.CURVE4, ctrl2),
        (Path.CURVE4, end)
    ]
    path = Path([pt for (_, pt) in path_data], [code for (code, _) in path_data])

    patch = PathPatch(path, facecolor='none', edgecolor=color, lw=lw)
    ax.add_patch(patch)

    # Draw arrowhead if desired
    if arrow:
        # Arrowhead at end direction
        delta = np.array(end) - np.array(ctrl2)
        angle = np.arctan2(delta[1], delta[0])
        head_length = 0.13 * radius
        
        ax.arrow(end[0] - 1.5 * head_length * np.cos(angle), end[1] - 1.5 * head_length * np.sin(angle),
                 1.5 * head_length * np.cos(angle), 1.5 * head_length * np.sin(angle),
                 head_width=0.8 * head_length, head_length=head_length,
                 fc=color, ec='none')


def draw_self_loop(ax, pos, node, direction=1.0, radius=0.3, angle=90, arrowstyle='fancy', color='black', label=None):
    """
    Draw a self-loop at a node position using FancyArrowPatch.
    """
    x, y = pos[node]

    angle_A, angle_B = 120, -120

    if direction < 0:
        angle_A, angle_B = 60, -60
        
    draw_bezier_arrow(ax, (x - 0.1, y +  direction * 0.12), (x + 0.1, y + direction * 0.17),
                      angle_A, angle_B,
                      radius * direction, color=color, lw=2.5)


def timescale_label(timescale):

    if timescale < 1.0e-6:
        return " Stable"
    elif timescale < 0.5:
        return rf"{timescale * 1.0e3:.0f} $\mu$s"
    else:
        return rf"{timescale:.1f} ms"

        
def visualize_markov_chain(P, dt, node_positions=None, use_timescale_instead_of_probabilities=False,
                           threshold=1.0e-6, labels=None, node_color=None):
    """
    Visualize a Markov chain given its transition matrix P.
    Arrows with probabilities below `threshold` are not shown.
    """
    N = P.shape[0]
    G = nx.MultiDiGraph()

    if node_positions is not None:
        pos = node_positions
    else:
        pos = {}
    
    node_size = 2000
    
    if labels is None:
        labels = {i: f"State {i+1}" for i in range(N)}

    if node_color is None:
        node_color = 'lightblue'

    max_y = 0.0
    
    # Position nodes in a line
    for i in range(N):
        
        G.add_node(i)

        if node_positions is None:
            pos[i] = (i, 0)
        else:
            max_y = max(np.abs(pos[i][0]), max_y)
    
    # Add edges with labels
    forward_edge_labels = {}
    backward_edge_labels = {}
    self_loop_labels = {}
    
    for i in range(N):
        for j in range(N):
            prob = P[i, j]
    
            transition_rate = -np.log(1.0 - prob) / dt if prob < 1.0 else np.inf
            time_scale = 1.0 / (transition_rate + 1.0e-16)
            
            if prob > threshold:
                
                G.add_edge(i, j)
                
                if use_timescale_instead_of_probabilities:
                    _label  = timescale_label(time_scale)# if transition_rate < -np.log(1.0e-24) / dt else r"$\infty$"
                else:
                    _label = f"{prob:.2f}"

                self_loop_labels[(i, j)] = ""
                forward_edge_labels[(i, j)] = ""
                backward_edge_labels[(i, j)] = ""
                    
                if i == j:
                    self_loop_labels[(i, j)] = _label
                elif j > i:
                    forward_edge_labels[(i, j)] = _label
                else:
                    backward_edge_labels[(i, j)] = _label

    # Draw nodes
    fig, ax = plt.subplots(figsize=(2.0 * N, 3.5  + 0.45 * max_y))
    
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=24, font_weight="bold", font_color="white")

    # Draw edges
    curved_edges = [(i, j) for (i, j) in G.edges() if i != j]
    self_loops = [(i, j) for (i, j) in G.edges() if i == j]

    arrow_style_1 = "fancy, tail_width=0.2, head_length=0.7, head_width=0.4"
    arrow_style_2 = "-|>, head_length=0.5, head_width=0.2"
    arrow_color = 'xkcd:gray'
    
    nx.draw_networkx_edges(G, pos, edgelist=curved_edges, edge_color=arrow_color, width=2.5, ax=ax, min_target_margin=15,
                           connectionstyle='arc3, rad=0.3', arrows=True, alpha=1, arrowstyle=arrow_style_2,
                           arrowsize=15, node_size=node_size)
    
    # Draw edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=forward_edge_labels, 
                                 label_pos=0.5, font_color='xkcd:gray',
                                 font_size=14, rotate=True, clip_on=False, verticalalignment='top',
                                 bbox=dict(boxstyle="round,pad=0.1", fc="none", ec="none"))

    nx.draw_networkx_edge_labels(G, pos, edge_labels=backward_edge_labels, 
                                 label_pos=0.5, font_color='xkcd:gray',
                                 font_size=14, rotate=True, clip_on=False, verticalalignment='bottom',
                                 bbox=dict(boxstyle="round,pad=0.1", fc="none", ec="none"))
    
    for (i, j) in self_loops:
        x, y = pos[i]
        upside = np.sign(y + 0.1)
        
        draw_self_loop(ax, pos, node=i, direction=upside, radius=0.6, arrowstyle=arrow_style_2, color=arrow_color)
        
        offset = 0.2 if upside > 0.0 else -0.45
        rotation = 90 if upside > 0.0 else 270
        
        plt.text(x, y + offset, self_loop_labels[(i, j)],
                 fontsize=14, color='xkcd:gray',
                 bbox=dict(boxstyle="round,pad=0.1", fc="none", ec="none"),
                 horizontalalignment='center', rotation=90)
        
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return fig
