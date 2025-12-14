import struct
from datetime import datetime
from worker_database import MarketSessionLocal
from models.can_frame import CanFrame

# Example CAN IDs (industry-like)
CAN_ID_VEHICLE_STATE = 0x100
CAN_ID_ADAS_STATUS = 0x200


def pack_vehicle_state(speed, lead_distance):
    """
    Pack speed & lead distance into 8-byte CAN payload
    """
    # speed: uint16 (0.1 km/h)
    # lead_distance: uint16 (0.1 m)
    data = struct.pack(
        "<HH4x",
        int(speed * 10),
        int(lead_distance * 10)
    )
    return data.hex()


def pack_adas_status(brake, throttle, aeb_active, lane_departure):
    """
    Pack ADAS control signals
    """
    data = struct.pack(
        "<BBBB4x",
        int(brake),
        int(throttle),
        int(aeb_active),
        int(lane_departure)
    )
    return data.hex()


def send_can_frames(speed, lead_distance, brake, throttle, aeb_active, lane_departure):
    session = MarketSessionLocal()

    vehicle_payload = pack_vehicle_state(speed, lead_distance)
    adas_payload = pack_adas_status(brake, throttle, aeb_active, lane_departure)

    frames = [
        CanFrame(can_id=CAN_ID_VEHICLE_STATE, data=vehicle_payload),
        CanFrame(can_id=CAN_ID_ADAS_STATUS, data=adas_payload),
    ]

    for frame in frames:
        session.add(frame)
        print(
            f"🚌 CAN TX | ID=0x{frame.can_id:X} | DATA={frame.data}"
        )

    session.commit()
    session.close()
