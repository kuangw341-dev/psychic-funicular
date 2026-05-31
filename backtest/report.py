# V50_CORE/backtest/report.py

class Report:

    def __init__(self):
        pass

    # ==================================================
    # Generate Report
    # ==================================================

    def generate(self, final_balance, total_trades, winrate, profit_factor, max_drawdown, total_profit, total_loss, sharpe_ratio, sortino_ratio, expectancy, recovery_factor, monte_carlo, regime_analysis, agent_analysis, shadow_analysis):
        report = f"""

================================
V50 FINAL REPORT
================================

最终余额:
{round(final_balance, 2)}

总交易:
{total_trades}

胜率:
{round(winrate, 2)}%

Profit Factor:
{round(profit_factor, 2)}

最大回撤:
{round(max_drawdown, 2)}%

总盈利:
{round(total_profit, 2)}

总亏损:
{round(total_loss, 2)}

================================
RISK METRICS
================================

Sharpe Ratio:
{sharpe_ratio}

Sortino Ratio:
{sortino_ratio}

Expectancy:
{expectancy}

Recovery Factor:
{recovery_factor}

================================
MONTE CARLO
================================

Best:
{monte_carlo["best"]}

Worst:
{monte_carlo["worst"]}

Average:
{monte_carlo["average"]}

================================
REGIME ANALYSIS
================================

{regime_analysis}

================================
AGENT ANALYSIS
================================

{agent_analysis}

================================
SHADOW ANALYSIS
================================

{shadow_analysis}

================================
"""

        return report

    # ==================================================
    # Save Report
    # ==================================================

    def save(self, report, filename="final_report.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"""

报告已保存:

{filename}
""")