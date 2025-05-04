def calculate_score(car_km, meat_days, plastic_use):
    score = 100
    score -= car_km * 0.3
    score -= meat_days * 5
    if plastic_use:
        score -= 10
    return max(0, min(score, 100))
