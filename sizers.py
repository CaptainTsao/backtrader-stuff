import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os

class mySizer(bt.Sizer):

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        margin = comminfo.margin
        mult = comminfo.params.mult
        #atr = self.strategy.atr[0]
        max_contracts = int(self.broker.getvalue() / margin / len(self.strategy.datas) / 20)
        pos = abs(self.strategy.getposition(data).size)
        max_contracts = max(max_contracts,pos)

        prev_strength = self.strategy.get_indicator(data, 'strength')[-1]
        strength = self.strategy.get_indicator(data, 'strength')[0]
        new_pos_size = int(self.strategy.get_indicator(data, 'strength')[0] * max_contracts)

        if abs(new_pos_size) > abs(pos):
            pass
            #we need to make sure there's enough cash to increase our position size

        if pos == new_pos_size:
            ret = 0
        elif pos == 0:
            ret = new_pos_size
        elif new_pos_size == 0:
            ret = pos
        elif (pos >= 0 and new_pos_size >= 0) or (pos <= 0 and new_pos_size <= 0):
            ret = abs(pos) - abs(new_pos_size)
        elif (pos >= 0 and new_pos_size <= 0) or (pos <= 0 and new_pos_size >= 0):
            ret = abs(pos) + abs(new_pos_size)



        #
        if ret > max_contracts * 2:
            ret = max_contracts*2
        elif ret < -max_contracts * 2:
            ret = -max_contracts*2


        return ret