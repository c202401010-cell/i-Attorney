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
GOLD = (255, 200, 50)
ORANGE_SPARK = (230, 105, 20)
CYAN = (70, 220, 245)
GREEN = (75, 215, 120)
RED = (235, 65, 75)
CRIMSON = (150, 22, 36)
PURPLE_ACCENT = (175, 110, 245)
GRAY = (150, 160, 175)

font_shout = pygame.font.SysFont("arial", 72, bold=True)
font_title = pygame.font.SysFont("arial", 44, bold=True)
font_menu = pygame.font.SysFont("arialblack,arial", 38, bold=True)
font_logo_word = pygame.font.SysFont("arialblack,arial", 46, bold=True)
font_logo_i = pygame.font.SysFont("georgia,timesnewroman", 76, bold=True)
font_sub = pygame.font.SysFont("consolas", 23, bold=True)
font_main = pygame.font.SysFont("consolas", 18, bold=True)
font_name = pygame.font.SysFont("consolas", 16, bold=True)
font_small = pygame.font.SysFont("consolas", 14, bold=True)

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
        "title_logo": {"file": "title_logo.png", "size": [485, 175]}
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
            "poses": {"idle": "dwyane.png"}
        },
        "CFO": {
            "folder": "cfo",
            "size": [430, 410],
            "poses": {"idle": "cfo.png"}
        },
        "Accountant": {
            "folder": "accountant",
            "size": [430, 410],
            "poses": {"idle": "accountant.png"}
        },
        "Employee": {
            "folder": "employee",
            "size": [430, 410],
            "poses": {"idle": "employee.png"}
        }
    }
}

STORY_REGISTRY = {
    "Dave": DAVE_STORY,
    "Tyrone": TYRONE_STORY
}

ENDINGS_DB = {
    "DAVE_VICTORY": {
        "banner": "ENDING 1 OF 3: DAVE'S VICTORY",
        "title": "THE UNBROKEN SHIELD",
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
            ("Dwyane", "Mr. Elijah is acquitted of all charges and retains full executive authority. Mr. Kendall is barred from corporate office, and the CFO is remanded into custody. Court is adjourned!", "idle")
        ]
    },
    "TYRONE_VICTORY": {
        "banner": "ENDING 2 OF 3: TYRONE'S VICTORY",
        "title": "THE STRATEGIST'S CHECKMATE",
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
            ("Dwyane", "Mr. Kendall is cleared of all liability and confirmed as sole Chief Executive. Mr. Elijah is removed from management, and the CFO stands indicted. Court is adjourned!", "idle")
        ]
    },
    "TRUE_ENDING": {
        "banner": "ENDING 3 OF 3: THE TRUE ENDING",
        "title": "THE PRICE OF GREED",
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
            ("Dwyane", "The CFO is indicted for grand embezzlement, and both founding partners shall submit to independent compliance oversight. Justice is served!", "idle")
        ]
    }
}


def build_wrong_evidence_dialogue(attorney_name, witness_name, ev_name, remaining_hp):
    """Generates unique, in-character dialogue lines when counsel presents irrelevant evidence."""
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
            "Nice dramatic finger-point, Counselor—too bad that exhibit has zero connection to what I just testified.",
            "Are you seriously waving that around in front of institutional observers? It doesn't contradict a syllable I said.",
            "I expected sharper due diligence from a trial attorney. That document proves nothing about my statement."
        ],
        "CFO": [
            "With respect, Counselor, that exhibit doesn't even share a fiscal quarter with the statement on the stand!",
            "You're grasping at random binders now. Not a single line on that page refutes my testimony.",
            "If that's the sharpest arrow in your quiver, this cross-examination is already over."
        ],
        "Elijah": [
            "Wait—why are you showing me that? That document doesn't have anything to do with what I just said!",
            "I'm trying to answer honestly, Counselor, but that exhibit doesn't contradict my statement at all!",
            "Look at the dates on that file again—it doesn't line up with the testimony you're challenging!"
        ],
        "Accountant": [
            "U-Um, pardon me, Counselor, but if you check the reference code, that exhibit doesn't actually relate to what I just testified...",
            "I double-checked every ledger myself, and... well, that document doesn't contradict my statement at all.",
            "A-Are you sure you pulled the right folder? That exhibit covers a completely different issue."
        ],
        "Employee": [
            "I'm really trying to help the court find the truth, Counselor, but that document doesn't match what I just said...",
            "Please check the Court Record again—that exhibit isn't connected to the part of my testimony you're pressing!",
            "Oh... that's not the file that proves what happened. Look closely at the details in my statement!"
        ]
    }
    w_reply = random.choice(witness_replies.get(
        witness_name,
        ["That exhibit has zero bearing on my testimony, Counselor."]
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
            (witness_name, w_reply, "idle"),
            ("Dwyane", judge_warn, "idle", "whoops"),
            counsel_react,
            ("Dwyane", judge_end, "idle")
        ]

    judge_penalties = [
        f"This is a court of law, {attorney_name}, not a guessing game! Penalty assessed! ({remaining_hp} credibility remaining)",
        f"Connect your exhibits to the testimony before shouting, {attorney_name}! Penalty issued! ({remaining_hp} credibility remaining)",
        f"Irrelevant filing! One more careless swing like that and you'll be arguing from the hallway, {attorney_name}! ({remaining_hp} remaining)"
    ]
    if attorney_name == "Dave":
        follow_up = ("Dave", "(Calm down, Dave! Read the witness's exact words and match them to the right piece of evidence!)", "think")
    else:
        follow_up = ("Tyrone", "(Sloppy, Tyrone. Re-read the testimony line by line and strike only where the logic fractures.)", "think")

    return [
        (attorney_name, opener, "point"),
        (witness_name, w_reply, "idle"),
        ("Dwyane", random.choice(judge_penalties), "idle", "whoops"),
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

        folders = self.data.get("folders", {})
        self.bg_dir = os.path.join(BASE_DIR, folders.get("bg", "assets/bg"))
        self.char_dir = os.path.join(BASE_DIR, folders.get("char", "assets/char"))
        self.icon_dir = os.path.join(BASE_DIR, folders.get("icon", "assets/icon"))
        self.sounds_dir = os.path.join(BASE_DIR, folders.get("sounds", "assets/sounds"))

        for path in (self.bg_dir, self.char_dir, self.icon_dir, self.sounds_dir):
            os.makedirs(path, exist_ok=True)

        self.backgrounds = {}
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

    def _load_surface(self, base_dir, filename, size, fallback_color, label="", optional=False, trim_vertical=False):
        found_path = self._find_file_case_insensitive(base_dir, filename)
        if found_path:
            try:
                img = pygame.image.load(found_path).convert_alpha()
                if trim_vertical:
                    bbox = img.get_bounding_rect()
                    if bbox.width > 0 and bbox.height > 0:
                        img = img.subsurface(pygame.Rect(0, bbox.top, img.get_width(), bbox.height)).copy()
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
            if bg_key == "title_logo":
                self.backgrounds["title_logo"] = self._load_surface(
                    self.bg_dir, cfg["file"], cfg["size"], NAVY, optional=True
                )
            else:
                self.backgrounds[bg_key] = self._load_surface(
                    self.bg_dir, cfg["file"], cfg["size"], (26, 36, 58)
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
            poses = cfg.get("poses")
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
        return char_poses.get(pose) or char_poses.get("idle")


def draw_fallback_logo(surface, x, y):
    cx, cy = x + 52, y + 72
    r = 56
    hex_pts = []
    for i in range(6):
        ang = math.radians(60 * i - 90)
        hex_pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    pygame.draw.polygon(surface, BLUE_ACCENT, hex_pts)

    i_surf = font_logo_i.render("I", True, WHITE)
    surface.blit(i_surf, (cx - i_surf.get_width() // 2, cy - i_surf.get_height() // 2 - 2))

    sx, sy = cx + 68, cy - 22
    pygame.draw.circle(surface, ORANGE_SPARK, (sx, sy), 42, 3)
    star_pts = [
        (sx - 56, sy - 64),
        (sx + 8, sy - 10),
        (sx + 68, sy - 42),
        (sx + 12, sy + 6),
        (sx + 58, sy + 56),
        (sx - 4, sy + 10),
        (sx - 54, sy + 46),
        (sx - 10, sy - 6),
    ]
    pygame.draw.polygon(surface, ORANGE_SPARK, star_pts)
    pygame.draw.circle(surface, (255, 245, 160), (sx, sy), 13)

    word_surf = font_logo_word.render("ATTORNEY", True, WHITE)
    surface.blit(word_surf, (cx + 48, cy + 4))


def draw_text_wrapped(surface, text, x, y, max_width, font, color=WHITE):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        test = current + word + " "
        if font.size(test)[0] < max_width:
            current = test
        else:
            lines.append(current)
            current = word + " "
    lines.append(current)

    for line in lines:
        surface.blit(font.render(line, True, color), (x, y))
        y += font.get_height() + 5


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
        "START",
        "LOAD",
        "CHAPTER",
        "CERTIFICATES",
        "QUIT"
    ]
    title_idx = 0

    story_keys = ["Dave", "Tyrone"]
    story_select_idx = 0
    story_select_mode = "PLAY"
    active_story = DAVE_STORY

    chapter_select_idx = 0
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
    shake_timer = 0
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
        if final_case_trigger == "FULL_TRUTH" and truth_score >= shield_score:
            return "TRUE_ENDING"
        if attorney == "Dave":
            return "DAVE_VICTORY"
        return "TYRONE_VICTORY"

    def trigger_shout(text, color=GOLD, shake=20, hold=65, snd_key=None, flash=10):
        nonlocal shout_text, shout_color, shout_timer, shake_timer, input_lock_timer, flash_timer, flash_color
        shout_text = text
        shout_color = color
        shout_timer = hold
        shake_timer = shake
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
                shake=26 if is_correct else 22,
                hold=68,
                snd_key="take_that",
                flash=12 if is_correct else 10
            )
        else:
            trigger_shout(
                "OBJECTION!",
                BLUE_ACCENT,
                shake=26 if is_correct else 22,
                hold=68,
                snd_key="objection",
                flash=12 if is_correct else 10
            )

    def trigger_impact(shake=14, flash=8, color=WHITE, play_bang=False):
        nonlocal shake_timer, flash_timer, flash_color
        shake_timer = max(shake_timer, shake)
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
        trigger_impact(shake=26, flash=14, color=RED)

    def enter_case_verdict():
        nonlocal scene, verdict_anim_tick, input_lock_timer
        scene = "CASE_VERDICT"
        verdict_anim_tick = 0
        input_lock_timer = 22
        trigger_impact(shake=8, flash=8, color=GOLD)

    def return_to_main_menu(msg=""):
        nonlocal scene, current_chapter_idx, dialogue_queue, cur_speaker, cur_line, cur_pose, prev_speaker
        nonlocal char_idx, card_timer, title_idx, title_msg, show_record, health, shout_timer, input_lock_timer
        nonlocal truth_score, shield_score, final_case_trigger, flash_timer
        scene = "TITLE"
        current_chapter_idx = 0
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
                trigger_shout("OBJECTION!", BLUE_ACCENT, shake=20, hold=48, snd_key="objection", flash=10)
            elif low_line.startswith("hold it"):
                trigger_shout("HOLD IT!", GOLD, shake=16, hold=45, snd_key="hold_it", flash=8)
            elif pose == "point" or any(
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
            card_timer = 165
            card_anim_tick = 0
            input_lock_timer = 30
            scene = "CHAPTER_CARD"
            assets.play_sound("testimony", stop_previous=True)

        transition_with_fade(_open_card)

    def begin_chapter_dialogue():
        chapter = active_story["chapters"][current_chapter_idx]
        transition_with_fade(lambda: queue_dialogue(chapter["intro"], "CROSS_EXAM"))

    def execute_title_option(opt):
        nonlocal story_select_idx, story_select_mode, input_lock_timer, scene
        nonlocal active_story, truth_score, shield_score, title_msg
        if opt == "START":
            def _go_select():
                nonlocal story_select_idx, story_select_mode, input_lock_timer, scene
                story_select_idx = 0
                story_select_mode = "PLAY"
                input_lock_timer = 10
                scene = "STORY_SELECT"
            transition_with_fade(_go_select)
        elif opt == "LOAD":
            saved = progress.get("last_run")
            if not saved or saved.get("attorney") not in STORY_REGISTRY:
                title_msg = "* No saved game found yet!"
            else:
                active_story = STORY_REGISTRY[saved["attorney"]]
                truth_score = saved.get("truth_score", 0)
                shield_score = saved.get("shield_score", 0)
                saved_ch = min(saved.get("chapter_idx", 0), len(active_story["chapters"]) - 1)
                start_chapter(saved_ch, play_prologue=False, reset_scores=False)
        elif opt == "CHAPTER":
            def _go_ch_select():
                nonlocal story_select_idx, story_select_mode, input_lock_timer, scene
                story_select_idx = 0
                story_select_mode = "CHAPTER_SELECT"
                input_lock_timer = 10
                scene = "STORY_SELECT"
            transition_with_fade(_go_ch_select)
        elif opt == "CERTIFICATES":
            def _go_certs():
                nonlocal input_lock_timer, scene
                input_lock_timer = 10
                scene = "CERTIFICATES"
            transition_with_fade(_go_certs)
        elif opt == "QUIT":
            pygame.quit()
            sys.exit()

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
                    for i in range(len(title_options)):
                        item_rect = pygame.Rect(24, 218 + i * 72, 420, 56)
                        if item_rect.collidepoint(mx, my):
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
                        if event.key == pygame.K_UP:
                            title_idx = (title_idx - 1) % len(title_options)
                            title_msg = ""
                        elif event.key == pygame.K_DOWN:
                            title_idx = (title_idx + 1) % len(title_options)
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
                                trigger_shout("HOLD IT!", GOLD, shake=18, hold=60, snd_key="hold_it", flash=8)
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
                                    press_lines.append(("Dwyane", "Witness, enter that clarification into your official testimony!", "idle"))
                                elif cur_stmt.get("unlocked_already") and stmt_idx + 1 < len(statements):
                                    stmt_idx += 1
                                queue_dialogue(press_lines, "CROSS_EXAM")
                            elif event.key == pygame.K_o:
                                show_record = True
                                input_lock_timer = 8

                    elif scene in ("END", "GAME_OVER"):
                        if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE, pygame.K_r):
                            if scene == "GAME_OVER" and event.key == pygame.K_r:
                                start_chapter(current_chapter_idx, reset_scores=False)
                            else:
                                transition_with_fade(return_to_main_menu)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if input_lock_timer > 0 or shout_timer > 0 or fade_dir != 0:
                        continue
                    mx, my = screen_to_virtual(event.pos, win_w, win_h)
                    if scene == "TITLE":
                        for i, opt in enumerate(title_options):
                            item_rect = pygame.Rect(24, 218 + i * 72, 420, 56)
                            if item_rect.collidepoint(mx, my):
                                title_idx = i
                                execute_title_option(opt)
                                break
                    elif scene == "CERTIFICATES":
                        transition_with_fade(return_to_main_menu)
                    elif scene == "CHAPTER_CARD":
                        begin_chapter_dialogue()
                    elif scene == "DIALOGUE":
                        advance_dialogue()
                    elif scene == "CASE_VERDICT":
                        start_chapter(current_chapter_idx + 1, reset_scores=False)
                    elif scene in ("END", "GAME_OVER"):
                        transition_with_fade(return_to_main_menu)

            # --- UPDATES ---
            if scene == "CHAPTER_CARD":
                card_anim_tick += 1
                card_timer -= 1
                if card_timer <= 0 and fade_dir == 0:
                    begin_chapter_dialogue()
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
                canvas.fill(PURE_BLACK)

                logo_img = assets.backgrounds.get("title_logo")
                if logo_img:
                    canvas.blit(logo_img, (22, 16))
                else:
                    draw_fallback_logo(canvas, 22, 16)

                for i, opt in enumerate(title_options):
                    is_sel = (i == title_idx)
                    item_y = 224 + i * 72
                    if is_sel:
                        pygame.draw.rect(canvas, GOLD, (14, item_y + 8, 6, 36), border_radius=3)
                    color = GOLD if is_sel else WHITE
                    opt_surf = font_menu.render(opt, True, color)
                    canvas.blit(opt_surf, (30, item_y))

                fs_state = "FULLSCREEN" if is_fullscreen else "WINDOWED"
                fs_hint = font_small.render(f"[F11] Toggle Fullscreen ({fs_state})", True, GRAY)
                canvas.blit(fs_hint, (WIDTH - fs_hint.get_width() - 22, 574))

                if title_msg:
                    msg_surf = font_small.render(title_msg, True, CYAN)
                    canvas.blit(msg_surf, (30, 574))

            elif scene == "CERTIFICATES":
                canvas.fill(PURE_BLACK)
                hdr = font_sub.render("BUSINESS ETHICS CERTIFICATES & ENDINGS", True, GOLD)
                canvas.blit(hdr, (40, 34))
                pygame.draw.line(canvas, GRAY, (40, 72), (760, 72), 1)

                end_hdr = font_name.render(f"UNLOCKED ENDINGS ({len(progress['endings'])}/3):", True, CYAN)
                canvas.blit(end_hdr, (40, 90))
                for idx_e, (ekey, edata) in enumerate(ENDINGS_DB.items()):
                    unlocked = ekey in progress["endings"]
                    status = edata["title"] if unlocked else "LOCKED"
                    col = edata["color"] if unlocked else GRAY
                    e_surf = font_small.render(f"• {edata['banner']}: {status}", True, col)
                    canvas.blit(e_surf, (52, 120 + idx_e * 26))

                cert_hdr = font_name.render(f"EARNED ETHICS CERTIFICATES ({len(progress['certificates'])}/10):", True, GREEN)
                canvas.blit(cert_hdr, (40, 218))

                if not progress["certificates"]:
                    none_surf = font_small.render("Complete cases in Dave's or Tyrone's campaign to earn certificates.", True, GRAY)
                    canvas.blit(none_surf, (52, 250))
                else:
                    for idx_c, cert_txt in enumerate(progress["certificates"][:9]):
                        c_surf = font_small.render(f"✓ {cert_txt[:74]}", True, WHITE)
                        canvas.blit(c_surf, (52, 248 + idx_c * 28))

                back_surf = font_small.render("[ENTER / ESC / CLICK] Return to Main Menu", True, GOLD)
                canvas.blit(back_surf, (40, 550))

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

                    lbl = font_main.render(("> " if is_sel else "  ") + key.upper(), True, GOLD if is_sel else WHITE)
                    story_lbl = font_small.render(st["subtitle"], True, CYAN if is_sel else GRAY)
                    client_lbl = font_small.render(f"Client: {client_name} | Rival: {rival_name}", True, WHITE if is_sel else GRAY)
                    canvas.blit(lbl, (card_x + 145 - lbl.get_width() // 2, 365))
                    canvas.blit(story_lbl, (card_x + 145 - story_lbl.get_width() // 2, 398))
                    canvas.blit(client_lbl, (card_x + 145 - client_lbl.get_width() // 2, 432))

                action_label = "Start Campaign" if story_select_mode == "PLAY" else "View Chapters"
                hint = font_name.render(f"[LEFT/RIGHT] Select  |  [ENTER] {action_label}  |  [ESC] Back", True, GRAY)
                canvas.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 528))

            elif scene == "CHAPTER_SELECT":
                canvas.fill(BLACK)
                header = font_sub.render(active_story["title"], True, GOLD)
                canvas.blit(header, (WIDTH // 2 - header.get_width() // 2, 75))

                chapters = active_story["chapters"]
                for i, ch in enumerate(chapters):
                    theme_c = get_case_theme(i)["accent"]
                    color = theme_c if i == chapter_select_idx else WHITE
                    prefix = "> " if i == chapter_select_idx else "  "
                    lbl = font_main.render(prefix + ch["title"], True, color)
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

                    route_tag = font_small.render(active_story["title"], True, GRAY)
                    phase_tag = font_small.render(theme["tag"], True, accent)
                    parts = chapter["title"].split(": ")
                    ch_num = font_sub.render(parts[0], True, WHITE)
                    ch_sub = font_title.render(parts[1] if len(parts) > 1 else "", True, accent)

                    canvas.blit(route_tag, (WIDTH // 2 - route_tag.get_width() // 2, 186))
                    canvas.blit(phase_tag, (WIDTH // 2 - phase_tag.get_width() // 2, 212))

                    line_half = int(260 * slide_ease)
                    pygame.draw.line(canvas, accent, (WIDTH // 2 - line_half, 242), (WIDTH // 2 + line_half, 242), 2)

                    canvas.blit(ch_num, (WIDTH // 2 - ch_num.get_width() // 2 + left_shift, 260))
                    canvas.blit(ch_sub, (WIDTH // 2 - ch_sub.get_width() // 2 + right_shift, 302))

                    eth_lbl = font_small.render(f"FOCUS: {chapter.get('ethics_topic', '')}", True, GOLD)
                    canvas.blit(eth_lbl, (WIDTH // 2 - eth_lbl.get_width() // 2, 372))

                if card_anim_tick >= 36:
                    prompt = font_small.render("[ENTER / CLICK] Enter Courtroom >>", True, WHITE)
                    canvas.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 456))

            elif scene == "DECISION":
                theme = get_case_theme(current_chapter_idx)
                accent = theme["accent"]
                canvas.fill(BLACK)
                chapter = active_story["chapters"][current_chapter_idx]
                dec = chapter["decision"]

                card = pygame.Rect(55, 110, 690, 380)
                pygame.draw.rect(canvas, DARK_NAVY, card, border_radius=12)
                pygame.draw.rect(canvas, accent, card, 3, border_radius=12)

                tag = font_sub.render("ETHICAL CROSSROADS — MAKE YOUR DECISION", True, GOLD)
                canvas.blit(tag, (WIDTH // 2 - tag.get_width() // 2, 138))

                draw_text_wrapped(canvas, dec["prompt"], 90, 195, 620, font_main, CYAN)

                for i, opt in enumerate(dec["options"]):
                    is_sel = (i == decision_idx)
                    opt_rect = pygame.Rect(85, 290 + i * 72, 630, 56)
                    pygame.draw.rect(canvas, NAVY if is_sel else BLACK, opt_rect, border_radius=8)
                    pygame.draw.rect(canvas, GOLD if is_sel else GRAY, opt_rect, 2, border_radius=8)
                    lbl = font_small.render(("> " if is_sel else "  ") + opt["label"], True, GOLD if is_sel else WHITE)
                    canvas.blit(lbl, (opt_rect.x + 14, opt_rect.y + 18))

                hint = font_small.render("[UP/DOWN] Choose Stance   |   [ENTER] Confirm Decision", True, GREEN)
                canvas.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 455))

            elif scene == "CASE_VERDICT":
                theme = get_case_theme(current_chapter_idx)
                accent = theme["accent"]
                canvas.fill(BLACK)
                chapter = active_story["chapters"][current_chapter_idx]

                v_ease = min(1.0, verdict_anim_tick / 18.0)
                card_y = int(145 + (1.0 - v_ease) * 35)
                card = pygame.Rect(70, card_y, 660, 305)
                pygame.draw.rect(canvas, theme["card_bg"], card, border_radius=12)
                pygame.draw.rect(canvas, GREEN, card, 3, border_radius=12)

                v_title = font_sub.render(f"{chapter['title']} — VERDICT SECURED!", True, GREEN)
                eth_hdr = font_name.render("BUSINESS ETHICS PRINCIPLE UNLOCKED:", True, GOLD)
                canvas.blit(v_title, (WIDTH // 2 - v_title.get_width() // 2, card_y + 30))
                canvas.blit(eth_hdr, (WIDTH // 2 - eth_hdr.get_width() // 2, card_y + 86))
                draw_text_wrapped(
                    canvas,
                    chapter.get("ethics_topic", "Corporate accountability and integrity."),
                    110, card_y + 122, 580, font_main, accent
                )

                alignment_txt = f"Truth Pursuit: {truth_score}   |   Client Shielding: {shield_score}"
                align_surf = font_small.render(alignment_txt, True, GRAY)
                canvas.blit(align_surf, (WIDTH // 2 - align_surf.get_width() // 2, card_y + 210))

                cont = font_small.render("[ENTER / CLICK] Advance to Next Case >>", True, WHITE)
                canvas.blit(cont, (WIDTH // 2 - cont.get_width() // 2, card_y + 260))

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
                    stage_pose = "idle"
                    is_talking = False

                char_bob_y = int(abs(math.sin(tick * 0.28)) * 5) if is_talking else 0
                portrait = assets.get_char_sprite(stage_speaker, stage_pose)
                if portrait:
                    char_x = WIDTH // 2 - portrait.get_width() // 2 + slide_offset
                    textbox_top = 395 if scene == "DIALOGUE" else 385
                    anchor_bottom_y = textbox_top + 78
                    char_y = anchor_bottom_y - portrait.get_height() + char_bob_y
                    canvas.blit(portrait, (char_x, char_y))

                pygame.draw.rect(canvas, NAVY, (0, 0, WIDTH, 56))
                pygame.draw.line(canvas, accent, (0, 56), (WIDTH, 56), 3)
                hud_left = font_name.render(f"{chapter['title']} | {attorney_name}", True, accent)
                canvas.blit(hud_left, (18, 18))

                hp_str = "CREDIBILITY: " + ("[!]" * health) + (" . " * (5 - health))
                hp_color = GREEN if health >= 3 else RED
                hp_surf = font_name.render(hp_str, True, hp_color)
                canvas.blit(hp_surf, (WIDTH - hp_surf.get_width() - 18, 18))

                if scene == "DIALOGUE":
                    box = pygame.Rect(40, 395, 720, 175)
                    pygame.draw.rect(canvas, NAVY, box, border_radius=10)
                    pygame.draw.rect(canvas, accent, box, 3, border_radius=10)

                    tag_color = CYAN if cur_speaker == attorney_name else GOLD
                    canvas.blit(font_name.render(cur_speaker.upper(), True, tag_color), (box.x + 20, box.y + 14))
                    draw_text_wrapped(canvas, cur_line[:char_idx], box.x + 20, box.y + 46, box.width - 40, font_main, WHITE)

                    if char_idx >= len(cur_line) and line_done_hold <= 0 and shout_timer <= 0:
                        blink = " >>" if (tick // 20) % 2 == 0 else "   "
                        hint = font_small.render(f"[ENTER / CLICK] Continue{blink}", True, GOLD)
                        canvas.blit(hint, (box.right - hint.get_width() - 20, box.bottom - 26))

                elif scene == "CROSS_EXAM":
                    ce_badge = pygame.Rect(40, 68, 330, 32)
                    pygame.draw.rect(canvas, RED, ce_badge, border_radius=6)
                    ce_lbl = font_small.render(f"CROSS-EXAMINATION ({stmt_idx + 1}/{len(statements)})", True, WHITE)
                    canvas.blit(ce_lbl, (ce_badge.x + 12, ce_badge.y + 7))

                    box = pygame.Rect(40, 385, 720, 185)
                    pygame.draw.rect(canvas, NAVY, box, border_radius=10)
                    pygame.draw.rect(canvas, GOLD, box, 3, border_radius=10)

                    canvas.blit(font_name.render(f"{stage_speaker.upper()} - TESTIMONY", True, GOLD), (box.x + 20, box.y + 12))
                    stmt_text = f'"{statements[stmt_idx]["text"]}"'
                    draw_text_wrapped(canvas, stmt_text, box.x + 20, box.y + 42, box.width - 40, font_main, CYAN)

                    pygame.draw.line(canvas, GRAY, (box.x + 16, box.bottom - 38), (box.right - 16, box.bottom - 38), 1)
                    controls = "[<-/->] Statement   [H] Hold It! (Press)   [O / TAB] Court Record & Object"
                    ctrl_surf = font_small.render(controls, True, WHITE)
                    canvas.blit(ctrl_surf, (box.x + 20, box.bottom - 28))

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
                            lbl = font_main.render(("> " if is_sel else "  ") + ev["name"], True, GOLD if is_sel else WHITE)
                            canvas.blit(lbl, (row.x + 14, row.y + 5))

                        desc_box = pygame.Rect(100, 375, 600, 105)
                        pygame.draw.rect(canvas, NAVY, desc_box, border_radius=8)
                        pygame.draw.rect(canvas, CYAN, desc_box, 2, border_radius=8)
                        cur_ev = evidence_db[active_evidence[record_idx]]
                        draw_text_wrapped(canvas, cur_ev["desc"], desc_box.x + 14, desc_box.y + 12, desc_box.width - 28, font_name, WHITE)

                        m_hint = font_small.render("[UP/DOWN] Browse   [O / ENTER] PRESENT EVIDENCE   [TAB / ESC] Close", True, GREEN)
                        canvas.blit(m_hint, (WIDTH // 2 - m_hint.get_width() // 2, 502))

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
                case_lbl = font_small.render(f"FAILED AT: {chapter['title']}", True, GOLD)
                sub1 = font_name.render(f"{attorney_name} lost all credibility before Judge Dwyane!", True, WHITE)
                sub2 = font_name.render("[R] Retry Case   |   [ENTER] Return to Main Menu", True, CYAN)

                canvas.blit(case_lbl, (WIDTH // 2 - case_lbl.get_width() // 2, card.y + 24))
                canvas.blit(g_surf, (WIDTH // 2 - g_surf.get_width() // 2, card.y + 58))
                canvas.blit(sub1, (WIDTH // 2 - sub1.get_width() // 2, card.y + 132))
                canvas.blit(sub2, (WIDTH // 2 - sub2.get_width() // 2, card.y + 190))

            elif scene == "END":
                ending = ENDINGS_DB[resolved_ending_key]
                e_color = ending["color"]
                canvas.fill(BLACK)

                card = pygame.Rect(60, 85, 680, 430)
                pygame.draw.rect(canvas, NAVY, card, border_radius=14)
                pygame.draw.rect(canvas, e_color, card, 4, border_radius=14)

                banner_surf = font_name.render(ending["banner"], True, GOLD)
                title_surf = font_sub.render(ending["title"], True, e_color)
                canvas.blit(banner_surf, (WIDTH // 2 - banner_surf.get_width() // 2, 115))
                canvas.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 152))

                pygame.draw.line(canvas, GRAY, (100, 195), (700, 195), 1)
                draw_text_wrapped(canvas, ending["summary"], 95, 215, 610, font_name, WHITE)

                stats = f"Final Alignment — Truth Pursuit: {truth_score}   |   Client Shielding: {shield_score}"
                stat_surf = font_small.render(stats, True, CYAN)
                canvas.blit(stat_surf, (WIDTH // 2 - stat_surf.get_width() // 2, 415))

                sub_surf = font_small.render("[ENTER / CLICK] Return to Main Menu", True, GOLD)
                canvas.blit(sub_surf, (WIDTH // 2 - sub_surf.get_width() // 2, 465))

            if shout_timer > 0:
                dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                dim.fill((0, 0, 0, 110))
                canvas.blit(dim, (0, 0))

                banner_rect = pygame.Rect(110, 215, 580, 120)
                pygame.draw.rect(canvas, BLACK, banner_rect, border_radius=14)
                pygame.draw.rect(canvas, shout_color, banner_rect, 5, border_radius=14)
                s_surf = font_shout.render(shout_text, True, shout_color)
                canvas.blit(s_surf, (WIDTH // 2 - s_surf.get_width() // 2, 235))

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
            offset_x = int(math.sin(tick * 1.9) * 8 * shake_scale_x) if shake_timer > 0 else 0
            offset_y = int(math.cos(tick * 2.3) * 6 * shake_scale_y) if shake_timer > 0 else 0

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