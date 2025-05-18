using QuantConnect;
using QuantConnect.Algorithm;
using QuantConnect.Brokerages;
using QuantConnect.Data;
using QuantConnect.Indicators;
using QuantConnect.Orders;

namespace QuantConnect.Algorithm.CSharp
{
    public class BinanceMovingAverageCrossover : QCAlgorithm
    {
        private Symbol _symbol;
        private SimpleMovingAverage _fastSMA;
        private SimpleMovingAverage _slowSMA;
        private int _fastPeriod = 50;
        private int _slowPeriod = 200;

        public override void Initialize()
        {
            // 1. Set start/end dates only for backtesting; ignore for live
            SetStartDate(2025, 1, 1);
            SetEndDate(2025, 6, 1);
            SetAccountCurrency("USDT",50);
            SetCash("USDT",50);
           


            // 2. Add the crypto pair on Binance spot
            _symbol = AddCrypto("BTCUSDT", Resolution.Minute, Market.Binance).Symbol;

            // 3. Create the fast and slow SMA indicators
            _fastSMA = SMA(_symbol, _fastPeriod, Resolution.Minute);
            _slowSMA = SMA(_symbol, _slowPeriod, Resolution.Minute) ;

            // 4. Warm up so we have enough history
            SetWarmUp(_slowPeriod + 10, Resolution.Minute);

            // 5. Use the Binance brokerage model in live
            SetBrokerageModel(BrokerageName.Binance, AccountType.Cash);

        }

        public override void OnData(Slice data)
        {
            if (IsWarmingUp) return;

            var price = data[_symbol].Close;
            var fast = _fastSMA.Current.Value;
            var slow = _slowSMA.Current.Value;
            var holdings = Portfolio[_symbol].Quantity;
            var holding_value = holdings * price;

            // Entry: fast crosses above slow
            if (fast > slow && holding_value <= 10)
            {
                SetHoldings(_symbol, 1m);
                //Debug($"BUY  >> Price: {price:F2}, FastSMA: {fast:F2}, SlowSMA: {slow:F2}");
            }
            // Exit: fast crosses below slow
            else if (fast < slow && holding_value > 10)
            {
                Liquidate(_symbol);
                //Debug($"SELL >> Price: {price:F2}, FastSMA: {fast:F2}, SlowSMA: {slow:F2}");
            }
        }

        public override void OnEndOfDay()
        {
            Log($"EOD {Time:yyyy-MM-dd} • Price={Securities[_symbol].Price:F2} • FastSMA={_fastSMA.Current.Value:F2} • SlowSMA={_slowSMA.Current.Value:F2}");
        }
    }
}
