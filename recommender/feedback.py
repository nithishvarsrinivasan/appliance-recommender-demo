
from collections import defaultdict
class FeedbackStore:
    def __init__(self):
        self.totals = defaultdict(lambda: {"helpful":0,"not_helpful":0})
        self.last = None
    def add(self, user_id, appliance, recommended_model, helpful: bool):
        key = (user_id, appliance, recommended_model)
        if helpful: self.totals[key]["helpful"] += 1
        else: self.totals[key]["not_helpful"] += 1
        self.last = {"user_id":user_id,"appliance":appliance,"recommended_model":recommended_model,"helpful":helpful}
        return self.totals[key]
    def stats_for(self, user_id, appliance, recommended_model):
        key = (user_id, appliance, recommended_model)
        return self.totals.get(key, {"helpful":0,"not_helpful":0})
