import pandas as pd


class AgentExpectancy:

    def analyze(self, csv_file="trade_attribution.csv"):

        df = pd.read_csv(csv_file)

        print()
        print("================================")
        print("FAST AGENT ANALYSIS")
        print("================================")
        print()

        print("CSV COLUMNS:")
        print(df.columns.tolist())
        print()

        agent_columns = [
            "TrendAgent",
            "StructureAgent",
            "SmartMoneyAgent",
            "VolatilityAgent",
            "PullbackAgent"
        ]

        for agent in agent_columns:

            if agent not in df.columns:
                continue

            # Agent参与过的交易
            sub = df[df[agent] != 0]

            trades = len(sub)

            net_profit = sub["profit"].sum()

            avg_profit = (
                sub["profit"].mean()
                if trades > 0 else 0
            )

            print(agent)
            print()

            print("Trades:", trades)

            print(
                "Net Profit:",
                round(net_profit, 2)
            )

            print(
                "Avg Profit:",
                round(avg_profit, 2)
            )

            print("--------------------------------")


if __name__ == "__main__":

    print("START")

    expectancy = AgentExpectancy()
    expectancy.analyze("trade_attribution.csv")

    print("END")