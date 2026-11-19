import copy
import json
import math
import os
import random
import sys
import traceback
import pygame

from dave_story import DAVE_STORY
from tyrone_story import TYRONE_STORY

pygame.init()
try:
    pygame.mixer.init()
except Exception as e:
    print(f"[AUDIO] Mixer init skipped: {e}")

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("i-Attorney: Corporate Justice")
clock = pygame.time.Clock()

# Colors & Fonts
PURE_BLACK = (0, 0, 0)
BLACK = (12, 16, 28)
WHITE = (255, 255, 255)
NAVY = (20, 34, 68)
DARK_NAVY = (14, 22, 46)
BLUE_ACCENT = (12, 92, 188)
TITLE_BTN_BLUE = (10, 78, 162)
TITLE_BTN_HOVER = (22, 108, 212)
GOLD = (255, 200, 50)
ORANGE_SPARK = (230, 105, 20)
CYAN = (70, 220, 245)
GREEN = (75, 215, 120)
RED = (235, 65, 75)
CRIMSON = (150, 22, 36)
PURPLE_ACCENT = (175, 110, 245)
GRAY = (150, 160, 175)

font_shout = pygame.font.SysFont("impact,arialblack,arial", 128, bold=True)
font_title = pygame.font.SysFont("arial", 44, bold=True)
font_menu = pygame.font.SysFont("georgia,timesnewroman", 26, bold=True)
font_logo_word = pygame.font.SysFont("georgia,timesnewroman", 54, bold=True)
font_logo_i = pygame.font.SysFont("georgia,timesnewroman", 88, bold=True)
font_sub = pygame.font.SysFont("consolas", 23, bold=True)
font_main = pygame.font.SysFont("consolas", 18, bold=True)
font_name = pygame.font.SysFont("consolas", 16, bold=True)
font_small = pygame.font.SysFont("consolas", 14, bold=True)

_SCALED_FONT_CACHE = {}


def get_sized_font(base_font, size):
    key = (id(base_font), size)
    if key not in _SCALED_FONT_CACHE:
        _SCALED_FONT_CACHE[key] = pygame.font.SysFont("consolas", size, bold=True)
    return _SCALED_FONT_CACHE[key]


def render_fitted_line(text, font, color, max_width, min_size=11):
    """Renders a single line of text, scaling down the font size if needed so it never exceeds max_width."""
    if font.size(text)[0] <= max_width:
        return font.render(text, True, color)

    start_size = font.get_height()
    for sz in range(start_size - 1, min_size - 1, -1):
        test_font = get_sized_font(font, sz)
        if test_font.size(text)[0] <= max_width:
            return test_font.render(text, True, color)

    fallback_font = get_sized_font(font, min_size)
    trimmed = text
    while len(trimmed) > 3 and fallback_font.size(trimmed + "...")[0] > max_width:
        trimmed = trimmed[:-1]
    return fallback_font.render(trimmed + "...", True, color)


def _wrap_lines_for_font(text, max_width, font):
    paragraphs = text.split("\n")
    lines = []
    for para in paragraphs:
        words = para.split(" ")
        current = ""
        for word in words:
            if not word:
                continue
            candidate = f"{current} {word}".strip() if current else word
            if font.size(candidate)[0] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                    current = ""
                if font.size(word)[0] <= max_width:
                    current = word
                else:
                    chunk = ""
                    for ch in word:
                        if font.size(chunk + ch)[0] <= max_width:
                            chunk += ch
                        else:
                            if chunk:
                                lines.append(chunk)
                            chunk = ch
                    current = chunk
        if current or not words:
            lines.append(current)
    return lines


def draw_text_wrapped(
    surface,
    text,
    x,
    y,
    max_width,
    font,
    color=WHITE,
    max_height=None,
    min_font_size=12,
    line_spacing=4,
    full_reference_text=None,
    center_x=None
):
    """Wraps text inside max_width and auto-scales font size if max_height is provided so text never overflows."""
    if not text:
        return y

    chosen_font = font
    chosen_spacing = line_spacing
    measure_text = full_reference_text if full_reference_text is not None else text

    if max_height is not None and max_height > 0:
        start_size = font.get_height()
        for sz in range(start_size, min_font_size - 1, -1):
            test_font = font if sz == start_size else get_sized_font(font, sz)
            test_spacing = max(2, line_spacing - (start_size - sz) // 3)
            test_lines = _wrap_lines_for_font(measure_text, max_width, test_font)
            total_h = len(test_lines) * (test_font.get_height() + test_spacing) - test_spacing
            if total_h <= max_height:
                chosen_font = test_font
                chosen_spacing = test_spacing
                break
        else:
            chosen_font = get_sized_font(font, min_font_size)
            chosen_spacing = 2

    render_lines = _wrap_lines_for_font(text, max_width, chosen_font)
    step_y = chosen_font.get_height() + chosen_spacing
    cur_y = y

    for line in render_lines:
        if max_height is not None and (cur_y + chosen_font.get_height() > y + max_height):
            break
        line_surf = chosen_font.render(line, True, color)
        draw_x = (center_x - line_surf.get_width() // 2) if center_x is not None else x
        surface.blit(line_surf, (draw_x, cur_y))
        cur_y += step_y

    return cur_y


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_FILE = os.path.join(BASE_DIR, "assets.json")
SAVE_FILE = os.path.join(BASE_DIR, "savegame.json")

CASE_THEMES = [
    {
        "accent": CYAN,
        "tint": (15, 45, 85, 38),
        "card_bg": (12, 26, 52),
        "tag": "PHASE I • DIGITAL FORENSICS & DATA INTEGRITY"
    },
    {
        "accent": ORANGE_SPARK,
        "tint": (75, 35, 12, 36),
        "card_bg": (36, 20, 14),
        "tag": "PHASE II • INTERNAL CONTROLS & COMPLIANCE"
    },
    {
        "accent": GREEN,
        "tint": (14, 58, 38, 36),
        "card_bg": (12, 34, 24),
        "tag": "PHASE III • WHISTLEBLOWER PROTECTION"
    },
    {
        "accent": PURPLE_ACCENT,
        "tint": (48, 22, 78, 40),
        "card_bg": (28, 16, 46),
        "tag": "PHASE IV • OFFSHORE TRAILS & SELF-DEALING"
    },
    {
        "accent": GOLD,
        "tint": (72, 52, 10, 42),
        "card_bg": (38, 28, 12),
        "tag": "FINAL PHASE • FIDUCIARY DUTY & THE VERDICT"
    }
]

DEFAULT_MANIFEST = {
    "folders": {
        "root": "assets",
        "bg": "assets/bg",
        "char": "assets/char",
        "icon": "assets/icon",
        "sounds": "assets/sounds"
    },
    "app_icon": "app_icon.png",
    "sounds": {
        "bang": "bang.wav",
        "speak": "speak.wav",
        "hold_it": "hold_it.wav",
        "objection": "objection.wav",
        "take_that": "take_that.wav",
        "whoops": "whoops.wav",
        "realization": "realization.wav",
        "testimony": "testimony.wav"
    },
    "backgrounds": {
        "courtroom": {"file": "bg_courtroom.png", "size": [800, 600]},
        "title_bg": {"file": "title_bg.png", "size": [800, 600]},
        "title_logo": {"file": "title_logo.png", "size": [560, 230]}
    },
    "shouts": {
        "OBJECTION!": {"file": "objection.png", "size": [790, 560]},
        "TAKE THAT!": {"file": "take_that.png", "size": [790, 560]},
        "HOLD IT!": {"file": "hold_it.png", "size": [790, 560]}
    },
    "characters": {
        "Dave": {
            "folder": "dave",
            "size": [430, 410],
            "poses": {
                "idle": "dave.png",
                "point": "dave_point.png",
                "smile": "dave_smile.png",
                "think": "dave_think.png"
            }
        },
        "Tyrone": {
            "folder": "tyrone",
            "size": [430, 410],
            "poses": {
                "idle": "tyrone.png",
                "point": "tyrone_point.png",
                "smile": "tyrone_smile.png",
                "think": "tyrone_think.png"
            }
        },
        "Kendall": {
            "folder": "kendall",
            "size": [430, 410],
            "poses": {
                "idle": "kendall.png",
                "point": "kendall_point.png",
                "smile": "kendall_smile.png",
                "think": "kendall_think.png"
            }
        },
        "Elijah": {
            "folder": "elijah",
            "size": [430, 410],
            "poses": {
                "idle": "elijah.png",
                "point": "elijah_point.png",
                "smile": "elijah_smile.png",
                "think": "elijah_think.png"
            }
        },
        "Dwyane": {
            "folder": "dwyane",
            "size": [430, 410],
            "poses": {
                "idle": "dwyane.png",
                "sigh": "dwyane_sigh.png",
                "stare": "dwyane_stare.png"
            }
        },
        "CFO": {
            "folder": "cfo",
            "size": [430, 410],
            "poses": {
                "idle": "cfo.png",
                "angry": "cfo_angry.png",
                "laugh": "cfo_laugh.png",
                "worried": "cfo_worried.png"
            }
        },
        "Accountant": {
            "folder": "accountant",
            "size": [430, 410],
            "poses": {
                "idle": "accountant.png",
                "relief": "accountant_relief.png",
                "shocked": "accountant_shocked.png",
                "smile": "accountant_smile.png",
                "worried": "accountant_worried.png"
            }
        },
        "Employee": {
            "folder": "employee",
            "size": [430, 410],
            "poses": {
                "idle": "employee.png",
                "relief": "employee_relief.png",
                "shocked": "employee_shocked.png",
                "smile": "employee_smile.png",
                "worried": "employee_worried.png"
            }
        }
    }
}

STORY_REGISTRY = {
    "Dave": DAVE_STORY,
    "Tyrone": TYRONE_STORY
}

CREDITS_PAGES = [
    {
        "page": 1,
        "header": "CREATOR & DIRECTOR",
        "lines": ["Game Made by: Adi De Vera"],
        "cast": []
    },
    {
        "page": 2,
        "header": "SCREENPLAY & STORY",
        "lines": ["Story by: Adi De Vera (Chatgpt)"],
        "cast": []
    },
    {
        "page": 3,
        "header": "PROGRAMMING & ENGINE",
        "lines": ["Code by: Adi De Vera (Gemini)"],
        "cast": []
    },
    {
        "page": 4,
        "header": "ART & CHARACTER DESIGN",
        "lines": ["Character Designs by: Adi De Vera (Gemini)"],
        "cast": []
    },
    {
        "page": 5,
        "header": "LEAD COUNSEL CAST",
        "lines": [],
        "cast": [
            {"char": "Dave", "file": "dave.png", "credit": "Dave Bartolabac as Attorney Dave"},
            {"char": "Tyrone", "file": "tyrone.png", "credit": "Tyrone Niere as Attorney Tyrone"}
        ]
    },
    {
        "page": 6,
        "header": "THE BENCH & EXECUTIVE CAST",
        "lines": [],
        "cast": [
            {"char": "Dwyane", "file": "dwyane.png", "credit": "Dwyane Sido as Judge Dwyane"},
            {"char": "Elijah", "file": "elijah.png", "credit": "Elijah Bes as Businessman Elijah"}
        ]
    },
    {
        "page": 7,
        "header": "CORPORATE & FINANCE CAST",
        "lines": [],
        "cast": [
            {"char": "Kendall", "file": "kendall.png", "credit": "Kendall Maputi as Businessman Kendall"},
            {"char": "Accountant", "file": "accountant.png", "credit": "James inopia as Accountant"}
        ]
    },
    {
        "page": 8,
        "header": "STAFF & EXECUTIVE CAST",
        "lines": [],
        "cast": [
            {"char": "Employee", "file": "employee.png", "credit": "Dion Rojo as Employee"},
            {"char": "CFO", "file": "cfo.png", "credit": "Paul Busgano as CFO"}
        ]
    },
    {
        "page": 9,
        "header": "i-ATTORNEY: CORPORATE JUSTICE",
        "lines": ["Thank you Everyone For Playing!!"],
        "cast": []
    }
]

ENDINGS_DB = {
    "DAVE_VICTORY": {
        "banner": "ENDING 1 OF 3: DAVE'S VICTORY",
        "title": "THE UNBROKEN SHIELD",
        "secret": False,
        "color": CYAN,
        "summary": (
            "Dave dismantles the prosecution's case and proves the CFO orchestrated the entire embezzlement scheme. "
            "Elijah is fully acquitted, keeps 100% control of EK Global, and closes the $150M Series D funding round—"
            "while Kendall is stripped of his board seat, hit with regulatory sanctions, and forced out in disgrace."
        ),
        "dialogue": [
            ("Elijah", "We did it, Dave! The court cleared my name, our Series D investors just wired the $150 million, and all 300 engineers keep their jobs!", "smile"),
            ("Elijah", "Tomorrow morning I'm restructuring the board, expanding our R&D lab, and taking EK Global to the top!", "smile"),
            ("Kendall", "N-No... My board seat, my voting shares, my reputation—gone in a single gavel strike! You ruined me, Dave!", "think"),
            ("Tyrone", "Tch... You shielded your client cleanly, Dave. Kendall will spend the next decade fighting shareholder lawsuits while Elijah takes the whole empire.", "think"),
            ("Dave", "Justice protected the people who actually build this company, Tyrone. Elijah earned every bit of his second chance!", "point"),
            ("Dwyane", "Mr. Elijah is acquitted of all charges and retains full executive authority. Mr. Kendall is barred from corporate office, and the CFO is remanded into custody. Court is adjourned!", "stare")
        ]
    },
    "TYRONE_VICTORY": {
        "banner": "ENDING 2 OF 3: TYRONE'S VICTORY",
        "title": "THE STRATEGIST'S CHECKMATE",
        "secret": False,
        "color": GOLD,
        "summary": (
            "Through razor-sharp cross-examination, Tyrone clears Kendall of every charge and pins the fraud on the CFO. "
            "Kendall wins sole executive control of EK Global, secures lucrative institutional partnerships, and dominates the market—"
            "while Elijah is removed as CEO, loses his voting shares, and faces harsh federal penalties."
        ),
        "dialogue": [
            ("Kendall", "Flawless victory, Tyrone! The board just voted me sole CEO, institutional funds are lining up at the door, and EK Global's valuation just hit an all-time high!", "smile"),
            ("Kendall", "With dead weight cleared out of the executive suite, nothing stands in the way of our global expansion!", "smile"),
            ("Elijah", "Wait—I'm being removed from the company I coded from scratch?! My shares are frozen, and I'm facing SEC sanctions?!", "think"),
            ("Dave", "Objection! You got Kendall acquitted, Tyrone—and left Elijah to take the fall for a company he built with his own hands!", "point"),
            ("Tyrone", "The record was crystal clear, Dave. Kendall walks away with the entire enterprise, while your client pays the price for negligence.", "smile"),
            ("Dwyane", "Mr. Kendall is cleared of all liability and confirmed as sole Chief Executive. Mr. Elijah is removed from management, and the CFO stands indicted. Court is adjourned!", "stare")
        ]
    },
    "TRUE_ENDING": {
        "banner": "SECRET ENDING: THE TRUE VERDICT",
        "title": "THE PRICE OF GREED",
        "secret": True,
        "color": GREEN,
        "summary": (
            "Choosing truth over blind client loyalty, Dave and Tyrone set aside their rivalry to expose "
            "the complete chain of corruption. The CFO is indicted for masterminding the financial fraud, "
            "while both Elijah and Kendall are held legally and ethically accountable—sparking true reform at EK Global."
        ),
        "dialogue": [
            ("Dave", "Being your counsel never meant helping you bury shortcuts, Elijah. Real loyalty means standing beside you when the truth hurts!", "point"),
            ("Tyrone", "And for the first time in our careers, Dave, our closing arguments converged on the exact same theorem.", "smile"),
            ("Elijah", "...Kendall and I chased a billion-dollar headline so hard we forgot the garage where we wrote our first line of code.", "think"),
            ("Elijah", "I signed off on inflated growth numbers to keep investors happy. I'll face the SEC regulators with my eyes open.", "think"),
            ("Kendall", "No more vanity metrics, no more dismissed HR tickets, and no more closed-door overrides. If EK Global survives, we rebuild in broad daylight.", "think"),
            ("Dwyane", "The CFO is indicted for grand embezzlement, and both founding partners shall submit to independent compliance oversight. Justice is served!", "stare")
        ]
    }
}


def build_wrong_evidence_dialogue(attorney_name, witness_name, ev_name, remaining_hp):
    """Generates unique, in-character dialogue lines and fitting poses when counsel presents irrelevant evidence."""
    is_game_over = (remaining_hp <= 0)

    if attorney_name == "Dave":
        opener = random.choice([
            f"Look closely at this exhibit: {ev_name}! Doesn't this tear a hole right through your story?!",
            f"Read every line of {ev_name}! This proves your testimony doesn't add up!",
            f"Explain {ev_name} to this courtroom! You can't talk your way around hard paper!"
        ])
    else:
        opener = random.choice([
            f"Examine {ev_name} under oath. That exhibit directly invalidates your previous statement.",
            f"Your timeline collapses the moment we cross-reference {ev_name}. Care to revise your testimony?",
            f"Let the record reflect {ev_name}. Explain the discrepancy—if you can."
        ])

    witness_replies = {
        "Kendall": [
            ("Nice dramatic finger-point, Counselor—too bad that exhibit has zero connection to what I just testified.", "smile"),
            ("Are you seriously waving that around in front of institutional observers? It doesn't contradict a syllable I said.", "smile"),
            ("I expected sharper due diligence from a trial attorney. That document proves nothing about my statement.", "think")
        ],
        "CFO": [
            ("With respect, Counselor, that exhibit doesn't even share a fiscal quarter with the statement on the stand!", "laugh"),
            ("You're grasping at random binders now. Not a single line on that page refutes my testimony.", "laugh"),
            ("If that's the sharpest arrow in your quiver, this cross-examination is already over.", "angry")
        ],
        "Elijah": [
            ("Wait—why are you showing me that? That document doesn't have anything to do with what I just said!", "think"),
            ("I'm trying to answer honestly, Counselor, but that exhibit doesn't contradict my statement at all!", "think"),
            ("Look at the dates on that file again—it doesn't line up with the testimony you're challenging!", "point")
        ],
        "Accountant": [
            ("U-Um, pardon me, Counselor, but if you check the reference code, that exhibit doesn't actually relate to what I just testified...", "worried"),
            ("I double-checked every ledger myself, and... well, that document doesn't contradict my statement at all.", "worried"),
            ("A-Are you sure you pulled the right folder? That exhibit covers a completely different issue.", "shocked")
        ],
        "Employee": [
            ("I'm really trying to help the court find the truth, Counselor, but that document doesn't match what I just said...", "worried"),
            ("Please check the Court Record again—that exhibit isn't connected to the part of my testimony you're pressing!", "worried"),
            ("Oh... that's not the file that proves what happened. Look closely at the details in my statement!", "shocked")
        ]
    }
    w_reply, w_pose = random.choice(witness_replies.get(
        witness_name,
        [("That exhibit has zero bearing on my testimony, Counselor.", "idle")]
    ))

    if is_game_over:
        if attorney_name == "Dave":
            judge_warn = "Enough, Mr. Dave! Passion is no substitute for relevance—you have exhausted the bench's patience!"
            judge_end = "Your defense has collapsed under its own reckless objections! This court is adjourned!"
            counsel_react = ("Dave", "(No... I pushed too hard without matching the right proof... I let Elijah down...)", "think")
        else:
            judge_warn = "Enough, Mr. Tyrone! Even a grandmaster loses the match when he sacrifices every piece on the board!"
            judge_end = "Your credibility with this bench is completely depleted! This court is adjourned!"
            counsel_react = ("Tyrone", "(Tch... A fatal miscalculation in sequence... I overplayed my hand before the endgame...)", "think")

        return [
            (attorney_name, opener, "point"),
            (witness_name, w_reply, w_pose),
            ("Dwyane", judge_warn, "stare", "whoops"),
            counsel_react,
            ("Dwyane", judge_end, "stare")
        ]

    judge_penalties = [
        (f"This is a court of law, {attorney_name}, not a guessing game! Penalty assessed! ({remaining_hp} credibility remaining)", "sigh"),
        (f"Connect your exhibits to the testimony before shouting, {attorney_name}! Penalty issued! ({remaining_hp} credibility remaining)", "stare"),
        (f"Irrelevant filing! One more careless swing like that and you'll be arguing from the hallway, {attorney_name}! ({remaining_hp} remaining)", "stare")
    ]
    chosen_penalty, judge_pose = random.choice(judge_penalties)

    if attorney_name == "Dave":
        follow_up = ("Dave", "(Calm down, Dave! Read the witness's exact words and match them to the right piece of evidence!)", "think")
    else:
        follow_up = ("Tyrone", "(Sloppy, Tyrone. Re-read the testimony line by line and strike only where the logic fractures.)", "think")

    return [
        (attorney_name, opener, "point"),
        (witness_name, w_reply, w_pose),
        ("Dwyane", chosen_penalty, judge_pose, "whoops"),
        follow_up
    ]


def get_case_theme(ch_idx):
    return CASE_THEMES[ch_idx % len(CASE_THEMES)]


def get_viewport_rect(win_w, win_h):
    if win_w <= 0 or win_h <= 0:
        return pygame.Rect(0, 0, WIDTH, HEIGHT)
    scale = min(win_w / WIDTH, win_h / HEIGHT)
    scaled_w = max(1, int(WIDTH * scale))
    scaled_h = max(1, int(HEIGHT * scale))
    offset_x = (win_w - scaled_w) // 2
    offset_y = (win_h - scaled_h) // 2
    return pygame.Rect(offset_x, offset_y, scaled_w, scaled_h)


def screen_to_virtual(pos, win_w, win_h):
    vp = get_viewport_rect(win_w, win_h)
    vx = int((pos[0] - vp.x) * WIDTH / vp.width)
    vy = int((pos[1] - vp.y) * HEIGHT / vp.height)
    vx = max(0, min(WIDTH - 1, vx))
    vy = max(0, min(HEIGHT - 1, vy))
    return (vx, vy)


def load_progress():
    default_data = {
        "last_run": None,
        "certificates": [],
        "endings": []
    }
    if not os.path.exists(SAVE_FILE):
        return default_data
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        default_data.update(data)
    except Exception:
        pass
    return default_data


def save_progress(data):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[SAVE] Could not write savegame.json: {e}")


class AssetManager:
    def __init__(self, manifest_path=MANIFEST_FILE):
        if not os.path.exists(manifest_path):
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_MANIFEST, f, indent=2)

        with open(manifest_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        manifest_updated = False
        bgs_block = self.data.setdefault("backgrounds", {})
        for bkey, bdef in DEFAULT_MANIFEST["backgrounds"].items():
            if bkey not in bgs_block:
                bgs_block[bkey] = copy.deepcopy(bdef)
                manifest_updated = True

        shouts_block = self.data.setdefault("shouts", {})
        for skey, sdef in DEFAULT_MANIFEST["shouts"].items():
            if skey not in shouts_block:
                shouts_block[skey] = copy.deepcopy(sdef)
                manifest_updated = True
            elif shouts_block[skey].get("size") in ([540, 220], [760, 440]):
                shouts_block[skey]["size"] = list(sdef["size"])
                manifest_updated = True

        chars_block = self.data.setdefault("characters", {})
        for cname, cdef in DEFAULT_MANIFEST["characters"].items():
            if cname not in chars_block:
                chars_block[cname] = copy.deepcopy(cdef)
                manifest_updated = True
            else:
                existing_poses = chars_block[cname].setdefault("poses", {})
                for pname, pfile in cdef.get("poses", {}).items():
                    if pname not in existing_poses:
                        existing_poses[pname] = pfile
                        manifest_updated = True

        if manifest_updated:
            try:
                with open(manifest_path, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=2)
            except Exception as e:
                print(f"[ASSETS] Could not update assets.json: {e}")

        folders = self.data.get("folders", {})
        self.bg_dir = os.path.join(BASE_DIR, folders.get("bg", "assets/bg"))
        self.char_dir = os.path.join(BASE_DIR, folders.get("char", "assets/char"))
        self.icon_dir = os.path.join(BASE_DIR, folders.get("icon", "assets/icon"))
        self.sounds_dir = os.path.join(BASE_DIR, folders.get("sounds", "assets/sounds"))

        for path in (self.bg_dir, self.char_dir, self.icon_dir, self.sounds_dir):
            os.makedirs(path, exist_ok=True)

        self.backgrounds = {}
        self.shouts = {}
        self.characters = {}
        self.sounds = {}
        self._load_all()

    def _find_file_case_insensitive(self, folder, filename):
        exact = os.path.join(folder, filename)
        if os.path.isfile(exact):
            return exact
        target = filename.lower()
        target_stem = os.path.splitext(target)[0]
        if os.path.isdir(folder):
            for entry in os.listdir(folder):
                low = entry.lower()
                if low == target or low == f"{target}.png" or os.path.splitext(low)[0] == target_stem:
                    return os.path.join(folder, entry)
        return None

    def _load_surface(
        self,
        base_dir,
        filename,
        size,
        fallback_color,
        label="",
        optional=False,
        trim_vertical=False,
        preserve_aspect=False
    ):
        found_path = self._find_file_case_insensitive(base_dir, filename)
        if found_path:
            try:
                img = pygame.image.load(found_path).convert_alpha()
                if trim_vertical:
                    bbox = img.get_bounding_rect()
                    if bbox.width > 0 and bbox.height > 0:
                        img = img.subsurface(pygame.Rect(0, bbox.top, img.get_width(), bbox.height)).copy()
                if preserve_aspect:
                    bbox = img.get_bounding_rect()
                    if bbox.width > 0 and bbox.height > 0:
                        img = img.subsurface(bbox).copy()
                    iw, ih = img.get_size()
                    ratio = min(size[0] / max(1, iw), size[1] / max(1, ih))
                    target_size = (max(1, int(iw * ratio)), max(1, int(ih * ratio)))
                    return pygame.transform.smoothscale(img, target_size)
                return pygame.transform.smoothscale(img, tuple(size))
            except Exception as e:
                print(f"[ASSETS] Error loading {found_path}: {e}")

        if optional:
            return None

        surf = pygame.Surface(tuple(size), pygame.SRCALPHA)
        pygame.draw.rect(surf, fallback_color, (0, 0, size[0], size[1]), border_radius=12)
        pygame.draw.rect(surf, WHITE, (0, 0, size[0], size[1]), 3, border_radius=12)
        if label:
            for i, line in enumerate(label.split("\n")):
                txt = font_name.render(line, True, WHITE)
                surf.blit(txt, (size[0] // 2 - txt.get_width() // 2, size[1] // 2 - 12 + i * 22))
        return surf

    def _load_all(self):
        app_icon_file = self.data.get("app_icon", "app_icon.png")
        app_icon = self._load_surface(self.icon_dir, app_icon_file, (64, 64), BLUE_ACCENT, optional=True)
        if app_icon:
            pygame.display.set_icon(app_icon)

        for bg_key, cfg in self.data.get("backgrounds", {}).items():
            if bg_key in ("title_logo", "title_bg"):
                self.backgrounds[bg_key] = self._load_surface(
                    self.bg_dir, cfg["file"], cfg["size"], NAVY, optional=True
                )
            else:
                self.backgrounds[bg_key] = self._load_surface(
                    self.bg_dir, cfg["file"], cfg["size"], (26, 36, 58)
                )

        for shout_key, cfg in self.data.get("shouts", {}).items():
            self.shouts[shout_key] = self._load_surface(
                self.bg_dir, cfg["file"], cfg["size"], GOLD, optional=True, preserve_aspect=True
            )

        palette = {
            "Dave": (35, 95, 195),
            "Tyrone": (40, 130, 110),
            "Elijah": (45, 115, 165),
            "Kendall": (150, 45, 65),
            "Dwyane": (75, 65, 115),
            "CFO": (130, 35, 50),
            "Accountant": (80, 95, 125),
            "Employee": (65, 110, 95)
        }
        for char_name, cfg in self.data.get("characters", {}).items():
            size = cfg.get("size", [430, 410])
            base_color = palette.get(char_name, (70, 90, 120))
            sub_folder = cfg.get("folder", char_name.lower())
            target_dir = os.path.join(self.char_dir, sub_folder)
            if not os.path.isdir(target_dir):
                target_dir = self.char_dir

            self.characters[char_name] = {}
            poses = dict(cfg.get("poses") or {})

            if os.path.isdir(target_dir):
                prefix = f"{sub_folder.lower()}_"
                for fname in os.listdir(target_dir):
                    low = fname.lower()
                    if low.endswith(".png") and low.startswith(prefix):
                        pose_key = os.path.splitext(low)[0][len(prefix):]
                        if pose_key and pose_key not in poses:
                            poses[pose_key] = fname

            if poses:
                for pose_name, filename in poses.items():
                    is_opt = (pose_name != "idle")
                    surf = self._load_surface(
                        target_dir,
                        filename,
                        size,
                        base_color,
                        f"{char_name}\n({pose_name})",
                        optional=is_opt,
                        trim_vertical=True
                    )
                    if surf:
                        self.characters[char_name][pose_name] = surf
            else:
                filename = cfg.get("file", f"{char_name.lower()}.png")
                self.characters[char_name]["idle"] = self._load_surface(
                    target_dir, filename, size, base_color, f"{char_name}", trim_vertical=True
                )

        if pygame.mixer.get_init():
            sound_map = dict(DEFAULT_MANIFEST["sounds"])
            sound_map.update(self.data.get("sounds", {}))
            for snd_key, filename in sound_map.items():
                found_snd = self._find_file_case_insensitive(self.sounds_dir, filename)
                if found_snd:
                    try:
                        snd = pygame.mixer.Sound(found_snd)
                        snd.set_volume(0.45 if snd_key == "speak" else 0.85)
                        self.sounds[snd_key] = snd
                    except Exception as e:
                        print(f"[ASSETS] Error loading sound {found_snd}: {e}")

    def play_sound(self, snd_key, stop_previous=True):
        snd = self.sounds.get(snd_key)
        if snd and pygame.mixer.get_init():
            if stop_previous:
                snd.stop()
            snd.play()

    def play_speak_blip(self):
        self.play_sound("speak", stop_previous=True)

    def get_char_sprite(self, char_name, pose="idle"):
        char_poses = self.characters.get(char_name)
        if not char_poses:
            return None
        if pose in char_poses:
            return char_poses[pose]
        pose_fallbacks = {
            "shocked": ("worried", "think", "idle"),
            "worried": ("shocked", "think", "sigh", "idle"),
            "sigh": ("think", "worried", "idle"),
            "stare": ("angry", "point", "idle"),
            "relief": ("smile", "idle"),
            "laugh": ("smile", "idle"),
            "angry": ("stare", "point", "worried", "idle"),
            "think": ("sigh", "worried", "idle"),
            "point": ("stare", "angry", "idle"),
            "smile": ("relief", "laugh", "idle")
        }
        for alt in pose_fallbacks.get(pose, ("idle",)):
            if alt in char_poses:
                return char_poses[alt]
        return char_poses.get("idle")


def draw_ace_attorney_shout(surface, shout_text, shout_color, shout_img, progress_elapsed, tick):
    """Renders an oversized Ace Attorney shout graphic with heavy screen-shake and slam impact."""
    cx, cy = WIDTH // 2, HEIGHT // 2

    dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dim.fill((0, 0, 0, 120))
    surface.blit(dim, (0, 0))

    # Slam-in scale (1.48x -> 1.0x over first 6 frames) + intense Ace Attorney vibration
    slam_scale = 1.0 + max(0.0, (6 - progress_elapsed) * 0.08)
    shake_decay = max(0.35, 1.0 - (progress_elapsed / 75.0))
    jx = int((math.sin(tick * 3.7) * 14 + math.cos(tick * 5.3) * 6) * shake_decay)
    jy = int((math.cos(tick * 4.1) * 12 + math.sin(tick * 6.1) * 5) * shake_decay)

    if shout_img:
        sw = max(1, int(shout_img.get_width() * slam_scale))
        sh = max(1, int(shout_img.get_height() * slam_scale))
        scaled_img = pygame.transform.smoothscale(shout_img, (sw, sh)) if slam_scale > 1.001 else shout_img
        surface.blit(scaled_img, (cx - sw // 2 + jx, cy - sh // 2 + jy))
        return

    # Full-screen jagged speech bubble fallback when PNG is not present
    num_spikes = 22
    outer_pts = []
    inner_pts = []
    rx_outer, ry_outer = int(410 * slam_scale), int(275 * slam_scale)
    rx_inner, ry_inner = int(390 * slam_scale), int(258 * slam_scale)
    for i in range(num_spikes):
        ang = 2 * math.pi * i / num_spikes
        spike = 1.0 if i % 2 == 0 else 0.74
        ox = cx + jx + int(math.cos(ang) * rx_outer * spike)
        oy = cy + jy + int(math.sin(ang) * ry_outer * spike)
        ix = cx + jx + int(math.cos(ang) * rx_inner * spike)
        iy = cy + jy + int(math.sin(ang) * ry_inner * spike)
        outer_pts.append((ox, oy))
        inner_pts.append((ix, iy))

    pygame.draw.polygon(surface, BLACK, outer_pts)
    pygame.draw.polygon(surface, WHITE, inner_pts)
    pygame.draw.polygon(surface, shout_color, inner_pts, 9)

    base_txt = font_shout.render(shout_text, True, shout_color)
    shadow_txt = font_shout.render(shout_text, True, BLACK)
    tw = max(1, int(base_txt.get_width() * slam_scale))
    th = max(1, int(base_txt.get_height() * slam_scale))
    if slam_scale > 1.001:
        base_txt = pygame.transform.smoothscale(base_txt, (tw, th))
        shadow_txt = pygame.transform.smoothscale(shadow_txt, (tw, th))

    tx = cx - tw // 2 + jx
    ty = cy - th // 2 + jy
    for ox, oy in ((-6, -6), (6, -6), (-6, 6), (6, 6), (8, 9)):
        surface.blit(shadow_txt, (tx + ox, ty + oy))
    surface.blit(base_txt, (tx, ty))


def draw_title_chamber_backdrop(surface):
    """Draws an atmospheric classical courtroom chamber backdrop when title_bg.png is not provided."""
    surface.fill((28, 34, 48))
    pygame.draw.rect(surface, (152, 162, 178), (40, 0, WIDTH - 80, 340))
    pygame.draw.rect(surface, (120, 130, 148), (40, 0, WIDTH - 80, 42))
    pygame.draw.rect(surface, (95, 105, 122), (40, 42, WIDTH - 80, 10))

    for cx in (190, 290, 455, 535, 645):
        pygame.draw.rect(surface, (175, 184, 198), (cx, 52, 26, 280))
        pygame.draw.rect(surface, (132, 140, 155), (cx + 5, 52, 4, 280))
        pygame.draw.rect(surface, (132, 140, 155), (cx + 15, 52, 4, 280))

    pygame.draw.rect(surface, (74, 46, 36), (70, 180, WIDTH - 140, 200))
    pygame.draw.rect(surface, (24, 28, 38), (345, 185, 86, 175))
    pygame.draw.rect(surface, (165, 174, 188), (341, 181, 94, 180), 4)

    pygame.draw.rect(surface, (82, 20, 32), (0, 0, 74, 410))
    pygame.draw.rect(surface, (82, 20, 32), (WIDTH - 74, 0, 74, 410))
    pygame.draw.line(surface, (175, 135, 70), (0, 78), (74, 52), 3)
    pygame.draw.line(surface, (175, 135, 70), (WIDTH - 74, 52), (WIDTH, 78), 3)

    pygame.draw.ellipse(surface, (52, 34, 28), (-60, 325, WIDTH + 120, 240))
    pygame.draw.ellipse(surface, (36, 22, 18), (-20, 365, WIDTH + 40, 210))
    pygame.draw.polygon(surface, (96, 26, 34), [(150, 460), (650, 460), (740, 600), (60, 600)])

    shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shade.fill((8, 12, 22, 75))
    surface.blit(shade, (0, 0))


def draw_centered_title_logo(surface, center_x, top_y, scale=1.0):
    """Draws the centered I-ATTORNEY hexagon + starburst emblem matching the title UI."""
    hx = center_x - int(190 * scale)
    hy = top_y + int(108 * scale)
    r = int(74 * scale)
    hex_pts = []
    for i in range(6):
        ang = math.radians(60 * i - 90)
        hex_pts.append((hx + r * math.cos(ang), hy + r * math.sin(ang)))
    pygame.draw.polygon(surface, (12, 82, 168), hex_pts)

    scaled_i_font = pygame.font.SysFont("georgia,timesnewroman", max(12, int(88 * scale)), bold=True)
    i_surf = scaled_i_font.render("I", True, WHITE)
    surface.blit(i_surf, (hx - i_surf.get_width() // 2, hy - i_surf.get_height() // 2 - int(2 * scale)))

    sx = hx + int(92 * scale)
    sy = hy - int(36 * scale)
    ring_r = int(58 * scale)
    pygame.draw.circle(surface, BLACK, (sx, sy), ring_r, max(2, int(9 * scale)))
    pygame.draw.circle(surface, ORANGE_SPARK, (sx, sy), ring_r, max(1, int(4 * scale)))

    raw_star = [
        (-78, -92), (12, -16), (94, -62), (18, 10),
        (82, 78), (-6, 16), (-76, 64), (-14, -10),
    ]
    star_pts = [(sx + int(dx * scale), sy + int(dy * scale)) for dx, dy in raw_star]
    shadow_off = max(1, int(2 * scale))
    pygame.draw.polygon(surface, BLACK, [(px + shadow_off, py + shadow_off) for px, py in star_pts])
    pygame.draw.polygon(surface, ORANGE_SPARK, star_pts)
    pygame.draw.circle(surface, (255, 245, 165), (sx, sy), int(22 * scale))

    scaled_word_font = pygame.font.SysFont("georgia,timesnewroman", max(12, int(54 * scale)), bold=True)
    word_shadow = scaled_word_font.render("ATTORNEY", True, (15, 18, 26))
    word_surf = scaled_word_font.render("ATTORNEY", True, WHITE)
    word_x = hx + int(58 * scale)
    word_y = hy - int(2 * scale)
    w_off = max(1, int(3 * scale))
    surface.blit(word_shadow, (word_x + w_off, word_y + w_off))
    surface.blit(word_surf, (word_x, word_y))


def get_title_button_rects():
    """Returns the 4 royal-blue 2x2 menu button rects matching the title UI layout."""
    btn_w, btn_h = 276, 56
    left_x = 104
    right_x = 420
    row1_y = 328
    row2_y = 438
    return [
        pygame.Rect(left_x, row1_y, btn_w, btn_h),    # 0: START GAME
        pygame.Rect(right_x, row1_y, btn_w, btn_h),   # 1: LOAD GAME
        pygame.Rect(left_x, row2_y, btn_w, btn_h),    # 2: ACHIEVEMENTS
        pygame.Rect(right_x, row2_y, btn_w, btn_h),   # 3: CHAPTERS
    ]


def get_char_delay(ch):
    if ch in (".", "!", "?"):
        return 14
    if ch in (",", ";", ":"):
        return 8
    if ch in ("—", "-"):
        return 10
    return 2


def unpack_dialogue_item(item):
    speaker = item[0]
    line = item[1]
    pose = item[2] if len(item) >= 3 else "idle"
    sfx = item[3] if len(item) >= 4 else None
    return speaker, line, pose, sfx


def main():
    global screen
    is_fullscreen = False
    windowed_size = (WIDTH, HEIGHT)

    assets = AssetManager()
    progress = load_progress()

    scene = "TITLE"
    title_options = [
        "START GAME",
        "LOAD GAME",
        "ACHIEVEMENTS",
        "CHAPTERS"
    ]
    title_idx = 0

    story_keys = ["Dave", "Tyrone"]
    story_select_idx = 0
    story_select_mode = "PLAY"
    active_story = DAVE_STORY

    chapter_select_idx = 0
    credits_page_idx = 0
    credits_anim_tick = 0
    title_msg = ""
    tick = 0

    truth_score = 0
    shield_score = 0
    final_case_trigger = "FULL_TRUTH"
    resolved_ending_key = "TRUE_ENDING"
    decision_idx = 0

    current_chapter_idx = 0
    dialogue_queue = []
    after_dialogue_action = "NEXT_CHAPTER"
    cur_speaker, cur_line, cur_pose = "", "", "idle"
    prev_speaker = ""
    slide_offset = 0
    char_idx = 0
    text_wait = 0
    line_done_hold = 0
    input_lock_timer = 0
    card_timer = 0
    card_anim_tick = 0
    brief_anim_tick = 0
    gameover_anim_tick = 0
    verdict_anim_tick = 0

    fade_alpha = 0
    fade_dir = 0
    fade_speed = 18
    fade_callback = None
    fade_color = PURE_BLACK

    health = 5
    statements = []
    stmt_idx = 0
    show_record = False
    record_idx = 0
    active_evidence = []
    shout_text = ""
    shout_color = GOLD
    shout_timer = 0
    shout_duration = 72
    shake_timer = 0
    shake_intensity = 10
    flash_timer = 0
    flash_color = WHITE

    def toggle_fullscreen():
        nonlocal is_fullscreen, windowed_size
        global screen
        is_fullscreen = not is_fullscreen
        if is_fullscreen:
            windowed_size = screen.get_size()
            info = pygame.display.Info()
            screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(windowed_size, pygame.RESIZABLE)

    def transition_with_fade(callback, color=PURE_BLACK, speed=20):
        nonlocal fade_alpha, fade_dir, fade_callback, fade_color, fade_speed
        if fade_dir == 1:
            return
        fade_color = color
        fade_speed = speed
        fade_callback = callback
        fade_dir = 1
        fade_alpha = 0

    def persist_checkpoint(ch_idx):
        progress["last_run"] = {
            "attorney": active_story["attorney"],
            "chapter_idx": ch_idx,
            "truth_score": truth_score,
            "shield_score": shield_score
        }
        save_progress(progress)

    def unlock_certificate(chapter_obj):
        entry = f"{active_story['attorney']} — {chapter_obj['title']}: {chapter_obj.get('ethics_topic', '')}"
        if entry not in progress["certificates"]:
            progress["certificates"].append(entry)
            save_progress(progress)

    def unlock_ending_record(ending_key):
        if ending_key not in progress["endings"]:
            progress["endings"].append(ending_key)
            save_progress(progress)

    def compute_ending():
        attorney = active_story["attorney"]
        unlocked = set(progress.get("endings", []))
        both_routes_cleared = ("DAVE_VICTORY" in unlocked and "TYRONE_VICTORY" in unlocked)

        if (
            both_routes_cleared
            and health == 5
            and final_case_trigger == "FULL_TRUTH"
            and shield_score == 0
            and truth_score >= 4
        ):
            return "TRUE_ENDING"

        if attorney == "Dave":
            return "DAVE_VICTORY"
        return "TYRONE_VICTORY"

    def trigger_shout(text, color=GOLD, shake=42, hold=72, snd_key=None, flash=14):
        nonlocal shout_text, shout_color, shout_timer, shout_duration, shake_timer, shake_intensity, input_lock_timer, flash_timer, flash_color
        shout_text = text
        shout_color = color
        shout_timer = hold
        shout_duration = hold
        shake_timer = shake
        shake_intensity = 22
        flash_timer = flash
        flash_color = WHITE
        input_lock_timer = hold
        if snd_key:
            assets.play_sound(snd_key, stop_previous=True)

    def trigger_random_evidence_shout(is_correct):
        """Randomly plays either 'TAKE THAT!' or 'OBJECTION!' only when presenting evidence."""
        choice = random.choice(["take_that", "objection"])
        if choice == "take_that":
            trigger_shout(
                "TAKE THAT!",
                ORANGE_SPARK,
                shake=48 if is_correct else 42,
                hold=74,
                snd_key="take_that",
                flash=14 if is_correct else 12
            )
        else:
            trigger_shout(
                "OBJECTION!",
                BLUE_ACCENT,
                shake=48 if is_correct else 42,
                hold=74,
                snd_key="objection",
                flash=14 if is_correct else 12
            )

    def trigger_impact(shake=14, flash=8, color=WHITE, play_bang=False, intensity=10):
        nonlocal shake_timer, shake_intensity, flash_timer, flash_color
        shake_timer = max(shake_timer, shake)
        shake_intensity = max(shake_intensity, intensity)
        flash_timer = max(flash_timer, flash)
        flash_color = color
        if play_bang:
            assets.play_sound("bang", stop_previous=True)

    def enter_game_over():
        nonlocal scene, gameover_anim_tick, input_lock_timer
        scene = "GAME_OVER"
        gameover_anim_tick = 0
        input_lock_timer = 35
        assets.play_sound("whoops", stop_previous=True)
        trigger_impact(shake=26, flash=14, color=RED, intensity=14)

    def enter_case_verdict():
        nonlocal scene, verdict_anim_tick, input_lock_timer
        scene = "CASE_VERDICT"
        verdict_anim_tick = 0
        input_lock_timer = 22
        assets.play_sound("testimony", stop_previous=True)
        trigger_impact(shake=8, flash=8, color=GOLD, intensity=8)

    def start_credits():
        def _open_credits():
            nonlocal scene, credits_page_idx, credits_anim_tick, input_lock_timer
            scene = "CREDITS"
            credits_page_idx = 0
            credits_anim_tick = 0
            input_lock_timer = 16
        transition_with_fade(_open_credits)

    def return_to_main_menu(msg=""):
        nonlocal scene, current_chapter_idx, dialogue_queue, cur_speaker, cur_line, cur_pose, prev_speaker
        nonlocal char_idx, card_timer, title_idx, title_msg, show_record, health, shout_timer, input_lock_timer
        nonlocal truth_score, shield_score, final_case_trigger, flash_timer, credits_page_idx
        scene = "TITLE"
        current_chapter_idx = 0
        credits_page_idx = 0
        dialogue_queue = []
        cur_speaker, cur_line, cur_pose, prev_speaker = "", "", "idle", ""
        char_idx = 0
        card_timer = 0
        title_idx = 0
        show_record = False
        shout_timer = 0
        flash_timer = 0
        input_lock_timer = 12
        health = 5
        truth_score = 0
        shield_score = 0
        final_case_trigger = "FULL_TRUTH"
        title_msg = msg

    def set_current_line(speaker, line, pose="idle", sfx=None):
        nonlocal cur_speaker, cur_line, cur_pose, prev_speaker, slide_offset, char_idx, text_wait, line_done_hold, input_lock_timer
        if speaker != prev_speaker:
            slide_offset = 45
            prev_speaker = speaker
        cur_speaker = speaker
        cur_line = line
        cur_pose = pose
        char_idx = 0
        text_wait = 8
        line_done_hold = 0
        input_lock_timer = 10

        stripped_line = line.strip()
        low_line = stripped_line.lower()
        if sfx:
            assets.play_sound(sfx, stop_previous=True)
            trigger_impact(shake=14, flash=8, color=RED if sfx == "whoops" else WHITE)
        elif stripped_line.startswith("(") and stripped_line.endswith(")"):
            assets.play_sound("realization", stop_previous=True)
        else:
            if low_line.startswith("objection"):
                trigger_shout("OBJECTION!", BLUE_ACCENT, shake=42, hold=58, snd_key="objection", flash=12)
            elif low_line.startswith("hold it"):
                trigger_shout("HOLD IT!", GOLD, shake=36, hold=54, snd_key="hold_it", flash=10)
            elif pose in ("point", "angry", "shocked", "stare") or any(
                kw in low_line for kw in ("impossible!", "lies!", "no way!", "contradiction", "fabricated", "red-handed", "guilty", "checkmate")
            ):
                trigger_impact(shake=14, flash=7, color=WHITE, play_bang=True)

    def queue_dialogue(lines, next_action):
        nonlocal dialogue_queue, scene, after_dialogue_action
        dialogue_queue = list(lines)
        first_speaker, first_line, first_pose, first_sfx = unpack_dialogue_item(dialogue_queue.pop(0))
        set_current_line(first_speaker, first_line, first_pose, first_sfx)
        after_dialogue_action = next_action
        scene = "DIALOGUE"

    def start_cross_exam():
        nonlocal scene, statements, stmt_idx, show_record, record_idx, active_evidence, input_lock_timer
        chapter = active_story["chapters"][current_chapter_idx]
        ce = chapter["cross_exam"]
        statements = copy.deepcopy(ce["statements"])
        stmt_idx = 0
        active_evidence = list(chapter["evidence"])
        record_idx = 0
        show_record = False
        input_lock_timer = 15
        scene = "CROSS_EXAM"

    def open_chapter_brief():
        def _show_brief():
            nonlocal scene, brief_anim_tick, input_lock_timer
            scene = "CHAPTER_BRIEF"
            brief_anim_tick = 0
            input_lock_timer = 18
        transition_with_fade(_show_brief)

    def start_chapter(idx, play_prologue=False, reset_scores=True):
        nonlocal scene, current_chapter_idx, card_timer, card_anim_tick, health, prev_speaker, input_lock_timer
        nonlocal truth_score, shield_score, resolved_ending_key

        if idx == 0 and reset_scores:
            truth_score = 0
            shield_score = 0

        chapters = active_story["chapters"]
        if idx >= len(chapters):
            resolved_ending_key = compute_ending()
            unlock_ending_record(resolved_ending_key)
            ending_data = ENDINGS_DB[resolved_ending_key]
            transition_with_fade(lambda: queue_dialogue(ending_data["dialogue"], "SHOW_ENDING_CARD"))
            return

        current_chapter_idx = idx
        health = 5
        prev_speaker = ""
        persist_checkpoint(idx)

        if play_prologue and idx == 0 and active_story.get("prologue"):
            transition_with_fade(lambda: queue_dialogue(active_story["prologue"], "START_CH0_CARD"))
            return

        def _open_card():
            nonlocal scene, card_timer, card_anim_tick, input_lock_timer
            card_timer = 155
            card_anim_tick = 0
            input_lock_timer = 25
            scene = "CHAPTER_CARD"
            assets.play_sound("testimony", stop_previous=True)

        transition_with_fade(_open_card)

    def begin_chapter_dialogue():
        chapter = active_story["chapters"][current_chapter_idx]
        transition_with_fade(lambda: queue_dialogue(chapter["intro"], "CROSS_EXAM"))

    def execute_title_option(opt):
        nonlocal story_select_idx, story_select_mode, input_lock_timer, scene
        nonlocal active_story, truth_score, shield_score, title_msg
        if opt == "START GAME":
            def _go_select():
                nonlocal story_select_idx, story_select_mode, input_lock_timer, scene
                story_select_idx = 0
                story_select_mode = "PLAY"
                input_lock_timer = 10
                scene = "STORY_SELECT"
            transition_with_fade(_go_select)
        elif opt == "LOAD GAME":
            saved = progress.get("last_run")
            if not saved or saved.get("attorney") not in STORY_REGISTRY:
                title_msg = "* No saved game found yet!"
            else:
                active_story = STORY_REGISTRY[saved["attorney"]]
                truth_score = saved.get("truth_score", 0)
                shield_score = saved.get("shield_score", 0)
                saved_ch = min(saved.get("chapter_idx", 0), len(active_story["chapters"]) - 1)
                start_chapter(saved_ch, play_prologue=False, reset_scores=False)
        elif opt == "ACHIEVEMENTS":
            def _go_certs():
                nonlocal input_lock_timer, scene
                input_lock_timer = 10
                scene = "CERTIFICATES"
            transition_with_fade(_go_certs)
        elif opt == "CHAPTERS":
            def _go_ch_select():
                nonlocal story_select_idx, story_select_mode, input_lock_timer, scene
                story_select_idx = 0
                story_select_mode = "CHAPTER_SELECT"
                input_lock_timer = 10
                scene = "STORY_SELECT"
            transition_with_fade(_go_ch_select)

    def advance_dialogue():
        nonlocal char_idx, line_done_hold, input_lock_timer, scene, decision_idx
        if input_lock_timer > 0 or shout_timer > 0 or fade_dir != 0:
            return

        if char_idx < len(cur_line):
            char_idx = len(cur_line)
            line_done_hold = 14
            input_lock_timer = 14
        elif line_done_hold <= 0:
            if dialogue_queue:
                next_speaker, next_line, next_pose, next_sfx = unpack_dialogue_item(dialogue_queue.pop(0))
                set_current_line(next_speaker, next_line, next_pose, next_sfx)
            else:
                if after_dialogue_action == "START_CH0_CARD":
                    start_chapter(0, play_prologue=False, reset_scores=False)
                elif after_dialogue_action == "CROSS_EXAM":
                    transition_with_fade(start_cross_exam)
                elif after_dialogue_action == "POST_WIN_CHECK":
                    chapter = active_story["chapters"][current_chapter_idx]
                    unlock_certificate(chapter)
                    if chapter.get("decision"):
                        def _open_dec():
                            nonlocal decision_idx, input_lock_timer, scene
                            decision_idx = 0
                            input_lock_timer = 15
                            scene = "DECISION"
                        transition_with_fade(_open_dec)
                    else:
                        transition_with_fade(enter_case_verdict)
                elif after_dialogue_action == "CASE_VERDICT":
                    transition_with_fade(enter_case_verdict)
                elif after_dialogue_action == "SHOW_ENDING_CARD":
                    def _open_end():
                        nonlocal input_lock_timer, scene
                        input_lock_timer = 25
                        scene = "END"
                    transition_with_fade(_open_end)
                elif after_dialogue_action == "GAME_OVER":
                    transition_with_fade(enter_game_over, color=CRIMSON, speed=16)
                else:
                    start_chapter(current_chapter_idx + 1, reset_scores=False)

    def advance_credits_page(step=1):
        nonlocal credits_page_idx, credits_anim_tick, input_lock_timer
        new_idx = credits_page_idx + step
        if new_idx < 0:
            return
        if new_idx >= len(CREDITS_PAGES):
            transition_with_fade(return_to_main_menu)
        else:
            def _set_page():
                nonlocal credits_page_idx, credits_anim_tick, input_lock_timer
                credits_page_idx = new_idx
                credits_anim_tick = 0
                input_lock_timer = 12
            transition_with_fade(_set_page, speed=26)

    while True:
        try:
            clock.tick(60)
            tick += 1
            canvas = pygame.Surface((WIDTH, HEIGHT))
            win_w, win_h = screen.get_size()

            if shout_timer > 0:
                shout_timer -= 1
            if shake_timer > 0:
                shake_timer -= 1
            else:
                shake_intensity = 10
            if flash_timer > 0:
                flash_timer -= 1
            if input_lock_timer > 0:
                input_lock_timer -= 1
            if line_done_hold > 0:
                line_done_hold -= 1
            if slide_offset > 0:
                slide_offset = max(0, slide_offset - 5)

            if fade_dir == 1:
                fade_alpha += fade_speed
                if fade_alpha >= 255:
                    fade_alpha = 255
                    if fade_callback:
                        cb = fade_callback
                        fade_callback = None
                        cb()
                    fade_dir = -1
            elif fade_dir == -1:
                fade_alpha -= fade_speed
                if fade_alpha <= 0:
                    fade_alpha = 0
                    fade_dir = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE and not is_fullscreen:
                    screen = pygame.display.set_mode((max(400, event.w), max(300, event.h)), pygame.RESIZABLE)
                    win_w, win_h = screen.get_size()

                if event.type == pygame.MOUSEMOTION and scene == "TITLE":
                    mx, my = screen_to_virtual(event.pos, win_w, win_h)
                    for i, rect in enumerate(get_title_button_rects()):
                        if rect.collidepoint(mx, my):
                            title_idx = i

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11 or (
                        event.key == pygame.K_RETURN and (event.mod & pygame.KMOD_ALT)
                    ):
                        toggle_fullscreen()
                        win_w, win_h = screen.get_size()
                        continue

                    if scene != "TITLE" and event.key == pygame.K_ESCAPE:
                        if scene == "CROSS_EXAM" and show_record:
                            show_record = False
                        elif scene == "CHAPTER_SELECT":
                            transition_with_fade(lambda: None)
                            scene = "STORY_SELECT"
                        else:
                            transition_with_fade(return_to_main_menu)
                        continue

                    if input_lock_timer > 0 or shout_timer > 0 or fade_dir != 0:
                        continue

                    if scene == "TITLE":
                        if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                            title_idx ^= 1
                            title_msg = ""
                        elif event.key in (pygame.K_UP, pygame.K_DOWN):
                            title_idx ^= 2
                            title_msg = ""
                        elif event.key == pygame.K_F5:
                            assets = AssetManager()
                            title_msg = "* Reloaded assets.json!"
                        elif event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                            execute_title_option(title_options[title_idx])

                    elif scene == "STORY_SELECT":
                        if event.key in (pygame.K_UP, pygame.K_LEFT):
                            story_select_idx = (story_select_idx - 1) % len(story_keys)
                        elif event.key in (pygame.K_DOWN, pygame.K_RIGHT):
                            story_select_idx = (story_select_idx + 1) % len(story_keys)
                        elif event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                            chosen_key = story_keys[story_select_idx]
                            active_story = STORY_REGISTRY[chosen_key]
                            if story_select_mode == "PLAY":
                                start_chapter(0, play_prologue=True, reset_scores=True)
                            else:
                                def _open_ch_list():
                                    nonlocal chapter_select_idx, input_lock_timer, scene
                                    chapter_select_idx = 0
                                    input_lock_timer = 10
                                    scene = "CHAPTER_SELECT"
                                transition_with_fade(_open_ch_list)

                    elif scene == "CHAPTER_SELECT":
                        chapters = active_story["chapters"]
                        if event.key == pygame.K_UP:
                            chapter_select_idx = (chapter_select_idx - 1) % len(chapters)
                        elif event.key == pygame.K_DOWN:
                            chapter_select_idx = (chapter_select_idx + 1) % len(chapters)
                        elif event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                            start_chapter(
                                chapter_select_idx,
                                play_prologue=(chapter_select_idx == 0),
                                reset_scores=True
                            )

                    elif scene == "CERTIFICATES":
                        if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                            transition_with_fade(return_to_main_menu)

                    elif scene == "CHAPTER_CARD":
                        if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                            open_chapter_brief()

                    elif scene == "CHAPTER_BRIEF":
                        if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                            begin_chapter_dialogue()

                    elif scene == "DIALOGUE":
                        if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                            advance_dialogue()

                    elif scene == "DECISION":
                        chapter = active_story["chapters"][current_chapter_idx]
                        opts = chapter["decision"]["options"]
                        if event.key == pygame.K_UP:
                            decision_idx = (decision_idx - 1) % len(opts)
                        elif event.key == pygame.K_DOWN:
                            decision_idx = (decision_idx + 1) % len(opts)
                        elif event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                            chosen_opt = opts[decision_idx]
                            truth_score += chosen_opt.get("truth_delta", 0)
                            shield_score += chosen_opt.get("shield_delta", 0)
                            queue_dialogue(chosen_opt["response"], "CASE_VERDICT")

                    elif scene == "CASE_VERDICT":
                        if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                            start_chapter(current_chapter_idx + 1, reset_scores=False)

                    elif scene == "CROSS_EXAM":
                        if event.key == pygame.K_TAB:
                            show_record = not show_record
                            input_lock_timer = 8
                            continue

                        evidence_db = active_story["evidence_db"]
                        attorney_name = active_story["attorney"]
                        witness_name = active_story["chapters"][current_chapter_idx]["cross_exam"]["witness"]

                        if show_record:
                            if event.key in (pygame.K_UP, pygame.K_LEFT):
                                record_idx = (record_idx - 1) % len(active_evidence)
                            elif event.key in (pygame.K_DOWN, pygame.K_RIGHT):
                                record_idx = (record_idx + 1) % len(active_evidence)
                            elif event.key in (pygame.K_o, pygame.K_RETURN, pygame.K_z):
                                chosen_ev = active_evidence[record_idx]
                                cur_stmt = statements[stmt_idx]
                                show_record = False

                                is_correct = (cur_stmt.get("contradiction") == chosen_ev)
                                trigger_random_evidence_shout(is_correct)

                                if is_correct:
                                    if cur_stmt.get("ending_trigger"):
                                        final_case_trigger = cur_stmt["ending_trigger"]
                                    queue_dialogue(cur_stmt["win_dialogue"], "POST_WIN_CHECK")
                                else:
                                    health -= 1
                                    fail_lines = build_wrong_evidence_dialogue(
                                        attorney_name,
                                        witness_name,
                                        evidence_db[chosen_ev]["name"],
                                        health
                                    )
                                    queue_dialogue(fail_lines, "GAME_OVER" if health <= 0 else "CROSS_EXAM")
                        else:
                            if event.key in (pygame.K_RIGHT, pygame.K_n):
                                stmt_idx = (stmt_idx + 1) % len(statements)
                                input_lock_timer = 8
                            elif event.key in (pygame.K_LEFT, pygame.K_p):
                                stmt_idx = (stmt_idx - 1) % len(statements)
                                input_lock_timer = 8
                            elif event.key == pygame.K_h:
                                cur_stmt = statements[stmt_idx]
                                trigger_shout("HOLD IT!", GOLD, shake=40, hold=68, snd_key="hold_it", flash=12)
                                press_lines = list(cur_stmt["press"])
                                if not cur_stmt.get("pressed_bonus"):
                                    cur_stmt["pressed_bonus"] = True
                                    truth_score += 1
                                if cur_stmt.get("unlocks"):
                                    new_stmt = cur_stmt.pop("unlocks")
                                    cur_stmt["unlocked_already"] = True
                                    if not any(s["text"] == new_stmt["text"] for s in statements):
                                        statements.insert(stmt_idx + 1, new_stmt)
                                    stmt_idx = next(
                                        (i for i, s in enumerate(statements) if s["text"] == new_stmt["text"]),
                                        stmt_idx
                                    )
                                    press_lines.append(("Dwyane", "Witness, enter that clarification into your official testimony!", "stare"))
                                elif cur_stmt.get("unlocked_already") and stmt_idx + 1 < len(statements):
                                    stmt_idx += 1
                                queue_dialogue(press_lines, "CROSS_EXAM")
                            elif event.key == pygame.K_o:
                                show_record = True
                                input_lock_timer = 8

                    elif scene == "END":
                        if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                            start_credits()

                    elif scene == "CREDITS":
                        if event.key in (pygame.K_LEFT, pygame.K_UP):
                            advance_credits_page(-1)
                        elif event.key in (pygame.K_RIGHT, pygame.K_DOWN, pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                            advance_credits_page(1)

                    elif scene == "GAME_OVER":
                        if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE, pygame.K_r):
                            if event.key == pygame.K_r:
                                start_chapter(current_chapter_idx, reset_scores=False)
                            else:
                                transition_with_fade(return_to_main_menu)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if input_lock_timer > 0 or shout_timer > 0 or fade_dir != 0:
                        continue
                    mx, my = screen_to_virtual(event.pos, win_w, win_h)
                    if scene == "TITLE":
                        for i, rect in enumerate(get_title_button_rects()):
                            if rect.collidepoint(mx, my):
                                title_idx = i
                                execute_title_option(title_options[i])
                                break
                    elif scene == "CERTIFICATES":
                        transition_with_fade(return_to_main_menu)
                    elif scene == "CHAPTER_CARD":
                        open_chapter_brief()
                    elif scene == "CHAPTER_BRIEF":
                        begin_chapter_dialogue()
                    elif scene == "DIALOGUE":
                        advance_dialogue()
                    elif scene == "CASE_VERDICT":
                        start_chapter(current_chapter_idx + 1, reset_scores=False)
                    elif scene == "END":
                        start_credits()
                    elif scene == "CREDITS":
                        advance_credits_page(1)
                    elif scene == "GAME_OVER":
                        transition_with_fade(return_to_main_menu)

            # --- UPDATES ---
            if scene == "CHAPTER_CARD":
                card_anim_tick += 1
                card_timer -= 1
                if card_timer <= 0 and fade_dir == 0:
                    open_chapter_brief()
            elif scene == "CHAPTER_BRIEF":
                brief_anim_tick += 1
            elif scene == "CREDITS":
                credits_anim_tick += 1
            elif scene == "GAME_OVER":
                gameover_anim_tick += 1
            elif scene == "CASE_VERDICT":
                verdict_anim_tick += 1
            elif scene == "DIALOGUE":
                if shout_timer <= 0 and char_idx < len(cur_line):
                    if text_wait > 0:
                        text_wait -= 1
                    else:
                        typed_char = cur_line[char_idx]
                        char_idx += 1
                        text_wait = get_char_delay(typed_char)

                        is_internal_thought = cur_line.strip().startswith("(")
                        if not is_internal_thought and typed_char.isalnum() and (char_idx % 2 == 1):
                            assets.play_speak_blip()

                        if char_idx >= len(cur_line):
                            line_done_hold = 12

            # --- RENDERING ON VIRTUAL 800x600 CANVAS ---
            if scene == "TITLE":
                title_bg = assets.backgrounds.get("title_bg")
                if title_bg:
                    canvas.blit(title_bg, (0, 0))
                else:
                    draw_title_chamber_backdrop(canvas)

                logo_img = assets.backgrounds.get("title_logo")
                if logo_img:
                    canvas.blit(logo_img, (WIDTH // 2 - logo_img.get_width() // 2, 34))
                else:
                    draw_centered_title_logo(canvas, WIDTH // 2, 38)

                btn_rects = get_title_button_rects()
                for i, (opt, rect) in enumerate(zip(title_options, btn_rects)):
                    is_sel = (i == title_idx)
                    btn_col = TITLE_BTN_HOVER if is_sel else TITLE_BTN_BLUE
                    pygame.draw.rect(canvas, btn_col, rect)
                    if is_sel:
                        pygame.draw.rect(canvas, GOLD, rect, 3)
                    lbl_surf = font_menu.render(opt, True, WHITE)
                    canvas.blit(
                        lbl_surf,
                        (rect.centerx - lbl_surf.get_width() // 2, rect.centery - lbl_surf.get_height() // 2)
                    )

                fs_state = "FULLSCREEN" if is_fullscreen else "WINDOWED"
                fs_hint = font_small.render(f"[F11] Fullscreen ({fs_state})", True, WHITE)
                canvas.blit(fs_hint, (WIDTH - fs_hint.get_width() - 20, 574))

                if title_msg:
                    msg_surf = render_fitted_line(title_msg, font_small, GOLD, WIDTH - fs_hint.get_width() - 60)
                    canvas.blit(msg_surf, (24, 574))

            elif scene == "CERTIFICATES":
                canvas.fill(PURE_BLACK)
                hdr = font_sub.render("ACHIEVEMENTS, ENDINGS & ETHICS CERTIFICATES", True, GOLD)
                canvas.blit(hdr, (40, 30))
                pygame.draw.line(canvas, GRAY, (40, 66), (760, 66), 1)

                end_hdr = font_name.render(f"UNLOCKED ENDINGS ({len(progress['endings'])}/3):", True, CYAN)
                canvas.blit(end_hdr, (40, 82))
                for idx_e, (ekey, edata) in enumerate(ENDINGS_DB.items()):
                    unlocked = ekey in progress["endings"]
                    if edata.get("secret") and not unlocked:
                        label_txt = "• ??? : [SECRET ENDING — LOCKED]"
                        col = GRAY
                    else:
                        status = edata["title"] if unlocked else "LOCKED"
                        label_txt = f"• {edata['banner']}: {status}"
                        col = edata["color"] if unlocked else GRAY
                    e_surf = render_fitted_line(label_txt, font_small, col, 708)
                    canvas.blit(e_surf, (52, 110 + idx_e * 25))

                cert_hdr = font_name.render(f"EARNED ETHICS CERTIFICATES ({len(progress['certificates'])}/10):", True, GREEN)
                canvas.blit(cert_hdr, (40, 200))

                if not progress["certificates"]:
                    none_surf = render_fitted_line(
                        "Complete cases in Dave's or Tyrone's campaign to earn achievements.",
                        font_small, GRAY, 708
                    )
                    canvas.blit(none_surf, (52, 232))
                else:
                    for idx_c, cert_txt in enumerate(progress["certificates"][:10]):
                        c_surf = render_fitted_line(f"✓ {cert_txt}", font_small, WHITE, 708, min_size=11)
                        canvas.blit(c_surf, (52, 230 + idx_c * 30))

                back_surf = font_small.render("[ENTER / ESC / CLICK] Return to Main Menu", True, GOLD)
                canvas.blit(back_surf, (40, 554))

            elif scene == "STORY_SELECT":
                canvas.fill(BLACK)
                heading_txt = (
                    "CHOOSE YOUR ATTORNEY TO START"
                    if story_select_mode == "PLAY"
                    else "CHOOSE CAMPAIGN FOR CHAPTER SELECT"
                )
                header = font_sub.render(heading_txt, True, GOLD)
                canvas.blit(header, (WIDTH // 2 - header.get_width() // 2, 40))

                for i, key in enumerate(story_keys):
                    st = STORY_REGISTRY[key]
                    card_x = 85 + i * 340
                    card_rect = pygame.Rect(card_x, 95, 290, 395)
                    is_sel = (i == story_select_idx)
                    pygame.draw.rect(canvas, NAVY if is_sel else DARK_NAVY, card_rect, border_radius=12)
                    pygame.draw.rect(canvas, GOLD if is_sel else GRAY, card_rect, 4 if is_sel else 2, border_radius=12)

                    preview_pose = "point" if is_sel else "idle"
                    spr = assets.get_char_sprite(key, preview_pose)
                    if spr:
                        scaled_spr = pygame.transform.smoothscale(spr, (215, 250))
                        canvas.blit(scaled_spr, (card_x + 37, 102))

                    client_name = st.get("client", "Elijah" if key == "Dave" else "Kendall")
                    rival_name = st.get("rival", "Tyrone" if key == "Dave" else "Dave")

                    lbl = render_fitted_line(("> " if is_sel else "  ") + key.upper(), font_main, GOLD if is_sel else WHITE, 266)
                    story_lbl = render_fitted_line(st["subtitle"], font_small, CYAN if is_sel else GRAY, 266)
                    client_lbl = render_fitted_line(
                        f"Client: {client_name} | Rival: {rival_name}",
                        font_small, WHITE if is_sel else GRAY, 266
                    )
                    canvas.blit(lbl, (card_x + 145 - lbl.get_width() // 2, 365))
                    canvas.blit(story_lbl, (card_x + 145 - story_lbl.get_width() // 2, 398))
                    canvas.blit(client_lbl, (card_x + 145 - client_lbl.get_width() // 2, 432))

                action_label = "Start Campaign" if story_select_mode == "PLAY" else "View Chapters"
                hint = font_name.render(f"[LEFT/RIGHT] Select  |  [ENTER] {action_label}  |  [ESC] Back", True, GRAY)
                canvas.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 528))

            elif scene == "CHAPTER_SELECT":
                canvas.fill(BLACK)
                header = render_fitted_line(active_story["title"], font_sub, GOLD, 720)
                canvas.blit(header, (WIDTH // 2 - header.get_width() // 2, 75))

                chapters = active_story["chapters"]
                for i, ch in enumerate(chapters):
                    theme_c = get_case_theme(i)["accent"]
                    color = theme_c if i == chapter_select_idx else WHITE
                    prefix = "> " if i == chapter_select_idx else "  "
                    lbl = render_fitted_line(prefix + ch["title"], font_main, color, 700)
                    canvas.blit(lbl, (WIDTH // 2 - lbl.get_width() // 2, 165 + i * 52))

                hint = font_name.render("[UP/DOWN] Select  |  [ENTER] Play  |  [ESC] Back", True, GRAY)
                canvas.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 510))

            elif scene == "CHAPTER_CARD":
                theme = get_case_theme(current_chapter_idx)
                accent = theme["accent"]
                card_bg = theme["card_bg"]
                chapter = active_story["chapters"][current_chapter_idx]

                canvas.fill(PURE_BLACK)
                t_norm = min(1.0, card_anim_tick / 28.0)
                ease = 1.0 - (1.0 - t_norm) ** 3

                for bar_i in range(6):
                    bar_y = 75 + bar_i * 88
                    bar_w = int((260 + bar_i * 75) * ease)
                    pygame.draw.rect(canvas, (accent[0] // 7, accent[1] // 7, accent[2] // 7), (0, bar_y, bar_w, 2))
                    pygame.draw.rect(canvas, (accent[0] // 7, accent[1] // 7, accent[2] // 7), (WIDTH - bar_w, bar_y + 44, bar_w, 2))

                card_w = int(680 * ease)
                card_h = 265
                card_x = WIDTH // 2 - card_w // 2
                card_y = 165
                if card_w > 12:
                    card = pygame.Rect(card_x, card_y, card_w, card_h)
                    pygame.draw.rect(canvas, card_bg, card, border_radius=14)
                    pygame.draw.rect(canvas, accent, card, 3, border_radius=14)

                if card_anim_tick >= 12:
                    slide_t = min(1.0, (card_anim_tick - 12) / 22.0)
                    slide_ease = 1.0 - (1.0 - slide_t) ** 3
                    left_shift = int((1.0 - slide_ease) * -140)
                    right_shift = int((1.0 - slide_ease) * 140)

                    route_tag = render_fitted_line(active_story["title"], font_small, GRAY, 630)
                    phase_tag = render_fitted_line(theme["tag"], font_small, accent, 630)
                    parts = chapter["title"].split(": ")
                    ch_num = render_fitted_line(parts[0], font_sub, WHITE, 630)
                    sub_txt = parts[1] if len(parts) > 1 else ""
                    ch_sub_font = font_title if font_title.size(sub_txt)[0] <= 630 else pygame.font.SysFont("arial", 32, bold=True)
                    ch_sub = ch_sub_font.render(sub_txt, True, accent)

                    canvas.blit(route_tag, (WIDTH // 2 - route_tag.get_width() // 2, 186))
                    canvas.blit(phase_tag, (WIDTH // 2 - phase_tag.get_width() // 2, 212))

                    line_half = int(260 * slide_ease)
                    pygame.draw.line(canvas, accent, (WIDTH // 2 - line_half, 242), (WIDTH // 2 + line_half, 242), 2)

                    canvas.blit(ch_num, (WIDTH // 2 - ch_num.get_width() // 2 + left_shift, 260))
                    canvas.blit(ch_sub, (WIDTH // 2 - ch_sub.get_width() // 2 + right_shift, 304))

                    eth_lbl = render_fitted_line(f"FOCUS: {chapter.get('ethics_topic', '')}", font_small, GOLD, 630)
                    canvas.blit(eth_lbl, (WIDTH // 2 - eth_lbl.get_width() // 2, 376))

                if card_anim_tick >= 36:
                    prompt = font_small.render("[ENTER / CLICK] Case Briefing >>", True, WHITE)
                    canvas.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 456))

            elif scene == "CHAPTER_BRIEF":
                theme = get_case_theme(current_chapter_idx)
                accent = theme["accent"]
                chapter = active_story["chapters"][current_chapter_idx]
                canvas.fill(PURE_BLACK)

                box_w, box_h = 680, 270
                center_box = pygame.Rect(WIDTH // 2 - box_w // 2, HEIGHT // 2 - box_h // 2, box_w, box_h)
                pygame.draw.rect(canvas, PURE_BLACK, center_box, border_radius=12)
                pygame.draw.rect(canvas, accent, center_box, 3, border_radius=12)

                hdr_lbl = render_fitted_line(f"CASE BRIEFING — {chapter['title']}", font_name, GOLD, box_w - 48)
                canvas.blit(hdr_lbl, (WIDTH // 2 - hdr_lbl.get_width() // 2, center_box.y + 22))
                pygame.draw.line(
                    canvas,
                    GRAY,
                    (center_box.x + 28, center_box.y + 52),
                    (center_box.right - 28, center_box.y + 52),
                    1
                )

                brief_txt = chapter.get(
                    "brief_summary",
                    "Both legal teams gather in court as new corporate records come under scrutiny."
                )
                draw_text_wrapped(
                    canvas,
                    brief_txt,
                    center_box.x + 32,
                    center_box.y + 68,
                    box_w - 64,
                    font_main,
                    WHITE,
                    max_height=142,
                    min_font_size=13,
                    line_spacing=6,
                    center_x=WIDTH // 2
                )

                blink = " >>" if (tick // 20) % 2 == 0 else "   "
                cont_lbl = font_small.render(f"[ENTER / CLICK] Begin Court Session{blink}", True, CYAN)
                canvas.blit(cont_lbl, (WIDTH // 2 - cont_lbl.get_width() // 2, center_box.bottom - 34))

            elif scene == "DECISION":
                theme = get_case_theme(current_chapter_idx)
                accent = theme["accent"]
                canvas.fill(BLACK)
                chapter = active_story["chapters"][current_chapter_idx]
                dec = chapter["decision"]

                card = pygame.Rect(55, 92, 690, 416)
                pygame.draw.rect(canvas, DARK_NAVY, card, border_radius=12)
                pygame.draw.rect(canvas, accent, card, 3, border_radius=12)

                tag = font_sub.render("ETHICAL CROSSROADS — MAKE YOUR DECISION", True, GOLD)
                canvas.blit(tag, (WIDTH // 2 - tag.get_width() // 2, 114))

                draw_text_wrapped(
                    canvas,
                    dec["prompt"],
                    85,
                    158,
                    630,
                    font_main,
                    CYAN,
                    max_height=105,
                    min_font_size=13
                )

                for i, opt in enumerate(dec["options"]):
                    is_sel = (i == decision_idx)
                    opt_rect = pygame.Rect(85, 276 + i * 82, 630, 68)
                    pygame.draw.rect(canvas, NAVY if is_sel else BLACK, opt_rect, border_radius=8)
                    pygame.draw.rect(canvas, GOLD if is_sel else GRAY, opt_rect, 2, border_radius=8)
                    draw_text_wrapped(
                        canvas,
                        ("> " if is_sel else "  ") + opt["label"],
                        opt_rect.x + 14,
                        opt_rect.y + 10,
                        opt_rect.width - 28,
                        font_small,
                        GOLD if is_sel else WHITE,
                        max_height=opt_rect.height - 16,
                        min_font_size=11,
                        line_spacing=3
                    )

                hint = font_small.render("[UP/DOWN] Choose Stance   |   [ENTER] Confirm Decision", True, GREEN)
                canvas.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 466))

            elif scene == "CASE_VERDICT":
                theme = get_case_theme(current_chapter_idx)
                accent = theme["accent"]
                canvas.fill(BLACK)
                chapter = active_story["chapters"][current_chapter_idx]

                v_ease = min(1.0, verdict_anim_tick / 18.0)
                card_y = int(68 + (1.0 - v_ease) * 30)
                card = pygame.Rect(55, card_y, 690, 464)
                pygame.draw.rect(canvas, theme["card_bg"], card, border_radius=14)
                pygame.draw.rect(canvas, GREEN, card, 3, border_radius=14)

                v_title = render_fitted_line(f"{chapter['title']} — COURT ADJOURNED", font_sub, GREEN, 640)
                canvas.blit(v_title, (WIDTH // 2 - v_title.get_width() // 2, card_y + 22))

                eth_hdr = render_fitted_line(
                    f"PRINCIPLE ESTABLISHED: {chapter.get('ethics_topic', 'Corporate Integrity')}",
                    font_name, GOLD, 640
                )
                canvas.blit(eth_hdr, (WIDTH // 2 - eth_hdr.get_width() // 2, card_y + 62))
                pygame.draw.line(canvas, GRAY, (90, card_y + 92), (710, card_y + 92), 1)

                ack_text = chapter.get(
                    "acknowledgement",
                    "Today's session established a decisive breakthrough in the EK Global proceedings, "
                    "demonstrating that clear documentation and ethical accountability prevail in court."
                )
                draw_text_wrapped(
                    canvas,
                    ack_text,
                    85,
                    card_y + 108,
                    630,
                    font_main,
                    WHITE,
                    max_height=248,
                    min_font_size=13,
                    line_spacing=5
                )

                pygame.draw.line(canvas, GRAY, (90, card_y + 370), (710, card_y + 370), 1)
                alignment_txt = f"Truth Pursuit: {truth_score}   |   Client Shielding: {shield_score}"
                align_surf = font_small.render(alignment_txt, True, CYAN)
                canvas.blit(align_surf, (WIDTH // 2 - align_surf.get_width() // 2, card_y + 384))

                cont = font_small.render("[ENTER / CLICK] Advance to Next Case >>", True, GOLD)
                canvas.blit(cont, (WIDTH // 2 - cont.get_width() // 2, card_y + 422))

            elif scene in ("DIALOGUE", "CROSS_EXAM"):
                theme = get_case_theme(current_chapter_idx)
                accent = theme["accent"]
                chapter = active_story["chapters"][current_chapter_idx]
                attorney_name = active_story["attorney"]
                evidence_db = active_story["evidence_db"]

                bg_img = assets.backgrounds.get(chapter["bg"])
                if bg_img:
                    canvas.blit(bg_img, (0, 0))
                else:
                    canvas.fill((26, 36, 58))

                tint_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                tint_surf.fill(theme["tint"])
                canvas.blit(tint_surf, (0, 0))

                if scene == "DIALOGUE":
                    stage_speaker = cur_speaker
                    stage_pose = cur_pose
                    is_talking = (shout_timer <= 0 and char_idx < len(cur_line) and text_wait <= 2)
                else:
                    stage_speaker = chapter["cross_exam"]["witness"]
                    stage_pose = statements[stmt_idx].get(
                        "witness_pose",
                        chapter["cross_exam"].get("default_pose", "idle")
                    )
                    is_talking = False

                char_bob_y = int(abs(math.sin(tick * 0.28)) * 5) if is_talking else 0
                portrait = assets.get_char_sprite(stage_speaker, stage_pose)
                if portrait:
                    char_x = WIDTH // 2 - portrait.get_width() // 2 + slide_offset
                    textbox_top = 388 if scene == "DIALOGUE" else 378
                    anchor_bottom_y = textbox_top + 78
                    char_y = anchor_bottom_y - portrait.get_height() + char_bob_y
                    canvas.blit(portrait, (char_x, char_y))

                pygame.draw.rect(canvas, NAVY, (0, 0, WIDTH, 56))
                pygame.draw.line(canvas, accent, (0, 56), (WIDTH, 56), 3)

                hp_str = "CREDIBILITY: " + ("[!]" * health) + (" . " * (5 - health))
                hp_color = GREEN if health >= 3 else RED
                hp_surf = font_name.render(hp_str, True, hp_color)
                canvas.blit(hp_surf, (WIDTH - hp_surf.get_width() - 18, 18))

                max_hud_w = WIDTH - hp_surf.get_width() - 48
                hud_left = render_fitted_line(f"{chapter['title']} | {attorney_name}", font_name, accent, max_hud_w)
                canvas.blit(hud_left, (18, 18))

                if scene == "DIALOGUE":
                    box = pygame.Rect(36, 388, 728, 186)
                    pygame.draw.rect(canvas, NAVY, box, border_radius=10)
                    pygame.draw.rect(canvas, accent, box, 3, border_radius=10)

                    tag_color = CYAN if cur_speaker == attorney_name else GOLD
                    canvas.blit(font_name.render(cur_speaker.upper(), True, tag_color), (box.x + 20, box.y + 12))

                    text_top = box.y + 40
                    text_bottom_limit = box.bottom - 30
                    draw_text_wrapped(
                        canvas,
                        cur_line[:char_idx],
                        box.x + 20,
                        text_top,
                        box.width - 40,
                        font_main,
                        WHITE,
                        max_height=text_bottom_limit - text_top,
                        min_font_size=12,
                        full_reference_text=cur_line
                    )

                    if char_idx >= len(cur_line) and line_done_hold <= 0 and shout_timer <= 0:
                        blink = " >>" if (tick // 20) % 2 == 0 else "   "
                        hint = font_small.render(f"[ENTER / CLICK] Continue{blink}", True, GOLD)
                        canvas.blit(hint, (box.right - hint.get_width() - 18, box.bottom - 24))

                elif scene == "CROSS_EXAM":
                    ce_badge = pygame.Rect(36, 68, 330, 32)
                    pygame.draw.rect(canvas, RED, ce_badge, border_radius=6)
                    ce_lbl = font_small.render(f"CROSS-EXAMINATION ({stmt_idx + 1}/{len(statements)})", True, WHITE)
                    canvas.blit(ce_lbl, (ce_badge.x + 12, ce_badge.y + 7))

                    box = pygame.Rect(36, 378, 728, 196)
                    pygame.draw.rect(canvas, NAVY, box, border_radius=10)
                    pygame.draw.rect(canvas, GOLD, box, 3, border_radius=10)

                    canvas.blit(font_name.render(f"{stage_speaker.upper()} - TESTIMONY", True, GOLD), (box.x + 20, box.y + 12))
                    stmt_text = f'"{statements[stmt_idx]["text"]}"'
                    stmt_top = box.y + 40
                    stmt_bottom_limit = box.bottom - 44
                    draw_text_wrapped(
                        canvas,
                        stmt_text,
                        box.x + 20,
                        stmt_top,
                        box.width - 40,
                        font_main,
                        CYAN,
                        max_height=stmt_bottom_limit - stmt_top,
                        min_font_size=12
                    )

                    pygame.draw.line(canvas, GRAY, (box.x + 16, box.bottom - 38), (box.right - 16, box.bottom - 38), 1)
                    controls = "[<-/->] Statement   [H] Hold It! (Press)   [O / TAB] Court Record & Object"
                    ctrl_surf = render_fitted_line(controls, font_small, WHITE, box.width - 36)
                    canvas.blit(ctrl_surf, (box.x + 18, box.bottom - 28))

                    if show_record:
                        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                        overlay.fill((8, 12, 24, 215))
                        canvas.blit(overlay, (0, 0))

                        modal = pygame.Rect(70, 55, 660, 490)
                        pygame.draw.rect(canvas, DARK_NAVY, modal, border_radius=12)
                        pygame.draw.rect(canvas, accent, modal, 3, border_radius=12)

                        rec_title = font_sub.render("COURT RECORD - SELECT EVIDENCE TO PRESENT", True, GOLD)
                        canvas.blit(rec_title, (WIDTH // 2 - rec_title.get_width() // 2, 72))

                        for i, ev_key in enumerate(active_evidence):
                            ev = evidence_db[ev_key]
                            is_sel = (i == record_idx)
                            row = pygame.Rect(100, 115 + i * 40, 600, 34)
                            if is_sel:
                                pygame.draw.rect(canvas, NAVY, row, border_radius=6)
                                pygame.draw.rect(canvas, GOLD, row, 2, border_radius=6)
                            lbl = render_fitted_line(
                                ("> " if is_sel else "  ") + ev["name"],
                                font_main,
                                GOLD if is_sel else WHITE,
                                row.width - 28
                            )
                            canvas.blit(lbl, (row.x + 14, row.y + 6))

                        desc_box = pygame.Rect(100, 368, 600, 118)
                        pygame.draw.rect(canvas, NAVY, desc_box, border_radius=8)
                        pygame.draw.rect(canvas, CYAN, desc_box, 2, border_radius=8)
                        cur_ev = evidence_db[active_evidence[record_idx]]
                        draw_text_wrapped(
                            canvas,
                            cur_ev["desc"],
                            desc_box.x + 14,
                            desc_box.y + 10,
                            desc_box.width - 28,
                            font_name,
                            WHITE,
                            max_height=desc_box.height - 20,
                            min_font_size=12
                        )

                        m_hint = font_small.render("[UP/DOWN] Browse   [O / ENTER] PRESENT EVIDENCE   [TAB / ESC] Close", True, GREEN)
                        canvas.blit(m_hint, (WIDTH // 2 - m_hint.get_width() // 2, 504))

            elif scene == "GAME_OVER":
                attorney_name = active_story["attorney"]
                chapter = active_story["chapters"][current_chapter_idx]
                canvas.fill((14, 4, 8))

                pulse = int(18 + 12 * math.sin(gameover_anim_tick * 0.08))
                pygame.draw.rect(canvas, (pulse + 20, 4, 10), (0, 0, WIDTH, HEIGHT))

                bar_drop = min(1.0, gameover_anim_tick / 26.0)
                bar_h = int(HEIGHT * bar_drop)
                for bx in range(45, WIDTH, 90):
                    pygame.draw.rect(canvas, (38, 12, 18), (bx, 0, 12, bar_h))

                slam_scale = max(1.0, 1.35 - min(0.35, gameover_anim_tick * 0.025))
                card_w = int(620 * slam_scale)
                card_h = int(260 * slam_scale)
                card = pygame.Rect(WIDTH // 2 - card_w // 2, HEIGHT // 2 - card_h // 2, card_w, card_h)
                pygame.draw.rect(canvas, (22, 8, 14), card, border_radius=14)
                pygame.draw.rect(canvas, RED, card, 4, border_radius=14)

                g_surf = font_title.render("APPEAL REJECTED", True, RED)
                case_lbl = render_fitted_line(f"FAILED AT: {chapter['title']}", font_small, GOLD, card_w - 40)
                sub1 = render_fitted_line(
                    f"{attorney_name} lost all credibility before Judge Dwyane!",
                    font_name, WHITE, card_w - 40
                )
                sub2 = font_name.render("[R] Retry Case   |   [ENTER] Return to Main Menu", True, CYAN)

                canvas.blit(case_lbl, (WIDTH // 2 - case_lbl.get_width() // 2, card.y + 24))
                canvas.blit(g_surf, (WIDTH // 2 - g_surf.get_width() // 2, card.y + 58))
                canvas.blit(sub1, (WIDTH // 2 - sub1.get_width() // 2, card.y + 132))
                canvas.blit(sub2, (WIDTH // 2 - sub2.get_width() // 2, card.y + 190))

            elif scene == "END":
                ending = ENDINGS_DB[resolved_ending_key]
                e_color = ending["color"]
                canvas.fill(BLACK)

                card = pygame.Rect(55, 72, 690, 456)
                pygame.draw.rect(canvas, NAVY, card, border_radius=14)
                pygame.draw.rect(canvas, e_color, card, 4, border_radius=14)

                banner_surf = font_name.render(ending["banner"], True, GOLD)
                title_surf = font_sub.render(ending["title"], True, e_color)
                canvas.blit(banner_surf, (WIDTH // 2 - banner_surf.get_width() // 2, 98))
                canvas.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 134))

                pygame.draw.line(canvas, GRAY, (95, 174), (705, 174), 1)
                draw_text_wrapped(
                    canvas,
                    ending["summary"],
                    90,
                    192,
                    620,
                    font_name,
                    WHITE,
                    max_height=205,
                    min_font_size=12
                )

                stats = f"Final Alignment — Truth Pursuit: {truth_score}   |   Client Shielding: {shield_score}"
                stat_surf = font_small.render(stats, True, CYAN)
                canvas.blit(stat_surf, (WIDTH // 2 - stat_surf.get_width() // 2, 424))

                sub_surf = font_small.render("[ENTER / CLICK] View Credits >>", True, GOLD)
                canvas.blit(sub_surf, (WIDTH // 2 - sub_surf.get_width() // 2, 474))

            elif scene == "CREDITS":
                canvas.fill(PURE_BLACK)
                page_obj = CREDITS_PAGES[credits_page_idx]
                total_pages = len(CREDITS_PAGES)

                frame = pygame.Rect(42, 36, WIDTH - 84, HEIGHT - 72)
                pygame.draw.rect(canvas, PURE_BLACK, frame, border_radius=14)
                pygame.draw.rect(canvas, GOLD if page_obj["page"] == 9 else BLUE_ACCENT, frame, 2, border_radius=14)

                page_tag = font_small.render(f"CREDITS  •  PAGE {page_obj['page']} / {total_pages}", True, GRAY)
                canvas.blit(page_tag, (WIDTH // 2 - page_tag.get_width() // 2, 56))

                hdr_surf = render_fitted_line(page_obj["header"], font_name, GOLD, WIDTH - 140)
                canvas.blit(hdr_surf, (WIDTH // 2 - hdr_surf.get_width() // 2, 86))
                pygame.draw.line(canvas, GRAY, (110, 114), (WIDTH - 110, 114), 1)

                cast_list = page_obj.get("cast", [])
                if cast_list:
                    for idx_member, member in enumerate(cast_list):
                        col_center_x = 235 if idx_member == 0 else 565
                        card_w, card_h = 285, 365
                        m_rect = pygame.Rect(col_center_x - card_w // 2, 134, card_w, card_h)
                        pygame.draw.rect(canvas, DARK_NAVY, m_rect, border_radius=12)
                        pygame.draw.rect(canvas, CYAN, m_rect, 2, border_radius=12)

                        # Displays original base character photo (idle pose: e.g., dwyane.png)
                        base_spr = assets.get_char_sprite(member["char"], "idle")
                        if base_spr:
                            scaled_spr = pygame.transform.smoothscale(base_spr, (215, 240))
                            canvas.blit(scaled_spr, (col_center_x - scaled_spr.get_width() // 2, 146))

                        file_lbl = font_small.render(f"[{member['file']}]", True, GRAY)
                        canvas.blit(file_lbl, (col_center_x - file_lbl.get_width() // 2, 396))

                        draw_text_wrapped(
                            canvas,
                            member["credit"],
                            m_rect.x + 14,
                            424,
                            card_w - 28,
                            font_main,
                            WHITE,
                            max_height=64,
                            min_font_size=12,
                            line_spacing=4,
                            center_x=col_center_x
                        )
                else:
                    main_line = page_obj["lines"][0] if page_obj["lines"] else ""
                    title_font = font_title if page_obj["page"] == 9 else font_sub
                    color_main = GOLD if page_obj["page"] == 9 else WHITE
                    draw_text_wrapped(
                        canvas,
                        main_line,
                        80,
                        HEIGHT // 2 - 28,
                        WIDTH - 160,
                        title_font,
                        color_main,
                        max_height=140,
                        min_font_size=16,
                        line_spacing=8,
                        center_x=WIDTH // 2
                    )

                is_last_page = (credits_page_idx == total_pages - 1)
                nav_text = (
                    "[ENTER / CLICK] Return to Main Menu"
                    if is_last_page
                    else "[ENTER / CLICK] Next Page >>   |   [LEFT] Previous"
                )
                nav_surf = font_small.render(nav_text, True, GOLD if is_last_page else CYAN)
                canvas.blit(nav_surf, (WIDTH // 2 - nav_surf.get_width() // 2, HEIGHT - 64))

            if shout_timer > 0:
                draw_ace_attorney_shout(
                    canvas,
                    shout_text,
                    shout_color,
                    assets.shouts.get(shout_text),
                    max(0, shout_duration - shout_timer),
                    tick
                )

            if flash_timer > 0:
                flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                alpha_val = min(180, flash_timer * 18)
                flash_surf.fill((flash_color[0], flash_color[1], flash_color[2], alpha_val))
                canvas.blit(flash_surf, (0, 0))

            if fade_alpha > 0:
                fade_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                fade_surf.fill((fade_color[0], fade_color[1], fade_color[2], min(255, fade_alpha)))
                canvas.blit(fade_surf, (0, 0))

            vp = get_viewport_rect(win_w, win_h)
            shake_scale_x = vp.width / WIDTH
            shake_scale_y = vp.height / HEIGHT
            if shake_timer > 0:
                offset_x = int((math.sin(tick * 3.1) * shake_intensity + math.cos(tick * 5.7) * (shake_intensity * 0.45)) * shake_scale_x)
                offset_y = int((math.cos(tick * 3.7) * (shake_intensity * 0.85) + math.sin(tick * 6.3) * (shake_intensity * 0.4)) * shake_scale_y)
            else:
                offset_x = 0
                offset_y = 0

            screen.fill(PURE_BLACK)
            if vp.size == (WIDTH, HEIGHT):
                screen.blit(canvas, (vp.x + offset_x, vp.y + offset_y))
            else:
                scaled_canvas = pygame.transform.smoothscale(canvas, vp.size)
                screen.blit(scaled_canvas, (vp.x + offset_x, vp.y + offset_y))
            pygame.display.flip()

        except Exception as err:
            traceback.print_exc()
            return_to_main_menu(f"* Error: {err}")


if __name__ == "__main__":
    main()