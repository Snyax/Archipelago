from textwrap import dedent
from typing import TYPE_CHECKING

from BaseClasses import ItemClassification as IC

if TYPE_CHECKING:
    from worlds.x2wotc import X2WOTCWorld
from worlds.x2wotc.ItemData import X2WOTCItemData, PROMOTION_ITEM_PREFIX, get_new_item_id
from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
    DEFAULT_RANK_NAMES,
)

MAX_RANK = 8

BASE_GAME_CLASS_NAMES = [
    "Grenadier",
    "Ranger",
    "Specialist",
    "Sharpshooter",
]

LW2_CLASS_NAMES = [
    "Assault",
    "Gunner",
    "Shinobi",
    "Technical",
]

name = "[WOTC] LW2 Classes and Perks"
location_map = {
    f"LWOTC_{class_name}Rank{rank}": f"{class_name}Rank{rank}"
    for class_name in BASE_GAME_CLASS_NAMES
    for rank in range(2, MAX_RANK + 1)
}
item_map = {
    f"{class_name}Rank": f"LWOTC_{class_name}Rank"
    for class_name in BASE_GAME_CLASS_NAMES + LW2_CLASS_NAMES
}

# If used alongside a mod that disables the 4 base game classes, this must be greater than the other mod
rule_priority = 1.0

def generate_early(world: "X2WOTCWorld"):
    # This mod reappropriates vanilla promotion items and locations for its own replacement classes of the same name,
    # despite using distinct soldier class templates. Another mod (with lower rule_priority) may have previously
    # disabled these, but is otherwise not opposed to our new classes, so we re-enable them when necessary.
    # This will not be compatible with other mods that want to do the same.
    if world.options.rank_sanity != "none":
        for soldier_class in BASE_GAME_CLASS_NAMES:
            for rank in range(2, 8):
                if world.loc_manager.enable_location(f"{soldier_class.title()}Rank{rank}"):
                    world.item_manager.add_item(f"{soldier_class.title()}Rank")

brigadier_locations: dict[str, X2WOTCLocationData] = {
    f"{class_name}Rank8": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + class_name + SOLDIER_RANK_LOCATION_INFIX + DEFAULT_RANK_NAMES[8],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {class_name.lower(), f"item:{class_name}Rank:7"},
        dlc = None,
        normal_item = f"{class_name}Rank"
    )
    for class_name in BASE_GAME_CLASS_NAMES
}

lw2_class_locations: dict[str, X2WOTCLocationData] = {
    f"LWOTC_{class_name}Rank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + class_name + SOLDIER_RANK_LOCATION_INFIX + DEFAULT_RANK_NAMES[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {class_name.lower(), f"item:{class_name}Rank:{rank - 1}"},
        dlc = None,
        normal_item = f"{class_name}Rank"
    )
    for class_name in LW2_CLASS_NAMES
    for rank in range(2, MAX_RANK + 1)
}

locations: dict[str, X2WOTCLocationData] = {
    **brigadier_locations,
    **lw2_class_locations,
}

config: dict[str, str] = {
    "WOTCArchipelago_Ranksanity": dedent(
        r"""
        +DisabledDataEntries=DefaultRanger
        +DisabledDataEntries=DefaultGrenadier
        +DisabledDataEntries=DefaultSpecialist
        +DisabledDataEntries=DefaultSharpshooter
        +RanksanityData=(ID=LW2Assault, SoldierClass=LWOTC_Assault, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LW2Grenadier, SoldierClass=LWOTC_Grenadier, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LW2Gunner, SoldierClass=LWOTC_Gunner, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LW2Ranger, SoldierClass=LWOTC_Ranger, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LW2Sharpshooter, SoldierClass=LWOTC_Sharpshooter, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LW2Shinobi, SoldierClass=LWOTC_Shinobi, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LW2Specialist, SoldierClass=LWOTC_Specialist, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        +RanksanityData=(ID=LW2Technical, SoldierClass=LWOTC_Technical, \\
        Ranks[0]=2, Ranks[1]=3, Ranks[2]=4, Ranks[3]=5, Ranks[4]=6, Ranks[5]=7, Ranks[6]=8)
        """
    )
}
