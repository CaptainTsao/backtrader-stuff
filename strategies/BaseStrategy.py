import backtrader as bt

import global_config

class BaseStrategy(bt.Strategy):

    def __init__(self):

        self.orders = dict()
        self.indicators = dict()
        self.brackets = dict()
        for d in self.datas:
            self.orders[d.params.name] = None
            self.indicators[d.params.name] = dict()

    def stop(self):
        for d in self.datas:
            self.close(data=d)

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date()
        t  = self.data.datetime.time()
        print('%s %s, %s' % (dt.isoformat(), t, txt))

    def add_indicator(self,data,name,ind,*args,**kwargs):
        self.indicators[data.params.name][name] = ind(data,*args,**kwargs)

    def get_indicator(self,data,name):
        return self.indicators[data.params.name][name]

    def do_sizing_simple(self,security_name, data):
        if global_config.GLOBAL_CONFIG == 'STOCK':
            leverage = self.broker.comminfo[None].params.leverage
            #return 100
            stocks = int(self.broker.getvalue() / len(self.datas) / data.close[0] * .9 * leverage)
            if stocks == 0:
                stocks = 1
            return stocks
        comminfo = self.broker.comminfo[security_name]
        margin = comminfo.margin
        mult = comminfo.params.mult
        max_contracts = int((self.broker.getvalue() / margin / len(self.datas))**(1.0 / 3.0))
        if max_contracts == 0:
            max_contracts = 1
        return max_contracts

    def close_open_orders(self, data):
        orders = self.orders[data.params.name]
        if orders is None:
            return
        for o in orders:
            self.cancel(o)
            self.log('Order cancelled')

    def record_bracket(self,bracket):
        # for brackets
        parent,stop,limit = bracket
        self.brackets[parent.ref] = [stop,limit]


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        security_name = order.params.data.params.name
        if order.status in [order.Completed]:
            if order.isbuy():
                pass
                self.log('{} BUY EXECUTED, {}'.format(security_name, order.executed.price))
            elif order.issell():
                pass
                self.log('{} SELL EXECUTED, {}'.format(security_name, order.executed.price))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled]:
            self.log('Order Canceled')
        elif order.status in [order.Margin]:
            self.log('Order Margin')
        elif order.status in [order.Rejected]:
            self.log('Order Rejected')

        if order.ref in self.brackets:
            #did we cancel the parent? if so we need to cancel the children
            if order.status in [order.Canceled, order.Margin, order.Rejected,order.Expired]:
                for o in self.brackets[order.ref]:
                    self.cancel(o)
                del self.brackets[order.ref]



        for k,v in self.orders.items():
            if v is None:
                continue
            if isinstance(v,list):
                for o in v:
                    if o.status not in [o.Canceled, o.Margin, o.Rejected, o.Completed, o.Expired]:
                        break
                else:
                    self.orders[k] = None
            elif v.status in [v.Canceled, v.Margin, v.Rejected, v.Completed, v.Expired]:
                self.orders[k] = None