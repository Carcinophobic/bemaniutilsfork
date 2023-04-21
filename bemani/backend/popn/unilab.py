# vim: set fileencoding=utf-8
import math
import random
from typing import Any, Dict, List, Tuple

from bemani.backend.popn.base import PopnMusicBase
from bemani.backend.popn.common import PopnMusicModernBase
from bemani.backend.popn.kaimei import PopnMusicKaimei
from bemani.common import VersionConstants
from bemani.common.validateddict import Profile
from bemani.data.types import UserID
from bemani.protocol.node import Node


class PopnMusicUniLab(PopnMusicModernBase):

    name: str = "Pop'n Music UniLab"
    version: int = VersionConstants.POPN_MUSIC_UNILAB

    # Biggest ID in the music DB
    GAME_MAX_MUSIC_ID: int = 2043

    # Biggest deco part ID in the game
    GAME_MAX_DECO_ID: int = 133

    # Item limits are as follows:
    # 0: 2043 - ID is the music ID that the player purchased/unlocked.
    # 1: 2344
    # 2: 3
    # 3: 133 - ID points at a character part that can be purchased on the character screen.
    # 4: 1
    # 5: 1
    # 6: 60

    def previous_version(self) -> PopnMusicBase:
        return PopnMusicKaimei(self.data, self.config, self.model)

    @classmethod
    def get_settings(cls) -> Dict[str, Any]:
        """
        Return all of our front-end modifiably settings.
        """
        return {
            "bools": [
                {
                    'name': 'Net Taisen',
                    'tip': 'Enable Net Taisen, including win/loss display on song select',
                    'category': 'game_config',
                    'setting': 'enable_net_taisen',
                },
                {
                    "name": "Force Song Unlock",
                    "tip": "Force unlock all songs.",
                    "category": "game_config",
                    "setting": "force_unlock_songs",
                },
            ],
        }

    def get_common_config(self) -> Tuple[Dict[int, int], bool]:
        game_config = self.get_game_config()
        enable_net_taisen = False  # game_config.get_bool('enable_net_taisen')

        # Event phases
        return (
            {
                # Unknown event (0)
                0: 0,
                # Unknown event (0-3)
                1: 3,
                # Unknown event (0)
                2: 0,
                # Enable Net Taisen, including win/loss display on song select (0-1)
                3: 1 if enable_net_taisen else 0,
                # Unknown event (0-1)
                4: 1,
            },
            False,
        )

    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        root = super().format_profile(userid, profile)

        option = root.child("option")
        if option is not None:
            option.add_child(Node.bool("lift", profile.get_bool("lift")))
            option.add_child(Node.s16("lift_rate", profile.get_int("lift_rate")))

        return root

    def unformat_profile(
        self, userid: UserID, request: Node, oldprofile: Profile
    ) -> Profile:
        newprofile = super().unformat_profile(userid, request, oldprofile)

        option = request.child("option")
        if option is not None:
            newprofile.replace_bool("lift", option.child_value("lift"))
            newprofile.replace_int("lift_rate", option.child_value("lift_rate"))

        return newprofile
