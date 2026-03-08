
def scoring_formula_price(min, max, curr):
    return (max - curr) / (max - min)
def scoring_formula_time(min, max, curr):
    return (curr - min) / (max - min)