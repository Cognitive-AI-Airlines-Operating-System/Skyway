# backend/app/api/optimized_route.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import networkx as nx

# ✅ FIXED IMPORT — use relative import (very important!)
from ..models.graph_routes import build_graph

router = APIRouter()

# Build the graph once when the module is imported
G = build_graph()

class RouteRequest(BaseModel):
    source: str
    destination: str
    optimize_for: str = "price"  # "price" or "distance"

@router.post("/optimized_route")
def optimized_route(req: RouteRequest):
    # Validate optimize_for
    if req.optimize_for not in ("price", "distance"):
        raise HTTPException(
            status_code=400,
            detail="optimize_for must be 'price' or 'distance'"
        )

    # Find shortest path based on the chosen weight
    try:
        path = nx.shortest_path(
            G,
            source=req.source,
            target=req.destination,
            weight=req.optimize_for,
        )
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No path found between given cities")
    except nx.NodeNotFound:
        raise HTTPException(status_code=400, detail="Invalid source or destination code")

    legs = []
    total_price = 0
    total_distance = 0

    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        data = G[u][v]  # edge attributes: {"price": ..., "distance": ...}

        legs.append({
            "from": u,
            "to": v,
            "price": data["price"],
            "distance": data["distance"]
        })

        total_price += data["price"]
        total_distance += data["distance"]

    return {
        "source": req.source,
        "destination": req.destination,
        "optimize_for": req.optimize_for,
        "path": path,
        "legs": legs,
        "total_price": total_price,
        "total_distance": total_distance,
    }
