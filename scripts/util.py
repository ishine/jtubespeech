import re
from datetime import datetime as dt
from pathlib import Path
import subprocess

# YouTube video URL


def make_video_url(videoid: str) -> str:
    return f"https://www.youtube.com/watch?v={videoid}"


# YouTube Search URL
def make_query_url(query: str) -> str:
    q = query.rstrip("\n").strip(" ").replace(" ", "+")
    return f"https://www.youtube.com/results?search_query={q}&sp=EgQQASgB"


# Wikipedia dump file URL
def make_dump_url(lang: str) -> str:
    return f"https://dumps.wikimedia.org/{lang}wiki/latest/{lang}wiki-latest-pages-articles-multistream-index.txt.bz2"


def make_basename(videoid: str) -> str:
    return str(Path(videoid[:8]) / videoid)


def count_total_second(t: dt) -> float:
    return t.hour * 3600 + t.minute * 60 + t.second * 1 + t.microsecond * 1e-6


def obtain_channelid(videoid: str) -> str:
    fn_html = Path("temp.html")

    # download
    url = make_video_url(videoid)
    subprocess.run(f"wget {url} -O {fn_html}", shell=True)

    # obtain ID
    html = "".join(open(fn_html, "r").readlines())
    try:
        # only Japanese
        channelid = re.findall(
            r"canonicalBaseUrl\":\"/channel/([\w\_\-]+?)\"\}\},\"subscriberCountText\":\{\"accessibility\":\{\"accessibilityData\":\{\"label\":\"チャンネル登録者数", html)[0]
    except:
        channelid = None

    return channelid


def vtt2txt(vtt: list) -> list:
    txt, is_started = [], False

    for v in vtt:
        m = re.match(
            r'(\d+\:\d+\:\d+\.\d+) --> (\d+\:\d+\:\d+\.\d+)', v.strip("\n"))
        if m is not None:
            st = count_total_second(dt.strptime(m.groups()[0], "%H:%M:%S.%f"))
            et = count_total_second(dt.strptime(m.groups()[1], "%H:%M:%S.%f"))
            txt.append([st, et, ""])
            is_started = True
        elif is_started:
            v = _normalize_text(v)
            if len(v) == 0:
                is_started = False
            else:
                txt[-1][-1] += " " + v

    # refine
    txt_refined = []
    for t in txt:
        x = _normalize_text(t[2])
        if len(x) > 0:
            txt_refined.append([t[0], t[1], x])

    return txt_refined


def _normalize_text(txt: str) -> str:
    return txt.replace("\n", " ").replace("　", " ").replace("  ", " ").strip(" ").strip("\t").replace("»", "").replace("«", "")


def autovtt2txt(vtt: list) -> list:
    txt = []

    for idx, v in enumerate(vtt):
        m = re.match(
            r'(\d+\:\d+\:\d+\.\d+) --> (\d+\:\d+\:\d+\.\d+) align:.+', v.strip("\n"))
        if m is None:
            continue

        st = count_total_second(dt.strptime(m.groups()[0], "%H:%M:%S.%f"))
        et = count_total_second(dt.strptime(m.groups()[1], "%H:%M:%S.%f"))

        text_line = ""
        for line in [vtt[idx+1], vtt[idx+2]]:
            line = _normalize_text(line)
            if len(line) == 0 or "<" not in line:
                continue

            head = line.split("<")[0]
            body = re.sub(f"^{head}", "", line)
            m = re.findall(r"<\d+\:\d+\:\d+\.\d+><c>(.+?)</c>", body)
            if len(m) != 0:
                text_line += head + "".join(m)

        if len(text_line) > 0:
            txt.append([st, et, text_line])

    # refine
    txt_refined = []
    for t in txt:
        x = _normalize_text(t[2])
        if len(x) > 0:
            txt_refined.append([t[0], t[1], x])

    return txt_refined


def get_subtitle_language(response_youtube):
    lang_code = ["aa", "ab", "ace", "ady", "af", "ak", "als", "alt", "am", "an", "ang", "ar", "arc", "ary", "arz", "as", "ast", "atj", "av", "avk", "awa", "ay", "az", "azb", "ba", "ban", "bar", "bat-smg", "bcl", "be", "be-tarask", "bg", "bh", "bi", "bjn", "bm", "bn", "bo", "bpy", "br", "bs", "bug", "bxr", "ca", "cbk-zam", "cdo", "ce", "ceb", "ch", "cho", "chr", "chy", "ckb", "co", "cr", "crh", "cs", "csb", "cu", "cv", "cy", "da", "de", "din", "diq", "dsb", "dty", "dv", "dz", "ee", "el", "eml", "en", "eo", "es", "et", "eu", "ext", "fa", "ff", "fi", "fiu-vro", "fj", "fo", "fr", "frp", "frr", "fur", "fy", "ga", "gag", "gan", "gcr", "gd", "gl", "glk", "gn", "gom", "gor", "got", "gu", "gv", "ha", "hak", "haw", "he", "hi", "hif", "ho", "hr", "hsb", "ht", "hu", "hy", "hyw", "hz", "ia", "id", "ie", "ig", "ii", "ik", "ilo", "inh", "io", "is", "it", "iu", "ja", "jam", "jbo", "jv", "ka", "kaa", "kab", "kbd", "kbp", "kg", "ki", "kj", "kk", "kl", "km", "kn", "ko", "koi", "kr", "krc", "ks", "ksh", "ku", "kv", "kw", "ky", "la", "lad", "lb", "lbe", "lez", "lfn", "lg", "li", "lij", "lld", "lmo", "ln", "lo", "lrc", "lt", "ltg", "lv", "mad", "mai", "map-bms", "mdf", "mg", "mh", "mhr", "mi", "min", "mk", "ml", "mn", "mni", "mnw", "mr", "mrj", "ms", "mt", "mus", "mwl", "my", "myv", "mzn", "na", "nah", "nap", "nds", "nds-nl", "ne", "new", "ng", "nia", "nl", "nn", "no", "nov", "nqo", "nrm", "nso", "nv", "ny", "oc", "olo", "om", "or", "os", "pa", "pag", "pam", "pap", "pcd", "pdc", "pfl", "pi", "pih", "pl", "pms", "pnb", "pnt", "ps", "pt", "qu", "rm", "rmy", "rn", "ro", "roa-rup", "roa-tara", "ru", "rue", "rw", "sa", "sah", "sat", "sc", "scn", "sco", "sd", "se", "sg", "sh", "shn", "si", "simple", "sk", "skr", "sl", "sm", "smn", "sn", "so", "sq", "sr", "srn", "ss", "st", "stq", "su", "sv", "sw", "szl", "szy", "ta", "tay", "tcy", "te", "tet", "tg", "th", "ti", "tk", "tl", "tn", "to", "tpi", "tr", "trv", "ts", "tt", "tum", "tw", "ty", "tyv", "udm", "ug", "uk", "ur", "uz", "ve", "vec", "vep", "vi", "vls", "vo", "wa", "war", "wo", "wuu", "xal", "xh", "xmf", "yi", "yo", "za", "zea", "zh", "zh-classical", "zh-min-nan",
                 "zh-yue", "zu"]

    sub_type = None
    subtitle = {"auto": [], "sub": []}
    for r in response_youtube.split("\n"):
        if r.startswith("Available automatic captions for"):
            sub_type = "auto"
        elif r.startswith("Available subtitles for"):
            sub_type = "sub"
        elif sub_type is not None:
            lang = r.split(" ")[0].lower()
            if lang in lang_code:
                subtitle[sub_type].append(lang)

    return subtitle["auto"], subtitle["sub"]

def load_audio_language_mapping():
    mapping = {
        'ab': 0,
        'af': 1,
        'am': 2,
        'ar': 3,
        'as': 4,
        'az': 5,
        'ba': 6,
        'be': 7,
        'bg': 8,
        'bn': 9,
        'bo': 10,
        'br': 11,
        'bs': 12,
        'ca': 13,
        'ceb': 14,
        'cs': 15,
        'cy': 16,
        'da': 17,
        'de': 18,
        'el': 19,
        'en': 20,
        'eo': 21,
        'es': 22,
        'et': 23,
        'eu': 24,
        'fa': 25,
        'fi': 26,
        'fo': 27,
        'fr': 28,
        'gl': 29,
        'gn': 30,
        'gu': 31,
        'gv': 32,
        'ha': 33,
        'haw': 34,
        'hi': 35,
        'hr': 36,
        'ht': 37,
        'hu': 38,
        'hy': 39,
        'ia': 40,
        'id': 41,
        'is': 42,
        'it': 43,
        'iw': 44,
        'ja': 45,
        'jw': 46,
        'ka': 47,
        'kk': 48,
        'km': 49,
        'kn': 50,
        'ko': 51,
        'la': 52,
        'lb': 53,
        'ln': 54,
        'lo': 55,
        'lt': 56,
        'lv': 57,
        'mg': 58,
        'mi': 59,
        'mk': 60,
        'ml': 61,
        'mn': 62,
        'mr': 63,
        'ms': 64,
        'mt': 65,
        'my': 66,
        'ne': 67,
        'nl': 68,
        'nn': 69,
        'no': 70,
        'oc': 71,
        'pa': 72,
        'pl': 73,
        'ps': 74,
        'pt': 75,
        'ro': 76,
        'ru': 77,
        'sa': 78,
        'sco': 79,
        'sd': 80,
        'si': 81,
        'sk': 82,
        'sl': 83,
        'sn': 84,
        'so': 85,
        'sq': 86,
        'sr': 87,
        'su': 88,
        'sv': 89,
        'sw': 90,
        'ta': 91,
        'te': 92,
        'tg': 93,
        'th': 94,
        'tk': 95,
        'tl': 96,
        'tr': 97,
        'tt': 98,
        'uk': 99,
        'ur': 100,
        'uz': 101,
        'vi': 102,
        'war': 103,
        'yi': 104,
        'yo': 105,
        'zh': 106
    }
    return mapping

def load_text_language_mapping():
    
    # this dictionary is the same as the model.config.id2label in check_target_language_video_title method in the detect_target_language module
    id_to_lang_mapping = {
        0: 'Arabic',
        1: 'Basque',
        2: 'Breton',
        3: 'Catalan',
        4: 'Chinese_China',
        5: 'Chinese_Hongkong',
        6: 'Chinese_Taiwan',
        7: 'Chuvash',
        8: 'Czech',
        9: 'Dhivehi',
        10: 'Dutch',
        11: 'English',
        12: 'Esperanto',
        13: 'Estonian',
        14: 'French',
        15: 'Frisian',
        16: 'Georgian',
        17: 'German',
        18: 'Greek',
        19: 'Hakha_Chin',
        20: 'Indonesian',
        21: 'Interlingua',
        22: 'Italian',
        23: 'Japanese',
        24: 'Kabyle',
        25: 'Kinyarwanda',
        26: 'Kyrgyz',
        27: 'Latvian',
        28: 'Maltese',
        29: 'Mongolian',
        30: 'Persian',
        31: 'Polish',
        32: 'Portuguese',
        33: 'Romanian',
        34: 'Romansh_Sursilvan',
        35: 'Russian',
        36: 'Sakha',
        37: 'Slovenian',
        38: 'Spanish',
        39: 'Swedish',
        40: 'Tamil',
        41: 'Tatar',
        42: 'Turkish',
        43: 'Ukranian',
        44: 'Welsh'
    }

  # this dictionary is the mapping from the name of the language to the language code of the language
    lang_to_code_mapping = {
        'Arabic': 'ar',
        'Basque': 'eu',
        'Breton': 'br',
        'Catalan': 'ca',
        'Chinese_China': 'zh',
        'Chinese_Hongkong': 'zh',
        'Chinese_Taiwan': 'zh',
        'Chuvash': 'cv',
        'Czech': 'cs',
        'Dhivehi': 'dv',
        'Dutch': 'nl',
        'English': 'en',
        'Esperanto': 'eo',
        'Estonian': 'et',
        'French': 'fr',
        'Frisian': 'fy',
        'Georgian': 'ka',
        'German': 'de',
        'Greek': 'el',
        'Hakha_Chin': '-',
        'Indonesian': 'id',
        'Interlingua': 'ia',
        'Italian': 'it',
        'Japanese': 'ja',
        'Kabyle': 'kl',
        'Kinyarwanda': 'rw',
        'Kyrgyz': 'ky',
        'Latvian': 'lv',
        'Maltese': 'mt',
        'Mongolian': 'mn',
        'Persian': 'fa',
        'Polish': 'pl',
        'Portuguese': 'pt',
        'Romanian': 'ro',
        'Romansh_Sursilvan': 'rm',
        'Russian': 'ru',
        'Sakha': '-',
        'Slovenian': 'sl',
        'Spanish': 'es',
        'Swedish': 'sv',
        'Tamil': 'ta',
        'Tatar': 'tt',
        'Turkish': 'tr',
        'Ukranian': 'uk',
        'Welsh': 'cy'
    }

    id_to_code_mapping = {k:j for k, j in zip(id_to_lang_mapping.keys(), lang_to_code_mapping.values())}
    return id_to_code_mapping