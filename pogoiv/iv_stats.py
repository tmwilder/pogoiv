import hashlib
import pprint

class IvStats:
    STAT_ATK_IV = 'atk_iv'
    STAT_DEF_IV = 'def_iv'
    STAT_STAM_IV = 'stam_iv'
    STAT_LEVEL = 'level'
    PERFECTION_PERCENTAGE = 'perfection'

    def __init__(self, level, atk_iv, def_iv, stam_iv, perfection):
        self._level = level
        self._atk_iv = atk_iv
        self._def_iv = def_iv
        self._stam_iv = stam_iv
        self._perfection = perfection

    def __hash__(self):
        """
        Hashes to a level agnostic value for use in equating the same base IVs across different powerups of the same
        Pokemon.
        """
        md5 = hashlib.md5()
        md5.update("a{atk_iv}d{def_iv}s{stam}".format(
            atk_iv=self._atk_iv,
            def_iv=self._def_iv,
            stam=self._stam_iv
        ).encode('ascii'))
        return int(md5.hexdigest(), 16)

    def as_dict(self):
        return {
            IvStats.STAT_ATK_IV: self._atk_iv,
            IvStats.STAT_STAM_IV: self._stam_iv,
            IvStats.STAT_DEF_IV: self._def_iv,
            IvStats.STAT_LEVEL: self._level,
            IvStats.PERFECTION_PERCENTAGE: self._perfection
        }

    def __eq__(self, other):
        """
        Uses to support set operations.
        """
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return pprint.pformat(self.as_dict())
