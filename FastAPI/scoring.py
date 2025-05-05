def calculate_score(car_km, daily_water_use, plastic_use):
    score = 100
    score -= car_km * 0.3
    score -= daily_water_use * 0.2
    if plastic_use:
        score -= 10
    return max(0, min(score, 100))
