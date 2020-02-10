class PredictionInfo:
  def __init__(self, pred_id, user_id, time_stamp, prob, stype):
    self.pred_id = pred_id
    self.user_id = user_id
    self.time_stamp = time_stamp
    self.prob = prob
    self.stype = stype