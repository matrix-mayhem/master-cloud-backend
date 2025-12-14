import random
import time
from datetime import datetime

from worker_database import MarketSessionLocal
from models.adas_frame import AdasFrame

SIM_RUNNING = False

# -----------------------------
# SENSOR MODELS (SIMULATED)
# -----------------------------

def simulate_radar():
    """
    Simulate radar lead vehicle distance (meters)
    """
    return max(3.0, random.uniform(5.0, 50.0))


def simulate_camera_lane():
    """
    Simulate camera-based lane detection
    """
    return random.choice(["LEFT", "CENTER", "RIGHT"])


def simulate_camera_sign():
    """
    Simulate traffic sign recognition
    """
    return random.choice(["NONE", "SPEED_30", "SPEED_60", "STOP"])


# -----------------------------
# SENSOR FUSION + CONTROL LOGIC
# -----------------------------

def fusion_and_control(ego_speed, lead_distance, lane_pos, sign):
    """
    Simple ADAS fusion logic:
    - Radar + camera + rules
    """
    action = "MAINTAIN"

    # 🚨 AEB LOGIC (highest priority)
    if lead_distance < 8.0:
        return "EMERGENCY_BRAKE", max(0.0, ego_speed - 20.0)

    # 🛑 STOP sign
    if sign == "STOP":
        return "BRAKE", max(0.0, ego_speed - 10.0)

    # 🚦 Speed signs
    if sign == "SPEED_30" and ego_speed > 30:
        return "BRAKE", ego_speed - 5.0

    if sign == "SPEED_60" and ego_speed < 60:
        return "ACCELERATE", ego_speed + 5.0

    # 🚗 Lane-based comfort control
    if lane_pos != "CENTER":
        return "MAINTAIN", ego_speed

    # 🧭 Default cruise behavior
    if ego_speed < 50:
        action = "ACCELERATE"
        ego_speed += 2.0

    return action, ego_speed


# -----------------------------
# MAIN ADAS SIMULATION LOOP
# -----------------------------

def start_adas_simulation():
    global SIM_RUNNING
    SIM_RUNNING = True

    session = MarketSessionLocal()
    ego_speed = 40.0  # km/h

    print("🚗 ADAS simulation started (Radar + Camera + Fusion)...")

    while SIM_RUNNING:
        try:
            # --- SENSOR INPUTS ---
            lead_distance = simulate_radar()
            lane_position = simulate_camera_lane()
            detected_sign = simulate_camera_sign()

            # --- FUSION + CONTROL ---
            commanded_action, ego_speed = fusion_and_control(
                ego_speed,
                lead_distance,
                lane_position,
                detected_sign
            )

            # --- STORE FRAME ---
            frame = AdasFrame(
                timestamp=datetime.utcnow(),
                ego_speed=ego_speed,
                lead_distance=lead_distance,
                detected_sign=f"{detected_sign}|LANE_{lane_position}",
                commanded_action=commanded_action
            )

            session.add(frame)
            session.commit()

            # --- LOG OUTPUT ---
            print(
                f"🚗 v={ego_speed:.1f} km/h | "
                f"radar={lead_distance:.1f} m | "
                f"lane={lane_position} | "
                f"sign={detected_sign} | "
                f"action={commanded_action}"
            )

            time.sleep(1)

        except Exception as e:
            print("❌ ADAS simulation error:", e)
            time.sleep(1)

    session.close()
    print("🛑 ADAS simulation stopped.")


def stop_adas_simulation():
    global SIM_RUNNING
    SIM_RUNNING = False
