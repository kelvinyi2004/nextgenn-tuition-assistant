"""
Multilingual detection and language state engine (English, Malay, Chinese).
Preserves natural conversation flow across Malaysian student demographics.
"""

import re
from typing import Optional


AMBIGUOUS_WORDS = {
    "hi",
    "hello",
    "hey",
    "hai",
    "你好",
    "嗨",
    "ok",
    "okay",
    "okok",
    "yes",
    "yep",
    "yaya",
    "thanks",
    "thank you",
    "terima kasih",
}

EN_MARKERS = set(
    "i am me my you your please can could would not available change send schedule "
    "teacher student lesson lessons question ask help next other dates work works "
    "when what how on at for from to with is are this that do does we our".split()
)

MS_MARKERS = set(
    "saya awak anda cikgu boleh tidak tak nak mahu hendak tolong tanya kelas soalan "
    "jadual belajar hari jam pukul setiap bulan minggu isnin selasa rabu khamis "
    "jumaat sabtu ahad ini itu untuk dengan pada esok depan petang pagi malam".split()
)


def is_ambiguous_message(text: str) -> bool:
    """Returns True if the message is too short or generic to reliably infer language."""
    clean = re.sub(r"[^\w\s]", "", str(text or "").strip().lower()).strip()
    if not clean or clean in AMBIGUOUS_WORDS:
        return True
    return bool(re.fullmatch(r"[\d\s]+", clean))


def detect_language(text: str) -> Optional[str]:
    """
    Detects language ('zh', 'en', 'ms') from message text.
    Returns None if text is ambiguous or carries insufficient signal.
    """
    if is_ambiguous_message(text):
        return None

    raw = str(text or "")

    # Chinese character presence is definitive
    if re.search(r"[\u4e00-\u9fff]", raw):
        return "zh"

    words = set(re.findall(r"[a-z]+", raw.lower()))
    en_score = len(words & EN_MARKERS)
    ms_score = len(words & MS_MARKERS)

    if en_score >= 2 and en_score > ms_score:
        return "en"
    if ms_score >= 2 and ms_score > en_score:
        return "ms"

    return None
