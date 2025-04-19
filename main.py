from flask import Flask, request, jsonify
from itertools import permutations

app = Flask(__name__)

# Product data: "product": (center, weight)
product_data = {
    "A": ("C1", 3), "B": ("C1", 2), "C": ("C1", 8),
    "D": ("C2", 12), "E": ("C2", 25), "F": ("C2", 15),
    "G": ("C3", 0.5), "H": ("C3", 1), "I": ("C3", 2)
}

# Distance data (bidirectional)
distances = {
    ("C1", "L1"): 3, ("C2", "L1"): 2.5, ("C3", "L1"): 2,
    ("C1", "C2"): 4, ("C2", "C3"): 3, ("C1", "C3"): 7
}
# Make bidirectional
for (a, b), d in list(distances.items()):
    distances[(b, a)] = d

def get_distance(a, b):
    return distances.get((a, b)) or distances.get((b, a))

def cost_per_distance(weight):
    if weight <= 5:
        return 10
    extra = weight - 5
    return 10 + (int((extra + 4.9999) // 5)) * 8

def group_products_by_center(order):
    grouped = {"C1": [], "C2": [], "C3": []}
    for prod, qty in order.items():
        if prod not in product_data:
            raise ValueError(f"Product {prod} not found.")
        center, weight = product_data[prod]
        grouped[center].append((prod, qty, weight))
    return grouped

def generate_sequences(start, centers):
    centers = list(set(centers))
    centers.remove(start)
    all_routes = []
    for perm in permutations(centers):
        route = [start]
        for c in perm:
            route += ["L1", c]
        route.append("L1")
        all_routes.append(route)
    return all_routes

def calculate_route_cost(route, grouped):
    total_cost = 0.0
    carried_items = []

    for i in range(1, len(route)):
        from_loc, to_loc = route[i - 1], route[i]

        if from_loc in grouped:
            for _, qty, wt in grouped[from_loc]:
                carried_items += [(wt, from_loc)] * qty

        weight = sum(w for w, _ in carried_items)
        per_unit = cost_per_distance(weight)
        total_cost += get_distance(from_loc, to_loc) * per_unit

        if to_loc == "L1":
            carried_items = []

    return total_cost

def compute_min_cost(order):
    grouped = group_products_by_center(order)
    centers = [c for c, items in grouped.items() if items]
    min_cost = float("inf")

    for start in centers:
        routes = generate_sequences(start, centers)
        for route in routes:
            cost = calculate_route_cost(route, grouped)
            if cost < min_cost:
                min_cost = cost

    return min_cost

@app.route('/calculate-cost', methods=['POST'])
def calculate():
    try:
        order = request.get_json()
        min_cost = compute_min_cost(order)
        return jsonify({"minimum_cost": round(min_cost, 2)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
