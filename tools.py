from enum import Enum


class Room(Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    OFFICE = "office"


_light_state = {room: False for room in Room}




def turn_on_light(room: str) -> str:
    try:
        r = Room(room)
    except ValueError:
        raise ValueError(f"Unknown room: {room}")
    _light_state[r] = True
    return f"The light in the {r.value} is now ON."




def turn_off_light(room: str) -> str:
    try:
     r = Room(room)
    except ValueError:
        raise ValueError(f"Unknown room: {room}")
    _light_state[r] = False
    return f"The light in the {r.value} is now OFF."




def get_light_status(room: str) -> str:
    try:
        r = Room(room)
    except ValueError:
        raise ValueError(f"Unknown room: {room}")
    state = "ON" if _light_state[r] else "OFF"
    return f"The light in the {r.value} is currently {state}."