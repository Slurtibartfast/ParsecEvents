from enum import Enum


def description(self, locale: str = None) -> str:
    result = str(self)
    locale = locale.lower() if locale else ""
    if hasattr(self, "_desc_"):
        if locale in self._desc_:
            result = self._desc_[locale]
        elif (locale != "") and ("" in self._desc_):
            result = self._desc_[""]

    return result


def describe(self, value: str, locale: str = None):
    locale = locale.lower() if locale else ""
    if not hasattr(self, "_desc_"):
        self._desc_ = {locale: value}
    else:
        self._desc_[locale] = value

    if not hasattr(self, "description"):
        self.__class__.description = description


def desc(obj, locale: str = None) -> str:
    return obj.description(locale) if hasattr(obj, "description") else str(obj)


class EnumEx(Enum):
    Test = 0,
    Test1 = 1,
    Test2 = 3


class EnumEx2(Enum):
    Test = 0,
    Test1 = 1,
    Test2 = 3


describe(EnumEx.Test, "this is a test")
describe(EnumEx.Test, "это тест", "ru")
describe(EnumEx.Test1, "this is another test")
describe(EnumEx.Test1, "это другой тест", "ru")

"""
print(EnumEx.Test.description())
print(EnumEx.Test.description("Ru"))
print(EnumEx.Test1.description())
print(EnumEx.Test1.description("rU"))
"""

print(desc(EnumEx.Test1))
#print(desc(EnumEx2.Test1))
print(EnumEx2.Test1.description())
