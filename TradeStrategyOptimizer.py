from datetime import datetime
import backtrader as bt

class PriceMACross(bt.Strategy):
    """Price and SMA Cross Strategy"""
    params = (
        ('SMAPeriod', 26),  # SMA Period
        ('PrintLog', False),  # Print log to console
    )

    def log(self, txt, dt=None, doprint=False):
        """Print a line with date to the console"""
        if self.p.PrintLog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        """Initialize the trading strategy"""
        self.DataClose = self.datas[0].close
        self.Order = None  # Order
        self.sma = bt.indicators.SMA(self.datas[0], period=self.p.SMAPeriod)  # SMA
        self.brokerStartValue = self.broker.getvalue()  # Initial capital

    def notify_order(self, order):
        """Notify order status change"""
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'Bought @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
            elif order.issell():
                self.log(f'Sold @{order.executed.price:.2f}, Cost={order.executed.value:.2f}, Comm={order.executed.comm:.2f}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Canceled/Margin/Rejected')
        self.Order = None

    def notify_trade(self, trade):
        """Notify position status change"""
        if not trade.isclosed:
            return

        self.log(f'Trade Profit, Gross={trade.pnl:.2f}, NET={trade.pnlcomm:.2f}')
    
    def next(self):
        """Get the next bar"""
        self.log(f'Close={self.DataClose[0]:.2f}')
        if self.Order:
            return
        
        if not self.position:
            isSignalBuy = self.DataClose[0] > self.sma[0]
            if isSignalBuy:
                self.log('Buy Market')
                self.Order = self.buy()
        else:
            isSignalSell = self.DataClose[0] < self.sma[0]
            if isSignalSell:
                self.log('Sell Market')
                self.Order = self.sell()

    def stop(self):
        """End of the trading system"""
        self.log(f'SMA({self.p.SMAPeriod}), {(self.broker.getvalue() - self.brokerStartValue):.2f}', doprint=True)

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.optstrategy(PriceMACross, SMAPeriod=range(8, 65))
    data = bt.feeds.GenericCSVData(
        dataname='TQBR.SBER_D1.txt',
        separator='\t',
        dtformat='%d.%m.%Y %H:%M',
        openinterest=-1,
        fromdate=datetime(2019, 1, 1),
        todate=datetime(2021, 1, 1))
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='TradeAnalyzer')
    print('Account profit/loss:')
    results = cerebro.run()
    print('Closed trades profit/loss:')
    stats = {}
    for result in results:
        p = result[0].p.SMAPeriod
        analysis = result[0].analyzers.TradeAnalyzer.get_analysis()
        v = analysis['pnl']['net']['total']
        stats[p] = v
        print(f'SMA({p}), {v:.2f}')
    bestStat = max(stats.items(), key=lambda x: x[1])
    worstStat = min(stats.items(), key=lambda x: x[1])
    avgStat = sum(stats.values()) / len(stats.values())
    print(f'Best value: SMA({bestStat[0]}), {bestStat[1]:.2f}')
    print(f'Worst value: SMA({worstStat[0]}), {worstStat[1]:.2f}')
    print(f'Average value: {avgStat:.2f}')
