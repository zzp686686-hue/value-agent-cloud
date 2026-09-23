def fair_value_engine(norm_eps, moat, roic, growth, balance_health):
    # 合理PE区间
    if moat=='Strong' and roic>0.2:
        pe_base_range = (22,30)
        pe_bear_range = (15,20)
    elif moat=='Moderate' and roic>0.12:
        pe_base_range = (15,25)
        pe_bear_range = (12,18)
    else:
        pe_base_range = (10,15)
        pe_bear_range = (8,12)
    
    base_pe = sum(pe_base_range)/2
    bear_pe = sum(pe_bear_range)/2
    
    # 增长衰减
    growth_base = min(growth, 0.25) * 0.85  # 高增长衰减
    growth_bear = growth_base * 0.3

    bear_fair = norm_eps * bear_pe * (1+growth_bear)
    base_fair = norm_eps * base_pe * (1+growth_base)
    
    return {
        "bear_fair": bear_fair,
        "base_fair": base_fair,
        "bear_pe": bear_pe,
        "base_pe": base_pe,
        "growth_bear": growth_bear,
        "growth_base": growth_base
    }
