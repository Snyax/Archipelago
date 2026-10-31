from BaseClasses import ItemClassification as IC

from worlds.x2wotc.ItemData import X2WOTCItemData, PROMOTION_ITEM_PREFIX, get_new_item_id
from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
)


name = "Scavenger Class"
id = 3158385565

rule_priority = 0.0

MAX_RANK = 8
RANKS_STR = ", ".join(f"Ranks[{i-2}]={i}" for i in range(2, MAX_RANK+1))
# Keys are internal names, values are localized names
SOLDIER_CLASSES = {
    "ARFMScavenger": "Scavenger",
}
RANK_NAMES = [
    "Scav",
    "Specialist",
    "Sergeant",
    "Staff Sergeant",
    "Sergeant First Class",
    "Master Sergeant",
    "First Sergeant",
    "Sergeant Major",
    "Command Sergeant Major",
]

items: dict[str, X2WOTCItemData] = {
    f"{internal_name}Rank": X2WOTCItemData(
        display_name = PROMOTION_ITEM_PREFIX + localized_name,
        id = get_new_item_id(),
        classification = IC.progression,
        type = "Promotion",
        tags = {localized_name.lower().replace(" ", "_")},
        power = 15.0
    )
    for internal_name, localized_name in SOLDIER_CLASSES.items()
}

locations: dict[str, X2WOTCLocationData] = {
    f"{internal_name}Rank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + localized_name + SOLDIER_RANK_LOCATION_INFIX + RANK_NAMES[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {localized_name.lower().replace(" ", "_"), f"item:{internal_name}Rank:{rank - 1}"},
        normal_item = f"{internal_name}Rank"
    )
    for internal_name, localized_name in SOLDIER_CLASSES.items()
    for rank in range(2, MAX_RANK + 1)
}

config: dict[str, str] = {
    "WOTCArchipelago_Ranksanity": "\n".join(
        f'+RanksanityData=(ID="{internal_name}", ClassName="{internal_name}", {RANKS_STR})'
        for internal_name in SOLDIER_CLASSES.keys()
    )
}
