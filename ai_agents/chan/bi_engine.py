class BiEngine:

    def __init__(self):
        pass

    # ==================================================

    def build_bi(self, pivots):
        pivot_highs = pivots["pivot_highs"]
        pivot_lows = pivots["pivot_lows"]

        all_points = []

        for p in pivot_highs:
            all_points.append({
                "type": "HIGH",
                "index": p["index"],
                "price": p["price"]
            })

        for p in pivot_lows:
            all_points.append({
                "type": "LOW",
                "index": p["index"],
                "price": p["price"]
            })

        all_points = sorted(all_points, key=lambda x: x["index"])

        bis = []

        for i in range(1, len(all_points)):
            prev_point = all_points[i - 1]
            current_point = all_points[i]

            if prev_point["type"] == current_point["type"]:
                continue

            direction = "UP"
            if current_point["price"] < prev_point["price"]:
                direction = "DOWN"

            bis.append({
                "direction": direction,
                "start_index": prev_point["index"],
                "end_index": current_point["index"],
                "start_price": prev_point["price"],
                "end_price": current_point["price"]
            })

        return bis