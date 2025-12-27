import statistics

def analyze_financials(data):

    score = 0
    flags = []
    suggestions = []

    categories = {
        "Profit Quality": "Healthy",
        "Liquidity": "Healthy",
        "Leverage": "Healthy",
        "Consistency": "Healthy"
    }

    # ===================== RATIOS (FY-3) =====================
    ratios = {}

    ratios["CFO_to_Profit"] = (
        data["CFO"][2] / data["Profit"][2]
        if data["Profit"][2] != 0 else 0
    )

    accruals = data["Profit"][2] - data["CFO"][2]
    ratios["Accrual_Intensity"] = (
        accruals / data["Revenue"][2]
        if data["Revenue"][2] != 0 else 0
    )

    ratios["Receivables_to_Revenue"] = (
        data["Receivables"][2] / data["Revenue"][2]
        if data["Revenue"][2] != 0 else 0
    )

    ratios["Debt_to_Revenue"] = (
        data["Debt"][2] / data["Revenue"][2]
        if data["Revenue"][2] != 0 else 0
    )

    # ===================== PROFIT QUALITY =====================
    if data["Profit"][2] > data["Profit"][1] and data["CFO"][2] < data["CFO"][1]:
        flags.append("Profit growth not supported by operating cash flows")
        categories["Profit Quality"] = "Red Flag"
        score += 25
        suggestions.append(
            "Assess sustainability of earnings and revenue recognition practices."
        )

    elif ratios["CFO_to_Profit"] < 1:
        flags.append("Operating cash flows are weaker than reported profits")
        categories["Profit Quality"] = "Watch"
        score += 15
        suggestions.append(
            "Monitor cash conversion trends closely."
        )

    # ===================== ACCRUAL SHOCK =====================
    prev_accrual = (
        (data["Profit"][1] - data["CFO"][1]) / data["Revenue"][1]
        if data["Revenue"][1] != 0 else 0
    )

    if ratios["Accrual_Intensity"] > prev_accrual * 1.5 and ratios["Accrual_Intensity"] > 0:
        flags.append("Sharp increase in accrual-based earnings in the latest year")
        categories["Profit Quality"] = "Red Flag"
        score += 25
        suggestions.append(
            "Examine accrual assumptions and accounting estimates."
        )

    # ===================== LIQUIDITY =====================
    if (data["Receivables"][2] - data["Receivables"][1]) > (
        data["Revenue"][2] - data["Revenue"][1]
    ):
        flags.append("Receivables growing faster than revenue")
        categories["Liquidity"] = "Red Flag"
        score += 25
        suggestions.append(
            "Review credit policy and collection efficiency."
        )

    # ===================== LEVERAGE =====================
    if (data["Debt"][2] - data["Debt"][1]) > 2 * (data["Debt"][1] - data["Debt"][0]):
        flags.append("Sharp acceleration in debt levels in the latest year")
        categories["Leverage"] = "Red Flag"
        score += 25
        suggestions.append(
            "Evaluate debt servicing capacity and refinancing risks."
        )

    # ===================== NEW: EARNINGS SMOOTHNESS =====================
    revenue_growth = [
        (data["Revenue"][i] - data["Revenue"][i-1]) / data["Revenue"][i-1]
        for i in range(1, 3) if data["Revenue"][i-1] != 0
    ]

    profit_growth = [
        (data["Profit"][i] - data["Profit"][i-1]) / abs(data["Profit"][i-1])
        for i in range(1, 3) if data["Profit"][i-1] != 0
    ]

    if len(revenue_growth) > 1 and len(profit_growth) > 1:
        if statistics.stdev(profit_growth) < statistics.stdev(revenue_growth) * 0.5:
            flags.append("Reported profits appear unusually smooth relative to revenue volatility")
            categories["Profit Quality"] = "Watch"
            score += 15
            suggestions.append(
                "Investigate potential earnings smoothing through accounting adjustments."
            )

    # ===================== NEW: GROWTH QUALITY =====================
    growth_quality = "No Growth or Decline"

    if data["Revenue"][2] > data["Revenue"][1]:
        if data["CFO"][2] > data["CFO"][1]:
            growth_quality = "Healthy Growth"
        elif (data["Receivables"][2] - data["Receivables"][1]) > (
            data["Revenue"][2] - data["Revenue"][1]
        ):
            growth_quality = "Aggressive (Credit-Driven) Growth"
        else:
            growth_quality = "Unsustainable Growth"

    ratios["Growth_Quality"] = growth_quality

    # ===================== CONSISTENCY =====================
    if score >= 50:
        categories["Consistency"] = "Red Flag"
        flags.append("Multiple financial anomalies concentrated in the latest year")
        suggestions.append(
            "Heightened monitoring recommended due to clustering of forensic risk signals."
        )

    # ===================== RISK LEVEL =====================
    if score >= 70:
        risk = "High Risk"
    elif score >= 35:
        risk = "Moderate Risk"
    else:
        risk = "Low Risk"

    explanation = (
        "The model integrates ratio diagnostics, accrual analysis, earnings smoothness checks, "
        "and growth quality classification to identify early forensic risk signals using "
        "multi-year financial statement behaviour."
    )

    return score, risk, flags, categories, explanation, suggestions, ratios
