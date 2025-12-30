import random
import time
from datetime import datetime

from worker_database import MarketSessionLocal
from models.adas_frame import AdasFrame
from models.can_frame import CanFrame


SIM_RUNNING = False


def send_can_frame(session, can_id: int, payload: bytes):
    """
    Send a CAN frame and store it in DB
    """
    frame = CanFrame(
        timestamp=datetime.utcnow(),
        can_id=can_id,
        dlc=len(payload),
        payload=payload
    )

    session.add(frame)
    session.commit()

    print(
        f"🚌 CAN TX | ID=0x{can_id:03X} | "
        f"DLC={len(payload)} | DATA={payload.hex()}"
    )


def start_adas_simulation():
    global SIM_RUNNING
    SIM_RUNNING = True

    session = MarketSessionLocal()
    print("🚗 ADAS simulation started (vECU Master)...")

    ego_speed = 50.0          # km/h
    lead_distance = 30.0      # meters

    while SIM_RUNNING:
        sign = random.choice(["NONE", "SPEED_30", "SPEED_60", "STOP"])

        # ---------- ADAS LOGIC ----------
        if sign == "STOP":
            action = "BRAKE"
            ego_speed = max(0.0, ego_speed - 10.0)
        elif sign == "SPEED_30":
            action = "BRAKE" if ego_speed > 30 else "MAINTAIN"
            ego_speed = max(30.0, ego_speed - 5.0)
        elif sign == "SPEED_60":
            action = "ACCELERATE" if ego_speed < 60 else "MAINTAIN"
            ego_speed = min(60.0, ego_speed + 5.0)
        else:
            action = "MAINTAIN"

        lead_distance = max(5.0, lead_distance + random.uniform(-2.0, 2.0))

        # ---------- STORE ADAS FRAME ----------
        adas = AdasFrame(
            timestamp=datetime.utcnow(),
            ego_speed=ego_speed,
            lead_distance=lead_distance,
            detected_sign=sign,
            commanded_action=action,
        )
        session.add(adas)
        session.commit()

        print(
            f"🚗 v={ego_speed:.1f} km/h | "
            f"d={lead_distance:.1f} m | "
            f"sign={sign} | action={action}"
        )

        # ---------- CAN SIGNAL ENCODING ----------
        # CAN ID 0x100 → Ego speed (Radar vECU expects this)
        speed_raw = int(ego_speed * 100)     # scale: 0.01 km/h
        payload_speed = speed_raw.to_bytes(2, "little") + b"\x00" * 6
        send_can_frame(session, 0x100, payload_speed)

        # CAN ID 0x200 → AEB / Brake command
        brake_flag = 1 if action == "BRAKE" else 0
        payload_brake = bytes([brake_flag]) + b"\x00" * 7
        send_can_frame(session, 0x200, payload_brake)

        time.sleep(1.0)

    session.close()
    print("🛑 ADAS simulation stopped.")


def stop_adas_simulation():
    global SIM_RUNNING
    SIM_RUNNING = False
