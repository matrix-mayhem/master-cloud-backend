import time
import random
import struct
from datetime import datetime

from worker_database import MarketSessionLocal
from models.adas_frame import AdasFrame
from models.can_frame import CanFrame

# ==============================
# Simulation control flag
# ==============================
SIM_RUNNING = False


# ==============================
# CAN ENCODING HELPERS
# ==============================
def encode_speed(speed_kmh: float) -> bytes:
    """
    Encode speed (km/h) into CAN payload (uint16, scale 0.01)
    """
    raw = int(speed_kmh * 100)
    return struct.pack("<H", raw) + b"\x00" * 6


def encode_aeb(active: bool) -> bytes:
    """
    Encode AEB status into CAN payload
    """
    return struct.pack("<B", 1 if active else 0) + b"\x00" * 7


# ==============================
# ADAS SIMULATION LOOP
# ==============================
def start_adas_simulation():
    global SIM_RUNNING
    SIM_RUNNING = True

    session = MarketSessionLocal()
    print("🚗 ADAS simulation started")

    ego_speed = 60.0        # km/h
    lead_distance = 40.0    # meters

    while SIM_RUNNING:
        # ------------------------------
        # Simulated Radar (vECU)
        # ------------------------------
        lead_distance += random.uniform(-3.0, 1.5)
        lead_distance = max(2.0, lead_distance)

        # ------------------------------
        # Camera Sign Detection (sim)
        # ------------------------------
        sign = random.choice(["NONE", "SPEED_30", "SPEED_60", "STOP"])

        # ------------------------------
        # AEB LOGIC
        # ------------------------------
        aeb_active = False
        action = "MAINTAIN"

        if lead_distance < 8.0:
            aeb_active = True
            ego_speed = max(0.0, ego_speed - 15.0)
            action = "BRAKE"

        elif sign == "STOP":
            ego_speed = max(0.0, ego_speed - 10.0)
            action = "BRAKE"

        elif sign == "SPEED_30" and ego_speed > 30:
            ego_speed -= 5.0
            action = "BRAKE"

        elif sign == "SPEED_60" and ego_speed < 60:
            ego_speed += 3.0
            action = "ACCELERATE"

        # ------------------------------
        # Store ADAS FRAME
        # ------------------------------
        adas = AdasFrame(
            timestamp=datetime.utcnow(),
            ego_speed=ego_speed,
            lead_distance=lead_distance,
            detected_sign=sign,
            commanded_action=action,
        )
        session.add(adas)

        # ------------------------------
        # CAN TX (ADAS ECU → Radar vECU)
        # ------------------------------
        speed_payload = encode_speed(ego_speed)
        aeb_payload = encode_aeb(aeb_active)

        can_speed = CanFrame(
            timestamp=datetime.utcnow(),
            can_id=0x100,
            payload=speed_payload,
        )

        can_aeb = CanFrame(
            timestamp=datetime.utcnow(),
            can_id=0x200,
            payload=aeb_payload,
        )

        session.add(can_speed)
        session.add(can_aeb)

        session.commit()

        # ------------------------------
        # LOG OUTPUT
        # ------------------------------
        print(
            f"🚗 v={ego_speed:.1f} km/h | "
            f"d={lead_distance:.1f} m | "
            f"sign={sign} | "
            f"AEB={'ON' if aeb_active else 'OFF'}"
        )
        print(f"🚌 CAN TX | ID=0x100 | DATA={speed_payload.hex()}")
        print(f"🚌 CAN TX | ID=0x200 | DATA={aeb_payload.hex()}")

        time.sleep(1.0)

    session.close()
    print("🛑 ADAS simulation stopped")


def stop_adas_simulation():
    global SIM_RUNNING
    SIM_RUNNING = False
