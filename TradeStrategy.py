from datetime import datetime
import backtrader as bt

class PriceMACross(bt.Strategy):
    """Price and SMA Cross Strategy"""
    params = (
        ('SMAPeriod', 26),  # SMA Period
    )

    def log(self, txt, dt=None):
        """Print a line with date to the console"""
        dt = bt.num2date(self.datas[0].datetime[0]) if dt is None else dt  # Specified date or the date of the current bar
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Print date and time with specified text to the console

    def __init__(self):
        """Initialize the trading strategy"""
        self.close = self.datas[0].close  # Close prices
        self.order = None  # Order
        self.sma = bt.indicators.SMA(self.datas[0], period=self.p.SMAPeriod)  # SMA

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
        self.order = None

    def notify_trade(self, trade):
        """Notify position status change"""
        if not trade.isclosed:
            return

        self.log(f'Trade Profit, Gross={trade.pnl:.2f}, NET={trade.pnlcomm:.2f}')
    
    def next(self):
        """Get the next bar"""
        self.log(f'Close={self.close[0]:.2f}')
        if self.order:
            return
        
        if not self.position:
            isSignalBuy = self.close[0] > self.sma[0]
            if isSignalBuy:
                self.log('Buy Market')
                self.order = self.buy()
        else:
            isSignalSell = self.close[0] < self.sma[0]
            if isSignalSell:
                self.log('Sell Market')
                self.order = self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(PriceMACross, SMAPeriod=26)
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
    brokerStartValue = cerebro.broker.getvalue()
    print(f'Initial capital: {brokerStartValue:.2f}')
    result = cerebro.run()
    brokerFinalValue = cerebro.broker.getvalue()
    print(f'Final capital: {brokerFinalValue:.2f}')
    print(f'Profit/Loss with commission: {(brokerFinalValue - brokerStartValue):.2f}')
    analysis = result[0].analyzers.TradeAnalyzer.get_analysis()
    print('Closed trades profit/loss:')
    print(f'- Without commission {analysis["pnl"]["gross"]["total"]:.2f}')
    print(f'- With commission  {analysis["pnl"]["net"]["total"]:.2f}')
    cerebro.plot()
