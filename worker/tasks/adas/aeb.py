def apply_aeb(ego_speed_kmh: float, lead_distance_m: float):
    """
    Simple AEB logic using Time-To-Collision (TTC).
    Returns (aeb_active: bool, reason: str)
    """

    # Avoid division by zero
    if ego_speed_kmh <= 0:
        return False, "vehicle_stopped"

    # Convert km/h → m/s
    ego_speed_ms = ego_speed_kmh / 3.6

    ttc = lead_distance_m / ego_speed_ms  # seconds

    if ttc < 1.5:
        return True, "AEB_EMERGENCY"
    elif ttc < 2.5:
        return True, "AEB_WARNING"
    else:
        return False, "SAFE"
