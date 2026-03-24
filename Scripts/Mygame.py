import random
import math
from typing import List, Dict, Tuple, Optional
import pygame


# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Player settings
PLAYER_SIZE = 50
PLAYER_SPEED = 5
PLAYER_MAX_HP = 3


# Dash settings
DASH_SPEED = 900          # pixels per second during dash
DASH_DURATION_MS = 150    # how long the dash lasts (ms)
DASH_COOLDOWN_MS = 400    # cooldown before next dash (ms)

# Dash state (module-level, reset on game restart via reset_dash_state())
_dash_state = {
    "active":      False,
    "start_ms":    0,
    "cooldown_ms": 0,
    "dir":         None,   # pygame.Vector2 unit direction
    "last_move":   pygame.Vector2(1, 0),  # fallback direction
}

# Enemy settings
ENEMY_RADIUS = 22
ENEMY_SPEED = 2
ENEMY_SPAWN_MIN_MS = 800
ENEMY_SPAWN_MAX_MS = 2500
ENEMY_MAX_HP = 4

# Projectile settings
PROJECTILE_SPEED = 8
PROJECTILE_RADIUS = 5
PROJECTILE_COOLDOWN_MS = 200
MAX_AMMO = 15
RELOAD_TIME_MS = 2000

# EXP / Level settings
EXP_PER_KILL = 20
EXP_TO_LEVEL = 100       # base EXP needed per level
EXP_SCALE = 1.3          # each level costs 30% more EXP

# EXP Star settings
STAR_LIFETIME_MS = 4000
STAR_RADIUS = 8
STAR_SPEED = 1.5
STAR_MAGNET_RANGE = 150
STAR_MAGNET_SPEED = 4

# Power-up durations (ms)
POWERUP_LIFESTEAL_DURATION = 8000
POWERUP_TIMEDIL_DURATION   = 5000
POWERUP_PIERCING_DURATION  = 10000
POWERUP_DRONE_DURATION     = 12000
DRONE_FIRE_RATE_MS         = 600
DRONE_PROJ_SPEED           = 6
SHOCKWAVE_COOLDOWN_MS      = 7000
SHOCKWAVE_RADIUS           = 280
SHOCKWAVE_PUSH_FORCE       = 250
SHOCKWAVE_DAMAGE_RATIO     = 0.50

# Colors
BLACK       = (0,   0,   0  )
RED         = (255, 0,   0  )
GREEN       = (0,   255, 0  )
BLUE        = (0,   128, 255)
WHITE       = (255, 255, 255)
YELLOW      = (255, 220, 50 )
GOLD        = (255, 180, 0  )
PURPLE      = (180, 80,  255)
CYAN        = (0,   230, 255)
ORANGE      = (255, 140, 0  )
LIGHT_GREEN = (100, 255, 140)

POWERUP_DEFS = [
    {
        "id": "shockwave",
        "name": "Shockwave Burst",
        "desc": "Push enemies away in a circle + 12% damage (7s cooldown, press E)",
        "color": CYAN,
    },
    {
        "id": "lifesteal",
        "name": "Lifesteal Module",
        "desc": "Heal 5% of damage dealt for 8 seconds",
        "color": LIGHT_GREEN,
    },
    {
        "id": "drone",
        "name": "Turret Drone",
        "desc": "Auto-firing drone ally for 12 seconds",
        "color": ORANGE,
    },
    {
        "id": "timedil",
        "name": "Time Dilation",
        "desc": "Enemies move 40% slower for 5 seconds",
        "color": PURPLE,
    },
    {
        "id": "piercing",
        "name": "Piercing Rounds",
        "desc": "Bullets pass through 2 extra enemies for 10 seconds",
        "color": GOLD,
    },
]


# ────────────────────────── helpers ──────────────────────────────

def exp_needed(level: int) -> int:
    return int(EXP_TO_LEVEL * (EXP_SCALE ** (level - 1)))


def pick_3_powerups() -> List[Dict]:
    return random.sample(POWERUP_DEFS, 3)


# ────────────────────────── movement ─────────────────────────────

def reset_dash_state() -> None:
    """Call this when restarting the game to clear any active dash."""
    _dash_state["active"]      = False
    _dash_state["start_ms"]    = 0
    _dash_state["cooldown_ms"] = 0
    _dash_state["dir"]         = None
    _dash_state["last_move"]   = pygame.Vector2(1, 0)


def try_trigger_dash() -> None:
    """Call this on KEYDOWN for K_LSHIFT to start a dash burst."""
    now = pygame.time.get_ticks()
    if _dash_state["active"]:
        return
    if now - _dash_state["cooldown_ms"] < DASH_COOLDOWN_MS:
        return
    # Direction: last held movement, or last_move fallback
    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_a]: dx -= 1
    if keys[pygame.K_d]: dx += 1
    if keys[pygame.K_w]: dy -= 1
    if keys[pygame.K_s]: dy += 1
    if dx == 0 and dy == 0:
        d = _dash_state["last_move"]
    else:
        d = pygame.Vector2(dx, dy).normalize()
    _dash_state["active"]    = True
    _dash_state["start_ms"]  = now
    _dash_state["dir"]       = pygame.Vector2(d)


def handle_movement(player_rect: pygame.Rect, keys: pygame.key.ScancodeWrapper, dt: float) -> None:
    """Move player each frame. dt = seconds since last frame."""
    now = pygame.time.get_ticks()

    # ── Dash movement ──────────────────────────────────────────────
    ds = _dash_state
    if ds["active"]:
        elapsed = now - ds["start_ms"]
        if elapsed < DASH_DURATION_MS:
            d = ds["dir"]
            move = d * DASH_SPEED * dt
            player_rect.move_ip(move.x, move.y)
            return   # skip normal movement while dashing
        else:
            # dash finished
            ds["active"]      = False
            ds["cooldown_ms"] = now

    # ── Normal movement ────────────────────────────────────────────
    dx = dy = 0
    if keys[pygame.K_a]: dx -= 1
    if keys[pygame.K_d]: dx += 1
    if keys[pygame.K_w]: dy -= 1
    if keys[pygame.K_s]: dy += 1

    if dx != 0 or dy != 0:
        v = pygame.Vector2(dx, dy).normalize() * PLAYER_SPEED
        player_rect.move_ip(v.x, v.y)
        ds["last_move"] = pygame.Vector2(dx, dy).normalize()


def get_player_color(state: Dict) -> Tuple[int, int, int]:
    if state.get("lifesteal_until", 0) > pygame.time.get_ticks():
        return LIGHT_GREEN
    mouse_buttons = pygame.mouse.get_pressed()
    return GREEN if mouse_buttons[0] else RED


# ────────────────────────── enemy ────────────────────────────────

def spawn_enemy() -> Dict:
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x, y = random.randint(0, SCREEN_WIDTH), -ENEMY_RADIUS * 2
    elif side == "bottom":
        x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + ENEMY_RADIUS * 2
    elif side == "left":
        x, y = -ENEMY_RADIUS * 2, random.randint(0, SCREEN_HEIGHT)
    else:
        x, y = SCREEN_WIDTH + ENEMY_RADIUS * 2, random.randint(0, SCREEN_HEIGHT)
    return {"pos": pygame.math.Vector2(x, y), "hp": ENEMY_MAX_HP}


def move_enemy_towards_player(enemy: Dict, player_rect: pygame.Rect, speed_mul: float = 1.0) -> None:
    ep = enemy["pos"]
    pc = pygame.math.Vector2(player_rect.centerx, player_rect.centery)
    d  = pc - ep
    if d.length_squared() > 0:
        ep += d.normalize() * ENEMY_SPEED * speed_mul


# ────────────────────────── projectiles ──────────────────────────

def shoot_projectile(projectiles: List[Dict], player_rect: pygame.Rect, mouse_pos: Tuple[int, int]) -> None:
    start  = pygame.math.Vector2(player_rect.centerx, player_rect.centery)
    target = pygame.math.Vector2(*mouse_pos)
    d = target - start
    if d.length_squared() == 0:
        return
    projectiles.append({"pos": start.copy(), "vel": d.normalize() * PROJECTILE_SPEED, "pierce_left": 0})


def update_projectiles(
    projectiles: List[Dict],
    enemies: List[Dict],
    exp_stars: List[Dict],
    state: Dict,
) -> int:
    now      = pygame.time.get_ticks()
    piercing = state.get("piercing_until", 0) > now
    lifesteal = state.get("lifesteal_until", 0) > now

    for proj in projectiles:
        proj["pos"] += proj["vel"]

    projectiles[:] = [
        p for p in projectiles
        if 0 <= p["pos"].x <= SCREEN_WIDTH and 0 <= p["pos"].y <= SCREEN_HEIGHT
    ]

    to_remove_proj   = set()
    to_remove_enemies = set()

    for i, proj in enumerate(projectiles):
        hits = 0
        max_hits = 3 if piercing else 1
        for j, enemy in enumerate(enemies):
            if j in to_remove_enemies:
                continue
            if (enemy["pos"] - proj["pos"]).length() <= ENEMY_RADIUS + PROJECTILE_RADIUS:
                enemy["hp"] -= 1
                if lifesteal:
                    state["player_hp_float"] = min(
                        state.get("player_hp_float", float(state["player_hp"])) + 0.05,
                        float(PLAYER_MAX_HP)
                    )
                    state["player_hp"] = int(state["player_hp_float"])
                if enemy["hp"] <= 0:
                    to_remove_enemies.add(j)
                    exp_stars.append({
                        "pos":  enemy["pos"].copy(),
                        "vel":  pygame.math.Vector2(random.uniform(-STAR_SPEED, STAR_SPEED),
                                                    random.uniform(-STAR_SPEED, STAR_SPEED)),
                        "born": now,
                    })
                hits += 1
                if hits >= max_hits:
                    to_remove_proj.add(i)
                    break

    projectiles[:] = [p for idx, p in enumerate(projectiles) if idx not in to_remove_proj]
    enemies[:]     = [e for idx, e in enumerate(enemies)     if idx not in to_remove_enemies]
    return len(to_remove_enemies)


# ────────────────────────── EXP stars ────────────────────────────

def update_exp_stars(exp_stars: List[Dict], player_rect: pygame.Rect, state: Dict) -> None:
    now = pygame.time.get_ticks()
    pc  = pygame.math.Vector2(player_rect.centerx, player_rect.centery)
    collected = []
    for star in exp_stars:
        if now - star["born"] > STAR_LIFETIME_MS:
            collected.append(star)
            continue
        dist = (pc - star["pos"]).length()
        if dist <= STAR_MAGNET_RANGE:
            d = pc - star["pos"]
            if d.length_squared() > 0:
                star["pos"] += d.normalize() * STAR_MAGNET_SPEED
        else:
            star["pos"] += star["vel"]

        if (pc - star["pos"]).length() <= PLAYER_SIZE // 2 + STAR_RADIUS:
            collected.append(star)
            state["exp"] += EXP_PER_KILL

    for s in collected:
        if s in exp_stars:
            exp_stars.remove(s)


def check_level_up(state: Dict) -> bool:
    needed = exp_needed(state["level"])
    if state["exp"] >= needed:
        state["exp"] -= needed
        state["level"] += 1
        return True
    return False


# ────────────────────────── shockwave ────────────────────────────

def trigger_shockwave(enemies: List[Dict], player_rect: pygame.Rect, state: Dict) -> None:
    now = pygame.time.get_ticks()
    if now - state.get("shockwave_last", -99999) < SHOCKWAVE_COOLDOWN_MS:
        return
    state["shockwave_last"] = now
    state["shockwave_anim"] = {"start": now}
    pc = pygame.math.Vector2(player_rect.centerx, player_rect.centery)
    to_remove = []
    for enemy in enemies:
        d    = enemy["pos"] - pc
        dist = d.length()
        if dist < SHOCKWAVE_RADIUS:
            if d.length_squared() > 0:
                enemy["pos"] += d.normalize() * SHOCKWAVE_PUSH_FORCE * (1 - dist / SHOCKWAVE_RADIUS)
            enemy["hp"] -= max(1, int(ENEMY_MAX_HP * SHOCKWAVE_DAMAGE_RATIO))
            if enemy["hp"] <= 0:
                to_remove.append(enemy)
    for e in to_remove:
        if e in enemies:
            enemies.remove(e)


# ────────────────────────── drone ────────────────────────────────

def update_drone(state: Dict, enemies: List[Dict], projectiles: List[Dict], player_rect: pygame.Rect) -> None:
    now = pygame.time.get_ticks()
    if state.get("drone_until", 0) <= now:
        return
    angle = (now / 1000.0) * 2.0
    state["drone_pos"] = pygame.math.Vector2(
        player_rect.centerx + math.cos(angle) * 60,
        player_rect.centery + math.sin(angle) * 60,
    )
    if now - state.get("drone_last_shot", 0) < DRONE_FIRE_RATE_MS or not enemies:
        return
    dp      = state["drone_pos"]
    nearest = min(enemies, key=lambda e: (e["pos"] - dp).length_squared())
    d       = nearest["pos"] - dp
    if d.length_squared() == 0:
        return
    projectiles.append({"pos": dp.copy(), "vel": d.normalize() * DRONE_PROJ_SPEED, "pierce_left": 0})
    state["drone_last_shot"] = now


# ────────────────────────── power-up overlay ─────────────────────

def draw_powerup_screen(screen: pygame.Surface, options: List[Dict], font_big, font_med, font_sm) -> int:
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 210))
    screen.blit(overlay, (0, 0))

    title = font_big.render("*  LEVEL UP!  *", True, GOLD)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 55))

    sub = font_med.render("Choose a Power-Up", True, (220, 220, 220))
    screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 118))

    card_w, card_h = 215, 240
    gap    = 18
    total_w = 3 * card_w + 2 * gap
    sx = (SCREEN_WIDTH - total_w) // 2
    sy = 160

    mx, my = pygame.mouse.get_pos()
    hovered = -1

    for i, opt in enumerate(options):
        cx   = sx + i * (card_w + gap)
        rect = pygame.Rect(cx, sy, card_w, card_h)
        hov  = rect.collidepoint(mx, my)
        if hov:
            hovered = i

        bg = (40, 40, 65) if hov else (22, 22, 42)
        pygame.draw.rect(screen, bg, rect, border_radius=14)
        pygame.draw.rect(screen, opt["color"], rect, 3 if hov else 2, border_radius=14)

        # Number badge
        num = font_big.render(str(i + 1), True, opt["color"])
        screen.blit(num, (cx + card_w // 2 - num.get_width() // 2, sy + 12))

        # Name (may wrap)
        name_surf = font_med.render(opt["name"], True, WHITE)
        if name_surf.get_width() > card_w - 10:
            words = opt["name"].split()
            mid   = len(words) // 2
            l1    = font_sm.render(" ".join(words[:mid]), True, WHITE)
            l2    = font_sm.render(" ".join(words[mid:]), True, WHITE)
            screen.blit(l1, (cx + card_w // 2 - l1.get_width() // 2, sy + 72))
            screen.blit(l2, (cx + card_w // 2 - l2.get_width() // 2, sy + 94))
            dy = sy + 122
        else:
            screen.blit(name_surf, (cx + card_w // 2 - name_surf.get_width() // 2, sy + 70))
            dy = sy + 108

        # Description word-wrap
        words, line, lines = opt["desc"].split(), [], []
        for w in words:
            test = font_sm.render(" ".join(line + [w]), True, WHITE)
            if test.get_width() > card_w - 18:
                if line: lines.append(" ".join(line))
                line = [w]
            else:
                line.append(w)
        if line: lines.append(" ".join(line))
        for li, ln in enumerate(lines[:5]):
            ls = font_sm.render(ln, True, (195, 195, 215))
            screen.blit(ls, (cx + 9, dy + li * 22))

    hint = font_sm.render("Click a card to select", True, (140, 140, 160))
    screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, sy + card_h + 18))
    return hovered


def apply_powerup(powerup_id: str, state: Dict) -> None:
    now = pygame.time.get_ticks()
    if powerup_id == "lifesteal":
        state["lifesteal_until"] = now + POWERUP_LIFESTEAL_DURATION
    elif powerup_id == "timedil":
        state["timedil_until"]   = now + POWERUP_TIMEDIL_DURATION
    elif powerup_id == "piercing":
        state["piercing_until"]  = now + POWERUP_PIERCING_DURATION
    elif powerup_id == "drone":
        state["drone_until"]     = now + POWERUP_DRONE_DURATION
        state["drone_pos"]       = pygame.math.Vector2(0, 0)
        state["drone_last_shot"] = 0
    elif powerup_id == "shockwave":
        state["has_shockwave"]   = True


# ────────────────────────── HUD ──────────────────────────────────

def draw_hud(screen, state: Dict, font, font_sm, ammo, reloading, score, high_score, now):
    screen.blit(font.render(f"HP: {state['player_hp']}", True, WHITE), (10, 10))
    ammo_str = f"Ammo: {ammo}/{MAX_AMMO}" + (" (reloading...)" if reloading else "")
    screen.blit(font.render(ammo_str, True, WHITE), (10, 40))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 70))
    screen.blit(font.render(f"High Score: {high_score}", True, WHITE), (10, 100))

    # Level label + EXP bar (top-right)
    lv = font.render(f"Level {state['level']}", True, GOLD)
    screen.blit(lv, (SCREEN_WIDTH - lv.get_width() - 10, 10))
    bar_w, bar_h = 160, 14
    bx, by = SCREEN_WIDTH - bar_w - 10, 40
    needed = exp_needed(state["level"])
    fill   = int(bar_w * min(state["exp"] / needed, 1.0))
    pygame.draw.rect(screen, (55, 55, 55), (bx, by, bar_w, bar_h), border_radius=6)
    if fill > 0:
        pygame.draw.rect(screen, GOLD, (bx, by, fill, bar_h), border_radius=6)
    pygame.draw.rect(screen, WHITE, (bx, by, bar_w, bar_h), 1, border_radius=6)
    el = font_sm.render(f"{state['exp']}/{needed} EXP", True, (220, 200, 90))
    screen.blit(el, (bx + bar_w // 2 - el.get_width() // 2, by))

    # Active buffs (bottom-right)
    icons = []
    if state.get("lifesteal_until", 0) > now:
        icons.append((f"Lifesteal {(state['lifesteal_until']-now)//1000+1}s", LIGHT_GREEN))
    if state.get("timedil_until", 0) > now:
        icons.append((f"Slow {(state['timedil_until']-now)//1000+1}s", PURPLE))
    if state.get("piercing_until", 0) > now:
        icons.append((f"Pierce {(state['piercing_until']-now)//1000+1}s", GOLD))
    if state.get("drone_until", 0) > now:
        icons.append((f"Drone {(state['drone_until']-now)//1000+1}s", ORANGE))
    if state.get("has_shockwave"):
        cd = max(0, SHOCKWAVE_COOLDOWN_MS - (now - state.get("shockwave_last", -99999)))
        label = "Shockwave [E]" if cd == 0 else f"Shockwave {cd//1000+1}s"
        icons.append((label, CYAN))
    for i, (label, color) in enumerate(icons):
        surf = font_sm.render(label, True, color)
        screen.blit(surf, (SCREEN_WIDTH - surf.get_width() - 10, SCREEN_HEIGHT - 30 - i * 24))


# ────────────────────────── game over ────────────────────────────

def draw_game_over_screen(
    screen: pygame.Surface,
    score: int,
    high_score: int,
    font_big: pygame.font.Font,
    font_med: pygame.font.Font,
    font_sm:  pygame.font.Font,
    now: int,
) -> pygame.Rect:
    """Draw the game-over overlay. Returns the Try Again button Rect."""

    # Dark translucent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 210))
    screen.blit(overlay, (0, 0))

    # "GAME OVER" – layered red glow
    title_font = pygame.font.Font(None, 102)
    for offset, alpha in [(7, 28), (5, 55), (3, 90)]:
        glow = title_font.render("GAME OVER", True, (180, 0, 0))
        glow.set_alpha(alpha)
        screen.blit(glow, (SCREEN_WIDTH // 2 - glow.get_width() // 2 + offset, 118 + offset))
    title_surf = title_font.render("GAME OVER", True, RED)
    screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 118))

    # Decorative triple-line divider
    for off, col, thick in [(0, (90, 15, 15), 1), (4, (210, 35, 35), 2), (8, (90, 15, 15), 1)]:
        pygame.draw.line(screen, col, (110, 232 + off), (SCREEN_WIDTH - 110, 232 + off), thick)

    # Score
    lbl = font_sm.render("Y O U R   S C O R E", True, (140, 140, 140))
    screen.blit(lbl, (SCREEN_WIDTH // 2 - lbl.get_width() // 2, 256))
    score_font = pygame.font.Font(None, 72)
    sv = score_font.render(str(score), True, WHITE)
    screen.blit(sv, (SCREEN_WIDTH // 2 - sv.get_width() // 2, 278))

    # High-score line – pulses gold on new record
    is_new = score > 0 and score >= high_score
    hs_text  = "*  NEW HIGH SCORE!  *" if is_new else f"High Score:  {high_score}"
    hs_color = GOLD if is_new else (150, 150, 150)
    hs_surf  = font_med.render(hs_text, True, hs_color)
    if is_new:
        hs_surf.set_alpha(int(200 + 55 * math.sin(now * 0.005)))
    screen.blit(hs_surf, (SCREEN_WIDTH // 2 - hs_surf.get_width() // 2, 350))

    # ── Try Again button ─────────────────────────────────────────
    btn_w, btn_h = 230, 56
    btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - btn_w // 2, 412, btn_w, btn_h)
    hovered  = btn_rect.collidepoint(pygame.mouse.get_pos())

    if hovered:
        glow_s = pygame.Surface((btn_w + 24, btn_h + 24), pygame.SRCALPHA)
        pygame.draw.rect(glow_s, (255, 0, 0, 55), glow_s.get_rect(), border_radius=32)
        screen.blit(glow_s, (btn_rect.x - 12, btn_rect.y - 12))

    pygame.draw.rect(screen, (210, 35, 35) if hovered else (145, 18, 18), btn_rect, border_radius=13)
    pygame.draw.rect(screen, (255, 80, 80) if hovered else (210, 50, 50), btn_rect, 2, border_radius=13)

    bl = font_med.render("TRY AGAIN", True, WHITE)
    screen.blit(bl, (btn_rect.centerx - bl.get_width() // 2, btn_rect.centery - bl.get_height() // 2))

    # Quit hint
    qh = font_sm.render("press  Q  to quit", True, (80, 80, 80))
    screen.blit(qh, (SCREEN_WIDTH // 2 - qh.get_width() // 2, 486))

    return btn_rect


def _fresh_state() -> Dict:
    return {
        "player_hp":       PLAYER_MAX_HP,
        "player_hp_float": float(PLAYER_MAX_HP),
        "level":           1,
        "exp":             0,
        "has_shockwave":   False,
        "shockwave_last":  -99999,
    }


# ────────────────────────── main ─────────────────────────────────

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cozy Game")
    clock = pygame.time.Clock()

    font_big = pygame.font.Font(None, 52)
    font     = pygame.font.Font(None, 30)
    font_sm  = pygame.font.Font(None, 22)

    player = pygame.Rect(
        (SCREEN_WIDTH - PLAYER_SIZE) // 2,
        (SCREEN_HEIGHT - PLAYER_SIZE) // 2,
        PLAYER_SIZE, PLAYER_SIZE,
    )

    state: Dict = _fresh_state()

    enemies:     List[Dict] = []
    projectiles: List[Dict] = []
    exp_stars:   List[Dict] = []

    next_spawn_time   = pygame.time.get_ticks() + random.randint(ENEMY_SPAWN_MIN_MS, ENEMY_SPAWN_MAX_MS)
    last_shot_time    = 0
    ammo              = MAX_AMMO
    reloading         = False
    reload_start_time = 0
    score             = 0
    high_score        = 0

    choosing_powerup = False
    powerup_options: List[Dict] = []
    game_over        = False

    _go_btn_rect: Optional[pygame.Rect] = None
    dash_trail: List[Dict] = []  # for afterimage particles
    running = True
    while running:
        dt  = clock.get_time() / 1000.0   # seconds since last frame
        now = pygame.time.get_ticks()

        # ── Events ──────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Game-over input
            if game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if _go_btn_rect and _go_btn_rect.collidepoint(event.pos):
                        # Full reset
                        state            = _fresh_state()
                        reset_dash_state()
                        dash_trail.clear()
                        enemies.clear(); projectiles.clear(); exp_stars.clear()
                        ammo             = MAX_AMMO
                        reloading        = False
                        reload_start_time = last_shot_time = 0
                        score            = 0
                        choosing_powerup = False
                        game_over        = False
                        player.center    = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                        next_spawn_time  = pygame.time.get_ticks() + random.randint(
                            ENEMY_SPAWN_MIN_MS, ENEMY_SPAWN_MAX_MS)
                continue  # skip rest of event loop while on game-over screen

            # Dash trigger — only fires once on key-down press, not while held
            if not game_over and not choosing_powerup:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                    try_trigger_dash()

            if choosing_powerup and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my   = pygame.mouse.get_pos()
                card_w, card_h = 215, 240
                gap      = 18
                total_w  = 3 * card_w + 2 * gap
                sx       = (SCREEN_WIDTH - total_w) // 2
                for i in range(3):
                    cx = sx + i * (card_w + gap)
                    if pygame.Rect(cx, 160, card_w, card_h).collidepoint(mx, my):
                        apply_powerup(powerup_options[i]["id"], state)
                        choosing_powerup = False
                        break

            if not choosing_powerup and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and state.get("has_shockwave"):
                    trigger_shockwave(enemies, player, state)

        if choosing_powerup:
            draw_powerup_screen(screen, powerup_options, font_big, font, font_sm)
            pygame.display.flip()
            clock.tick(60)
            continue

        # Game-over screen
        if game_over:
            screen.fill(BLACK)
            _go_btn_rect = draw_game_over_screen(screen, score, high_score, font_big, font, font_sm, now)
            pygame.display.flip()
            clock.tick(60)
            continue

        # ── Game logic ──────────────────────────────────────────
        keys = pygame.key.get_pressed()
        handle_movement(player, keys, dt)
        player.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Spawn afterimage trail particles while dashing
        if _dash_state["active"]:
            dash_trail.append({
                "pos":   pygame.Vector2(player.centerx, player.centery),
                "born":  now,
                "size":  PLAYER_SIZE,
            })
        # Expire old trail particles (lifetime 120 ms)
        dash_trail[:] = [p for p in dash_trail if now - p["born"] < 120]

        if reloading and now - reload_start_time >= RELOAD_TIME_MS:
            ammo, reloading = MAX_AMMO, False

        mb = pygame.mouse.get_pressed()
        if mb[0] and now - last_shot_time >= PROJECTILE_COOLDOWN_MS and not reloading and ammo > 0:
            shoot_projectile(projectiles, player, pygame.mouse.get_pos())
            last_shot_time = now
            ammo -= 1
            if ammo == 0:
                reloading, reload_start_time = True, now

        if now >= next_spawn_time:
            enemies.append(spawn_enemy())
            next_spawn_time = now + random.randint(ENEMY_SPAWN_MIN_MS, ENEMY_SPAWN_MAX_MS)

        speed_mul = 0.6 if state.get("timedil_until", 0) > now else 1.0
        for enemy in enemies:
            move_enemy_towards_player(enemy, player, speed_mul)

        update_drone(state, enemies, projectiles, player)
        kills = update_projectiles(projectiles, enemies, exp_stars, state)
        if kills:
            score += kills * 50
            high_score = max(score, high_score)

        update_exp_stars(exp_stars, player, state)
        if check_level_up(state):
            choosing_powerup = True
            powerup_options  = pick_3_powerups()

        pc = pygame.math.Vector2(player.centerx, player.centery)
        for enemy in list(enemies):
            if (enemy["pos"] - pc).length() <= ENEMY_RADIUS + PLAYER_SIZE / 2:
                state["player_hp"] -= 1
                state["player_hp_float"] = float(state["player_hp"])
                enemies.remove(enemy)
                if state["player_hp"] <= 0:
                    game_over = True
                break
                
        # ── Draw ────────────────────────────────────────────────
        screen.fill(BLACK)

        # Dash afterimage trail
        for tp in dash_trail:
            age_frac = (now - tp["born"]) / 120.0
            alpha    = int(180 * (1.0 - age_frac))
            size     = int(tp["size"] * (0.9 - 0.3 * age_frac))
            trail_s  = pygame.Surface((size, size), pygame.SRCALPHA)
            trail_s.fill((100, 200, 255, alpha))
            screen.blit(trail_s, (int(tp["pos"].x) - size // 2, int(tp["pos"].y) - size // 2))

        pygame.draw.rect(screen, get_player_color(state), player)

        for enemy in enemies:
            ep = enemy["pos"]
            pygame.draw.circle(screen, BLUE, (int(ep.x), int(ep.y)), ENEMY_RADIUS)
            # HP bar
            hp_frac = enemy["hp"] / ENEMY_MAX_HP
            bw = ENEMY_RADIUS * 2
            bx, by = int(ep.x) - ENEMY_RADIUS, int(ep.y) - ENEMY_RADIUS - 8
            pygame.draw.rect(screen, (80, 0, 0), (bx, by, bw, 4))
            pygame.draw.rect(screen, RED,        (bx, by, int(bw * hp_frac), 4))

        for proj in projectiles:
            pp = proj["pos"]
            pygame.draw.circle(screen, WHITE, (int(pp.x), int(pp.y)), PROJECTILE_RADIUS)

        # EXP stars
        for star in exp_stars:
            sp = star["pos"]
            cx, cy = int(sp.x), int(sp.y)
            age_frac = min(1.0, (now - star["born"]) / STAR_LIFETIME_MS)
            col = (int(255 * (1 - age_frac * 0.6)), int(180 * (1 - age_frac * 0.6)), 0)
            pts = []
            for k in range(5):
                oa = math.radians(-90 + k * 72)
                ia = math.radians(-90 + k * 72 + 36)
                pts.append((cx + STAR_RADIUS * math.cos(oa), cy + STAR_RADIUS * math.sin(oa)))
                pts.append((cx + STAR_RADIUS * 0.45 * math.cos(ia), cy + STAR_RADIUS * 0.45 * math.sin(ia)))
            pygame.draw.polygon(screen, col, pts)
            pygame.draw.polygon(screen, GOLD, pts, 1)

        # Drone
        if state.get("drone_until", 0) > now and "drone_pos" in state:
            dp = state["drone_pos"]
            pygame.draw.circle(screen, ORANGE, (int(dp.x), int(dp.y)), 10)
            pygame.draw.circle(screen, WHITE,  (int(dp.x), int(dp.y)), 10, 2)

        # Shockwave animation
        sa = state.get("shockwave_anim")
        if sa:
            elapsed = now - sa["start"]
            dur     = 400
            if elapsed < dur:
                radius = SHOCKWAVE_RADIUS * elapsed / dur
                alpha  = 200 * (1 - elapsed / dur)
                surf   = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*CYAN, alpha), (player.centerx, player.centery), radius, 3)
                screen.blit(surf, (0, 0))
            else:
                state["shockwave_anim"] = None

        draw_hud(screen, state, font, font_sm, ammo, reloading, score, high_score, now)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()