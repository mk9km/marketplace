import enum

class EnumBase(enum.Enum):

    @classmethod
    def from_value(cls, value):
        for member in cls:
            if member.value == value:
                return member
        return None
