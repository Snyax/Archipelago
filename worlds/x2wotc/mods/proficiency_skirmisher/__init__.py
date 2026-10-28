from BaseClasses import ItemClassification as IC

from worlds.x2wotc.ItemData import X2WOTCItemData, PROMOTION_ITEM_PREFIX, get_new_item_id
from worlds.x2wotc.LocationData import (
    X2WOTCLocationData,
    get_new_location_id,
    SOLDIER_RANK_LOCATION_PREFIX,
    SOLDIER_RANK_LOCATION_INFIX,
    DEFAULT_RANK_NAMES,
)

name = "[WOTC] Proficiency Class Plugin: Skirmisher"

rule_priority = 0.0

MAX_RANK = 7
RANKS_STR = ", ".join(f"Ranks[{i-2}]={i}" for i in range(2, MAX_RANK+1))

items: dict[str, X2WOTCItemData] = {
    "WOTC_APA_SkirmisherCohortRank": X2WOTCItemData(
        display_name = PROMOTION_ITEM_PREFIX + "Skirmisher Cohort",
        id = get_new_item_id(),
        classification = IC.progression,
        type = "Promotion",
        tags = {"skirmisher_cohort"},
        power = 15.0,
    )
}

locations: dict[str, X2WOTCLocationData] = {
    f"WOTC_APA_SkirmisherCohortRank{rank}": X2WOTCLocationData(
        display_name = SOLDIER_RANK_LOCATION_PREFIX + "Skirmisher Cohort" + SOLDIER_RANK_LOCATION_INFIX + DEFAULT_RANK_NAMES[rank],
        id = get_new_location_id(),
        type = "SoldierRank",
        tags = {"skirmisher_cohort", f"item:WOTC_APA_SkirmisherCohortRank:{rank - 1}"},
        dlc = None,
        normal_item = "WOTC_APA_SkirmisherCohortRank"
    )
    for rank in range(2, MAX_RANK + 1)
}

config: dict[str, str] = {
    "WOTCArchipelago_Ranksanity": f'+RanksanityData=(ID="WOTC_APA_SkirmisherCohort", ClassName="WOTC_APA_SkirmisherCohort", {RANKS_STR})'
}
