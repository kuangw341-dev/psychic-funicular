import pandas as pd

from ai_agents.trend_agent import TrendAgent
from ai_agents.structure_agent import StructureAgent
from ai_agents.smart_money_agent import SmartMoneyAgent
from ai_agents.volatility_agent import VolatilityAgent
from ai_agents.pullback_agent import PullbackAgent
from ai_agents.risk_manager import RiskManager
from ai_agents.trap_filter import TrapFilter
from ai_agents.weight_manager import WeightManager
from ai_agents.regime_filter import RegimeFilter
from ai_agents.momentum_engine import MomentumEngine
from ai_agents.global_risk import GlobalRiskController
from ai_agents.liquidity_map import LiquidityMap
from ai_agents.central_zone import CentralZoneDetector
from ai_agents.structure_engine import StructureEngine
from ai_agents.liquidity_sweep import LiquiditySweepDetector

from ai_agents.chan.pivot_engine import PivotEngine
from ai_agents.chan.bi_engine import BiEngine
from ai_agents.chan.segment_engine import SegmentEngine
from ai_agents.chan.central_engine import CentralEngine
from ai_agents.chan.divergence_engine import DivergenceEngine

from ai_agents.orderflow.delta_engine import DeltaEngine
from ai_agents.orderflow.absorption_engine import AbsorptionEngine

from ai_agents.risk.structure_trailing import StructureTrailing

from ai_agents.shadow.shadow_learning import ShadowLearning

from ai_agents.orderflow.aggressive_flow import AggressiveFlow

from structure.bos_engine import BOSEngine
from structure.choch_engine import CHOCHEngine
from liquidity.sweep_engine import LiquiditySweepEngine
from smart_money.fvg_engine import FVGEngine

class ChiefAI:
    def __init__(self):
        self.agents = [
            TrendAgent(),
            StructureAgent(),
            SmartMoneyAgent(),
            VolatilityAgent(),
            PullbackAgent()
        ]
        self.risk_manager = RiskManager()
        self.trap_filter = TrapFilter()
        self.weight_manager = WeightManager()
        self.regime_filter = RegimeFilter()
        self.momentum_engine = MomentumEngine()
        self.global_risk = GlobalRiskController()
        self.liquidity_map = LiquidityMap()
        self.central_zone = CentralZoneDetector()
        self.structure_engine = StructureEngine()
        self.sweep_detector = LiquiditySweepDetector()

        self.pivot_engine = PivotEngine()
        self.bi_engine = BiEngine()
        self.segment_engine = SegmentEngine()
        self.central_engine = CentralEngine()
        self.divergence_engine = DivergenceEngine()

        self.delta_engine = DeltaEngine()
        self.absorption_engine = AbsorptionEngine()

        self.structure_trailing = StructureTrailing()

        self.shadow_learning = ShadowLearning()

        self.aggressive_flow = AggressiveFlow()

        self.bos_engine = BOSEngine()
        self.choch_engine = CHOCHEngine()
        self.sweep_engine = LiquiditySweepEngine()
        self.fvg_engine = FVGEngine()

        self.agent_signals = {}

    def evaluate(self, fast_df, slow_df, df_4h, df_1d, balance=1000):
        # ==================== 原有数据准备 ====================
        if len(slow_df) < 10:
            market_regime = "SIDEWAYS"
            ema_slope_15m = 0
            ema_slope_1h = 0
            ema_distance = 0
            atr_pct = 0
            ema20_15m = None
            ema50_15m = None
        else:
            ema20_15m = fast_df["close"].ewm(span=20, adjust=False).mean()
            ema50_15m = fast_df["close"].ewm(span=50, adjust=False).mean()
            ema20_1h = slow_df["close"].ewm(span=20, adjust=False).mean()
            ema50_1h = slow_df["close"].ewm(span=50, adjust=False).mean()

            tr1 = fast_df["high"] - fast_df["low"]
            tr2 = abs(fast_df["high"] - fast_df["close"].shift())
            tr3 = abs(fast_df["low"] - fast_df["close"].shift())
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(14).mean()
            atr_pct = atr.iloc[-1] / fast_df["close"].iloc[-1]

            ema_slope_15m = (ema20_15m.iloc[-1] - ema20_15m.iloc[-5]) / fast_df["close"].iloc[-1]
            ema_slope_1h = (ema20_1h.iloc[-1] - ema20_1h.iloc[-5]) / slow_df["close"].iloc[-1]
            ema_distance = abs(ema20_15m.iloc[-1] - ema50_15m.iloc[-1]) / fast_df["close"].iloc[-1]

            trend_strength = abs(ema20_15m.iloc[-1] - ema50_15m.iloc[-1]) / fast_df["close"].iloc[-1]
            volatility = (fast_df["high"].tail(20).max() - fast_df["low"].tail(20).min()) / fast_df["close"].iloc[-1]

            if trend_strength > 0.003:
                if ema20_15m.iloc[-1] > ema50_15m.iloc[-1]:
                    market_regime = "TREND_BULL"
                else:
                    market_regime = "TREND_BEAR"
            else:
                market_regime = "SIDEWAYS"
            if volatility > 0.03:
                market_regime += "_HIGH_VOL"

        # 打印原有 REGIME 信息（保留）
        print(f'\n================ REGIME =================\nRegime:\n{market_regime}\nATR:\n{round(atr_pct,4)}\nEMA Distance:\n{round(ema_distance,4)}\nSlope15m:\n{round(ema_slope_15m,4)}\nSlope1h:\n{round(ema_slope_1h,4)}\n==========================================\n')

        liquidity = self.liquidity_map.analyze(fast_df)
        aggressive = self.aggressive_flow.detect(fast_df)
        trap_ok = self.trap_filter.check(fast_df)
        if not trap_ok:
            return {
                "action": "HOLD",
                "score": 0,
                "confidence": 0,
                "leverage": 1,
                "position_size": 0,
                "risk_amount": 0,
                "reasons": ["Trap Filter 阻止交易"],
                "market_regime": market_regime
            }

        bull_score = 0
        bear_score = 0
        long_votes = 0
        short_votes = 0
        reasons = []
        smart_money_score = 0

        bos_result = self.bos_engine.detect(fast_df)
        bos_signal = bos_result["bos"]
        if len(slow_df) >= 10 and ema20_15m.iloc[-1] > ema50_15m.iloc[-1]:
            current_trend = "BULL"
        else:
            current_trend = "BEAR"
        choch_signal = self.choch_engine.detect(current_trend, bos_signal)
        sweep_signal = self.sweep_engine.detect(fast_df)
        fvg_signal = self.fvg_engine.detect(fast_df)

        pivots = self.pivot_engine.detect_pivots(fast_df)
        bis = self.bi_engine.build_bi(pivots)
        segment = self.segment_engine.detect_segments(bis)
        central = self.central_engine.detect_central(bis)
        divergence = self.divergence_engine.detect(fast_df)

        if segment["trend"] == "BULL":
            bull_score += 15
            long_votes += 2
            print("\n📈 Chan趋势段: BULL")
        if segment["trend"] == "BEAR":
            bear_score += 15
            short_votes += 2
            print("\n📉 Chan趋势段: BEAR")

        if divergence["bull_divergence"]:
            bull_score += 10
            long_votes += 1
            print("\n🔥 底背驰")
        if divergence["bear_divergence"]:
            bear_score += 10
            short_votes += 1
            print("\n💀 顶背驰")

        for agent in self.agents:
            try:
                result = agent.analyze(fast_df, slow_df)
                signal = result["signal"]
                score = result["score"]
                reason = result["reason"]
                self.agent_signals[agent.__class__.__name__] = {
                    "signal": signal,
                    "score": score,
                    "weighted_score": 0,
                    "reason": reason,
                    "used": False
                }
                if isinstance(agent, SmartMoneyAgent):
                    smart_money_score = score
                weighted_score = self.weight_manager.apply_weight(agent.__class__.__name__, score)
                if agent.__class__.__name__ in self.agent_signals:
                    self.agent_signals[agent.__class__.__name__]["weighted_score"] = weighted_score
                if signal == "LONG":
                    bull_score += weighted_score
                    long_votes += 1
                elif signal == "SHORT":
                    bear_score += weighted_score
                    short_votes += 1
                reasons.append(f"{agent.__class__.__name__}: {reason}")
            except Exception as e:
                print(f"{agent} 错误: {e}")

        structure_data = self.structure_engine.analyze(fast_df)
        structure = structure_data["structure"]
        if structure == "BULL":
            bull_score += 10
            long_votes += 1
        elif structure == "BEAR":
            bear_score += 10
            short_votes += 1

        sweep = self.sweep_detector.detect(fast_df, liquidity)
        if sweep["sweep_high"]:
            bear_score += 15
            short_votes += 2
            print("\n💀 检测到上方流动性扫盘，偏向做空")
        if sweep["sweep_low"]:
            bull_score += 15
            long_votes += 2
            print("\n🔥 检测到下方流动性扫盘，偏向做多")

        central_zone = self.central_zone.detect(fast_df)
        if central_zone["is_central"]:
            print("\n⚠️ 当前处于中枢震荡区，降低交易优先级")
            bull_score = max(bull_score - 20, 0)
            bear_score = max(bear_score - 20, 0)

        if bos_signal == "BULLISH":
            bull_score += 20
            reasons.append("ICT: Bullish BOS")
        if choch_signal == "BULLISH_CHOCH":
            bull_score += 20
            long_votes += 2
            reasons.append("ICT: Bullish CHOCH")
        if sweep_signal == "SWEEP_LOW":
            bull_score += 10
            reasons.append("ICT: Sweep Low")
        if fvg_signal and fvg_signal["type"] == "BULLISH_FVG":
            bull_score += 15
            reasons.append("ICT: Bullish FVG")

        if bos_signal == "BEARISH":
            bear_score += 20
            reasons.append("ICT: Bearish BOS")
        if choch_signal == "BEARISH_CHOCH":
            bear_score += 20
            short_votes += 2
            reasons.append("ICT: Bearish CHOCH")
        if sweep_signal == "SWEEP_HIGH":
            bear_score += 10
            reasons.append("ICT: Sweep High")
        if fvg_signal and fvg_signal["type"] == "BEARISH_FVG":
            bear_score += 15
            reasons.append("ICT: Bearish FVG")

        if len(slow_df) >= 10:
            trend_long = ema20_15m.iloc[-1] > ema50_15m.iloc[-1]
            ict_bull = (bos_signal == "BULLISH" or (fvg_signal and fvg_signal["type"] == "BULLISH_FVG"))
            ict_bear = (bos_signal == "BEARISH" or (fvg_signal and fvg_signal["type"] == "BEARISH_FVG"))
            if trend_long and ict_bear:
                bear_score = max(bear_score - 15, 0)
                reasons.append("冲突过滤: Trend BULL + ICT BEAR，降低空头分数")
            if (not trend_long) and ict_bull:
                bull_score = max(bull_score - 15, 0)
                reasons.append("冲突过滤: Trend BEAR + ICT BULL，降低多头分数")

        delta = self.delta_engine.calculate(fast_df.tail(20))
        absorption = self.absorption_engine.detect(fast_df.tail(20))

        if delta["buy_delta"] > delta["sell_delta"] * 1.3:
            bull_score += 10
            long_votes += 1
            print("\n🟢 主动买盘增强")
        if delta["sell_delta"] > delta["buy_delta"] * 1.3:
            bear_score += 10
            short_votes += 1
            print("\n🔴 主动卖盘增强")
        if absorption["absorption"]:
            bull_score += 10
            print("\n🏦 检测到吸筹行为")

        if market_regime == "TREND_BULL":
            if short_votes >= 3:
                short_votes = 0
        elif market_regime == "TREND_BEAR":
            if long_votes >= 3:
                long_votes = 0

        bull_score = min(bull_score, 100)
        bear_score = min(bear_score, 100)
        score_gap = abs(bull_score - bear_score)
        total_score = max(bull_score, bear_score)
        confidence = round(total_score / 100, 2)

        # ========== 放宽开仓条件 ==========
        action = "HOLD"
        trigger_score = 45      # 原58
        # 投票数要求从3降到2，分数差距从15降到10
        long_condition = (bull_score > bear_score and score_gap >= 10 and long_votes >= 2 and bull_score >= trigger_score)
        short_condition = (bear_score > bull_score and score_gap >= 10 and short_votes >= 2 and bear_score >= trigger_score)
        # LONG额外条件：增加备用 bull_score >= 70
        long_extra = (aggressive["aggressive_flow"] or smart_money_score >= 15 or bull_score >= 70)

        # 处理无BOS情况（不强制HOLD，降低权重）
        if bos_signal is None:
            confidence *= 0.8
            bull_score *= 0.9
            bear_score *= 0.9
            score_gap = abs(bull_score - bear_score)
            total_score = max(bull_score, bear_score)
            print("⚠️ ICT: 无 BOS 结构，降低权重")

        if long_condition:
            if long_extra:
                action = "LONG"
            else:
                print("\n⚠️ Aggressive Flow 不满足且 SmartMoney 分数不足且总分<70，LONG 被过滤")
        elif short_condition:
            action = "SHORT"

        # ========== 超级行情检测 ==========
        burst_data = self.momentum_engine.detect(fast_df)
        burst_mode = burst_data["burst"]
        burst_strength = burst_data["strength"]
        if burst_mode:
            bull_score += 15
            bear_score += 15
            bull_score = min(bull_score, 100)
            bear_score = min(bear_score, 100)
            total_score = max(bull_score, bear_score)
            confidence = round(total_score / 100, 2)
            print(f"\n🚀 检测到超级行情，强度: {round(burst_strength,2)}")

        risk = self.risk_manager.calculate(confidence, balance, market_regime, trend_strength=burst_strength)

        # 调试输出
        print("\n================ AGENT DEBUG ================")
        print("LONG VOTES:", long_votes)
        print("SHORT VOTES:", short_votes)
        print("BULL SCORE:", round(bull_score, 2))
        print("BEAR SCORE:", round(bear_score, 2))
        print("GAP:", round(score_gap, 2))
        print("ACTION:", action)
        print("REASONS:", reasons)
        self.weight_manager.show_weights()
        print("\n============================================\n")

        decision_log = {
            "bull_score": bull_score,
            "bear_score": bear_score,
            "score_gap": score_gap,
            "long_votes": long_votes,
            "short_votes": short_votes,
            "bos": bos_signal,
            "choch": choch_signal,
            "sweep": sweep_signal,
            "fvg": fvg_signal,
            "regime": market_regime,
            "action": action
        }

        if action in ["LONG", "SHORT"]:
            for name, data in self.agent_signals.items():
                if data["signal"] == action:
                    data["used"] = True

        return {
            "action": action,
            "score": round(total_score, 2),
            "confidence": confidence,
            "decision_log": decision_log,
            "leverage": risk["leverage"],
            "position_size": risk["position_size"],
            "risk_amount": risk["risk_amount"],
            "reasons": reasons,
            "market_regime": market_regime,
            "pivots": pivots,
            "central": central,
            "bos_signal": bos_signal,
            "choch_signal": choch_signal,
            "fvg_signal": fvg_signal,
            "chan_trend": segment["trend"],
            "divergence": divergence
        }