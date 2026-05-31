class SegmentEngine:

    def __init__(self):
        pass

    # ==================================================

    def detect_segments(self, bis):
        if len(bis) < 3:
            return {
                "trend": "RANGE"
            }

        recent = bis[-3:]

        up_count = 0
        down_count = 0

        for b in recent:
            if b["direction"] == "UP":
                up_count += 1
            else:
                down_count += 1

        if up_count >= 2:
            return {
                "trend": "BULL"
            }

        if down_count >= 2:
            return {
                "trend": "BEAR"
            }

        return {
            "trend": "RANGE"
        }