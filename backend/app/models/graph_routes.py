# backend/app/models/graph_routes.py
import networkx as nx

def build_graph():
    G = nx.DiGraph()

    # (source, destination, price, distance)
    routes = [
        ("HYD", "DEL", 5000, 1250),
        ("HYD", "BOM", 4000, 700),
        ("BOM", "DEL", 3500, 1100),
        ("HYD", "GOI", 3000, 650),
        ("GOI", "DEL", 4500, 1500),
    ]

    for src, dst, price, dist in routes:
        G.add_edge(src, dst, price=price, distance=dist)

    return G
