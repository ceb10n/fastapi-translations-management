from enum import Enum, unique


@unique
class Languages(Enum):
    """Languages that the FastAPI documentation has translation.

    For more information about the languages, check `FastAPI docs`_.

    .. _FastAPI docs: https://github.com/fastapi/fastapi/tree/master/docs
    """

    az = "az"
    bn = "bn"
    de = "de"
    em = "em"
    es = "es"
    fa = "fa"
    fr = "fr"
    he = "he"
    hu = "hu"
    id = "id"
    it = "it"
    ja = "ja"
    ko = "ko"
    nl = "nl"
    pl = "pl"
    pt = "pt"
    ru = "ru"
    tr = "tr"
    uk = "uk"
    ur = "ur"
    vi = "vi"
    yo = "yo"
    zh = "zh"
    zh_hant = "zh-hant"
