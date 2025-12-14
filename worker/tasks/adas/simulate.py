import random
import time
from datetime import datetime

from worker_database import MarketSessionLocal
from models.adas_frame import AdasFrame

# Simple global flag to control simulation loop
SIM_RUNNING = False


def start_adas_simulation(symbol: str = "SIM_ROAD"):
    """
    Start a simple ADAS simulation loop that:
    - simulates ego speed
    - lead vehicle distance
    - random road signs
    - commanded action
    """
    global SIM_RUNNING
    SIM_RUNNING = True

    session = MarketSessionLocal()
    print("🚗 ADAS simulation started...")

    ego_speed = 50.0       # km/h
    lead_distance = 30.0   # meters

    while SIM_RUNNING:
        # Randomly simulate road sign
        sign = random.choice(["NONE", "SPEED_30", "SPEED_60", "STOP"])

        # Simple rule-based controller
        if sign == "STOP":
            commanded = "BRAKE"
            ego_speed = max(0.0, ego_speed - 10.0)
        elif sign == "SPEED_30":
            if ego_speed > 30:
                commanded = "BRAKE"
                ego_speed -= 5.0
            else:
                commanded = "MAINTAIN"
        elif sign == "SPEED_60":
            if ego_speed < 60:
                commanded = "ACCELERATE"
                ego_speed += 5.0
            else:
                commanded = "MAINTAIN"
        else:
            commanded = random.choice(["MAINTAIN", "ACCELERATE", "BRAKE"])

        # Simulate lead vehicle distance
        lead_distance = max(5.0, lead_distance + random.uniform(-2.0, 2.0))

        frame = AdasFrame(
            timestamp=datetime.utcnow(),
            ego_speed=ego_speed,
            lead_distance=lead_distance,
            detected_sign=sign,
            commanded_action=commanded,
        )
        session.add(frame)
        session.commit()

        print(
            f"🚗 [{frame.timestamp}] v={ego_speed:.1f} km/h,"
            f" d_lead={lead_distance:.1f} m, sign={sign}, action={commanded}"
        )

        time.sleep(1.0)

    session.close()
    print("🛑 ADAS simulation stopped.")


def stop_adas_simulation():
    global SIM_RUNNING
    SIM_RUNNING = False
