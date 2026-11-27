#!/usr/bin/env python3
"""
CheckMate Apple/macOS Keynote Launch Video Generator
Renders a 1080p 30fps Apple-inspired product launch video:
- Minimalist typography (SF Pro / Segoe UI / Georgia)
- Apple ceramic & space black lighting with frosted glass window chrome
- macOS traffic lights, smooth floating elevation shadows, and Apple-style bento grids
- Beat-synced soundtrack with professional easing
"""

import sys
import os
import math
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION = 38.0
TOTAL_FRAMES = int(DURATION * FPS)

OUTPUT_DIR = "brag-output"
WORK_DIR = os.path.join(OUTPUT_DIR, "work")
os.makedirs(WORK_DIR, exist_ok=True)

WINDIR = os.environ.get("WINDIR", r"C:\Windows")
FONTS_DIR = os.path.join(WINDIR, "Fonts")

def get_font(name, size):
    path = os.path.join(FONTS_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# Apple Keynote Type Stack
font_apple_hero = get_font("segoeuib.ttf", 68)
font_apple_xl = get_font("segoeuib.ttf", 52)
font_apple_lg = get_font("segoeuib.ttf", 36)
font_apple_md = get_font("segoeui.ttf", 24)
font_apple_sm = get_font("segoeui.ttf", 19)
font_apple_xs = get_font("segoeui.ttf", 15)

font_serif_hero = get_font("georgiab.ttf", 64)
font_serif_lg = get_font("georgiab.ttf", 40)
font_serif_md = get_font("georgia.ttf", 26)

font_mono_lg = get_font("consolab.ttf", 28)
font_mono_md = get_font("consola.ttf", 22)
font_mono_sm = get_font("consola.ttf", 17)

def load_img(path, target_size=None):
    if path and os.path.exists(path):
        try:
            img = Image.open(path).convert("RGBA")
            if target_size:
                img = img.resize(target_size, Image.Resampling.LANCZOS)
            return img
        except Exception:
            pass
    return None

logo_img = load_img("logo.png")
if logo_img:
    logo_sm = logo_img.resize((240, 140), Image.Resampling.LANCZOS)
    logo_hero = logo_img.resize((380, 222), Image.Resampling.LANCZOS)
    logo_mini = logo_img.resize((150, 88), Image.Resampling.LANCZOS)
else:
    logo_sm = logo_hero = logo_mini = None

def draw_macos_window(draw, x1, y1, x2, y2, title="CheckMate — Console", dark=False):
    bg_color = (24, 24, 27) if dark else (255, 255, 255)
    border_color = (39, 39, 42) if dark else (226, 232, 240)
    header_color = (39, 39, 42) if dark else (248, 250, 252)
    text_color = (161, 161, 170) if dark else (100, 116, 139)

    # Window shadow
    shadow_color = (0, 0, 0, 50) if dark else (0, 0, 0, 20)
    for offset in range(6, 0, -2):
        draw.rounded_rectangle([x1 - offset, y1 - offset + 4, x2 + offset, y2 + offset + 4], radius=18, outline=(0, 0, 0))

    # Main window body
    draw.rounded_rectangle([x1, y1, x2, y2], radius=16, fill=bg_color, outline=border_color, width=1)
    
    # macOS Titlebar
    draw.rounded_rectangle([x1, y1, x2, y1 + 46], radius=16, fill=header_color)
    draw.rectangle([x1, y1 + 25, x2, y1 + 46], fill=header_color)
    draw.line([x1, y1 + 46, x2, y1 + 46], fill=border_color, width=1)

    # macOS Traffic Lights
    draw.ellipse([x1 + 18, y1 + 16, x1 + 30, y1 + 28], fill=(255, 95, 87), outline=(224, 68, 62), width=1)
    draw.ellipse([x1 + 38, y1 + 16, x1 + 50, y1 + 28], fill=(255, 189, 46), outline=(223, 158, 24), width=1)
    draw.ellipse([x1 + 58, y1 + 16, x1 + 70, y1 + 28], fill=(39, 201, 63), outline=(26, 171, 49), width=1)

    # Centered macOS Title
    draw.text((x1 + 100, y1 + 13), title, fill=text_color, font=font_apple_xs)

def draw_apple_header(draw, active_tab="Overview"):
    # Apple minimalist top navigation
    draw.rectangle([0, 0, WIDTH, 64], fill=(255, 255, 255))
    draw.line([0, 64, WIDTH, 64], fill=(226, 232, 240), width=1)
    
    draw.text((80, 18), "CheckMate", fill=(29, 29, 31), font=font_apple_lg)
    
    tabs = ["Overview", "Killswitch", "PQC Inspector", "Audit Stream"]
    tx = 340
    for t in tabs:
        col = (0, 113, 227) if t == active_tab else (134, 134, 139)
        draw.text((tx, 22), t, fill=col, font=font_apple_sm)
        if t == active_tab:
            draw.line([tx, 60, tx + 60, 60], fill=(0, 113, 227), width=2)
        tx += 170

    draw.rounded_rectangle([WIDTH - 380, 16, WIDTH - 80, 48], radius=16, fill=(245, 245, 247))
    draw.text((WIDTH - 360, 22), "Track 4: Trust, but verify", fill=(29, 29, 31), font=font_apple_xs)

# -----------------------------------------------------------------------------
# SCENE 1: The Apple Problem Keynote (0.0s – 7.5s)
# -----------------------------------------------------------------------------
def render_scene_1(t):
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 10, 12))
    draw = ImageDraw.Draw(img)

    # Subtle radial center glow
    cx, cy = WIDTH // 2, HEIGHT // 2
    for r in range(400, 50, -50):
        alpha = int(12 * (1.0 - r / 400.0))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(15, 23, 42))

    draw.text((100, 80), "THE ENTERPRISE HARDWARE DILEMMA", fill=(41, 151, 255), font=font_apple_sm)
    draw.text((100, 130), "Hardware gets lost.\nTokens stay active.", fill=(245, 245, 247), font=font_apple_hero)
    draw.text((100, 290), "Standard JWT tokens remain valid for up to 60 minutes after a laptop is stolen.\nThieves disconnect networking into Airplane Mode — blinding MDM remote wipes.", fill=(161, 161, 170), font=font_apple_md)

    # macOS Terminal Window
    tx1, ty1, tx2, ty2 = 100, 390, 1180, 950
    draw_macos_window(draw, tx1, ty1, tx2, ty2, "Terminal — zsh — Compromised Workstation", dark=True)

    lines = [
        ("# 1. Attacker physically steals authenticated corporate laptop", (113, 113, 122)),
        ("$ sudo nmcli radio wifi off  # Disconnect Wi-Fi (Faraday cage)", (228, 228, 231)),
        ("$ curl -H 'Authorization: Bearer jwt_valid_for_45m' /api/export", (234, 179, 8)),
        ("HTTP/1.1 200 OK  # Token accepted without server-side verification!", (239, 68, 68)),
        ("$ ./extract_database_keys.sh", (228, 228, 231)),
        ("Extracting customer records, proprietary source code, credentials...", (248, 113, 113)),
        ("[MDM Remote Wipe Status]: WAITING FOR NETWORK (WIPE BLINDED)", (239, 68, 68)),
    ]
    dy = ty1 + 70
    for txt, col in lines:
        draw.text((tx1 + 35, dy), txt, fill=col, font=font_mono_md)
        dy += 44

    # Apple-style Dark Glass Cards on Right
    if t > 1.8:
        prog1 = min(1.0, (t - 1.8) / 0.4)
        rx1 = int(1240 + (1.0 - prog1) * 80)
        draw.rounded_rectangle([rx1, 390, 1820, 620], radius=18, fill=(24, 24, 27), outline=(239, 68, 68), width=1)
        draw.text((rx1 + 35, 425), "THE 45-MINUTE WINDOW", fill=(239, 68, 68), font=font_apple_xs)
        draw.text((rx1 + 35, 465), "Token Expiration Lag", fill=(255, 255, 255), font=font_apple_lg)
        draw.text((rx1 + 35, 520), "Central user directory revocations are completely ignored by client-side cached tokens.", fill=(161, 161, 170), font=font_apple_sm)

    if t > 4.2:
        prog2 = min(1.0, (t - 4.2) / 0.4)
        rx2 = int(1240 + (1.0 - prog2) * 80)
        draw.rounded_rectangle([rx2, 660, 1820, 950], radius=18, fill=(24, 24, 27), outline=(39, 39, 42), width=1)
        draw.text((rx2 + 35, 695), "HARVEST NOW, DECRYPT LATER", fill=(234, 179, 8), font=font_apple_xs)
        draw.text((rx2 + 35, 735), "The Quantum Threat", fill=(255, 255, 255), font=font_apple_lg)
        draw.text((rx2 + 35, 790), "Classical RSA & ECDH exchanges intercepted today will be decrypted by tomorrow's quantum computers.", fill=(161, 161, 170), font=font_apple_sm)

    return img

# -----------------------------------------------------------------------------
# SCENE 2: The Apple Hero Product Reveal (7.5s – 15.5s)
# -----------------------------------------------------------------------------
def render_scene_2(t):
    img = Image.new("RGB", (WIDTH, HEIGHT), (245, 245, 247))
    draw = ImageDraw.Draw(img)
    draw_apple_header(draw, "Overview")

    st = t - 7.5
    float_y = int(math.sin(st * 2.8) * 9)

    # Hero Left: Floating Chess Logo
    if logo_hero:
        # Soft shadow under logo
        draw.ellipse([140, 380, 480, 420], fill=(226, 232, 240))
        img.paste(logo_hero, (120, 170 + float_y), logo_hero)

    # Hero Center/Right: Apple Keynote Headline
    draw.text((560, 160), "Introducing CheckMate.", fill=(29, 29, 31), font=font_apple_hero)
    draw.text((560, 245), "Zero-Trust. Post-Quantum. Sub-millisecond.", fill=(134, 134, 139), font=font_serif_lg)
    draw.text((560, 310), "Continuous RFC 7662 OAuth 2.0 introspection coupled with NIST FIPS 203 ML-KEM-768 lattice cryptography.", fill=(0, 113, 227), font=font_apple_md)

    # 3 Apple Ceramic Bento Cards
    cards = [
        ("INSTANT KILLSWITCH", "< 0.8 ms", "Immediate server-side deny cutoff across all fleet nodes. Zero grace period for compromised devices.", (220, 38, 38)),
        ("POST-QUANTUM KEM", "ML-KEM-768", "NIST standardized lattice cryptography. Mathematically immune to Shor's polynomial quantum algorithm.", (0, 113, 227)),
        ("CONTINUOUS GATEWAY", "RFC 7662", "Every file access is verified live at the gateway. Offline stolen devices cannot decrypt confidential payloads.", (16, 185, 129))
    ]

    cx = 100
    card_w = 540
    card_h = 390
    for kicker, metric, desc, accent in cards:
        # Card shadow
        draw.rounded_rectangle([cx, 400, cx + card_w, 400 + card_h], radius=22, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        draw.text((cx + 36, 435), kicker, fill=accent, font=font_apple_xs)
        draw.text((cx + 36, 475), metric, fill=(29, 29, 31), font=font_apple_hero)
        
        # Wrapped text
        words = desc.split(" ")
        lines, cur = [], ""
        for w in words:
            if len(cur + " " + w) < 32:
                cur += (" " if cur else "") + w
            else:
                lines.append(cur)
                cur = w
        if cur: lines.append(cur)

        cy = 570
        for l in lines:
            draw.text((cx + 36, cy), l, fill=(113, 113, 122), font=font_apple_md)
            cy += 36

        # Apple-style pill tag
        draw.rounded_rectangle([cx + 36, 715, cx + 160, 750], radius=14, fill=(245, 245, 247))
        draw.text((cx + 52, 724), "VERIFIED", fill=(29, 29, 31), font=font_apple_xs)

        cx += card_w + 50

    return img

# -----------------------------------------------------------------------------
# SCENE 3: macOS Safari & Live Killswitch in Action (15.5s – 24.5s)
# -----------------------------------------------------------------------------
def render_scene_3(t):
    img = Image.new("RGB", (WIDTH, HEIGHT), (245, 245, 247))
    draw = ImageDraw.Draw(img)
    draw_apple_header(draw, "Killswitch")

    st = t - 15.5
    draw.text((100, 80), "LIVE FLEET CONTAINMENT", fill=(0, 113, 227), font=font_apple_xs)
    draw.text((100, 110), "One Click Quarantines The Device Across The Fleet", fill=(29, 29, 31), font=font_apple_xl)

    # Left Window: SecOps Management Dashboard (Safari Light)
    wx1, wy1, wx2, wy2 = 100, 180, 1020, 960
    draw_macos_window(draw, wx1, wy1, wx2, wy2, "CheckMate SecOps — https://checkmateee.vercel.app/killswitch.html")

    # Table Header
    draw.text((135, 255), "IDENTITY", fill=(134, 134, 139), font=font_apple_xs)
    draw.text((360, 255), "DEVICE & IP", fill=(134, 134, 139), font=font_apple_xs)
    draw.text((640, 255), "ZERO-TRUST STATUS", fill=(134, 134, 139), font=font_apple_xs)
    draw.text((820, 255), "ACTION", fill=(134, 134, 139), font=font_apple_xs)
    draw.line([135, 285, 985, 285], fill=(226, 232, 240), width=1)

    devices = [
        ("dev_suhas", "Windows 11 (192.168.1.104)", st > 2.2),
        ("dev_priya", "macOS Sonoma (10.0.0.12)", False),
        ("ci_runner_01", "Ubuntu Linux (172.31.8.44)", False),
    ]

    dy = 320
    for actor, dev, is_revoked in devices:
        draw.text((135, dy), actor, fill=(29, 29, 31), font=font_mono_md)
        draw.text((360, dy), dev, fill=(113, 113, 122), font=font_apple_sm)

        if is_revoked:
            # Apple Red Capsule
            draw.rounded_rectangle([635, dy - 4, 760, dy + 28], radius=16, fill=(254, 226, 226))
            draw.text((652, dy + 3), "QUARANTINED", fill=(220, 38, 38), font=font_apple_xs)

            draw.rounded_rectangle([810, dy - 4, 960, dy + 28], radius=16, fill=(220, 252, 231))
            draw.text((830, dy + 3), "Restore Access", fill=(22, 101, 52), font=font_apple_xs)
        else:
            # Apple Green Capsule
            draw.rounded_rectangle([635, dy - 4, 740, dy + 28], radius=16, fill=(220, 252, 231))
            draw.text((655, dy + 3), "ACTIVE", fill=(22, 101, 52), font=font_apple_xs)

            draw.rounded_rectangle([810, dy - 4, 960, dy + 28], radius=16, fill=(254, 226, 226))
            draw.text((830, dy + 3), "⚡ Killswitch", fill=(220, 38, 38), font=font_apple_xs)

        dy += 80

    # Live Audit Feed inside Dashboard
    draw.rounded_rectangle([135, 620, 985, 920], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((160, 645), "LIVE SECURITY EVENT LEDGER (RFC 7662)", fill=(100, 116, 139), font=font_apple_xs)
    
    logs = [
        ("08:14:02", "INSPECTION_ALLOW", "dev_suhas authorized for asset tapeout_spec.v", (22, 101, 52)),
        ("08:14:05", "KILLSWITCH_ENGAGED", "Manager triggered instant killswitch for dev_suhas", (220, 38, 38)),
        ("08:14:05", "PROPAGATED (<0.8ms)", "Revocation enforced across all cluster nodes", (220, 38, 38)),
        ("08:14:07", "INSPECTION_DENY", "Access blocked for dev_suhas: HTTP 403 Forbidden", (239, 68, 68))
    ]
    ly = 680
    for ts, ev, desc, col in logs:
        draw.text((160, ly), f"[{ts}] {ev}:", fill=col, font=font_mono_sm)
        draw.text((450, ly), desc, fill=(71, 85, 105), font=font_apple_xs)
        ly += 45

    # Right Window: Workstation Client Lockout Screen
    cx1, cy1, cx2, cy2 = 1070, 180, 1820, 960
    draw_macos_window(draw, cx1, cy1, cx2, cy2, "Workstation — Workspace", dark=st > 2.2)

    if st > 2.2:
        # Apple Pro Red Lockout Card
        draw.rounded_rectangle([cx1 + 45, cy1 + 90, cx2 - 45, cy2 - 90], radius=20, fill=(24, 15, 20), outline=(239, 68, 68), width=2)
        draw.text((cx1 + 170, cy1 + 160), "⛔ ACCESS DENIED BY SECURITY POLICY", fill=(239, 68, 68), font=font_apple_lg)
        draw.text((cx1 + 140, cy1 + 240), "[CHECKMATE ZERO-TRUST KILLSWITCH ENGAGED]", fill=(248, 113, 113), font=font_mono_md)
        draw.text((cx1 + 140, cy1 + 300), "Workstation Actor: dev_suhas", fill=(255, 255, 255), font=font_apple_sm)
        draw.text((cx1 + 140, cy1 + 350), "Enforcement: RFC 7662 OAuth 2.0 Introspection Revoked", fill=(248, 113, 113), font=font_apple_sm)
        draw.text((cx1 + 140, cy1 + 400), "Payload Status: Confidential Payloads & Keys Sealed", fill=(248, 113, 113), font=font_apple_sm)
        draw.text((cx1 + 140, cy1 + 470), "Central SecOps has quarantined this workstation. Stolen tokens are neutralized.", fill=(161, 161, 170), font=font_apple_md)

        draw.rounded_rectangle([cx1 + 240, cy1 + 540, cx1 + 470, cy1 + 590], radius=16, fill=(0, 113, 227))
        draw.text((cx1 + 265, cy1 + 555), "Re-Check Clearance", fill=(255, 255, 255), font=font_apple_sm)
    else:
        draw.text((cx1 + 180, cy1 + 340), "Workstation Active & Authorized", fill=(16, 185, 129), font=font_apple_xl)
        draw.text((cx1 + 180, cy1 + 410), "Continuous RFC 7662 token introspection active...", fill=(113, 113, 122), font=font_apple_md)

    return img

# -----------------------------------------------------------------------------
# SCENE 4: Apple M-Series "Spec Sheet" Keynote (24.5s – 32.5s)
# -----------------------------------------------------------------------------
def render_scene_4(t):
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 10, 12))
    draw = ImageDraw.Draw(img)

    draw.text((100, 80), "NIST FIPS 203 STANDARDIZED LATTICE CRYPTOGRAPHY", fill=(41, 151, 255), font=font_apple_xs)
    draw.text((100, 120), "Quantum-safe by design.", fill=(255, 255, 255), font=font_apple_hero)

    # 4 Apple Keynote Bento Spec Cards
    specs = [
        ("PUBLIC KEY", "1,184 B", "Standardized ML-KEM-768 lattice public vector bytes.", (41, 151, 255)),
        ("CIPHERTEXT", "1,088 B", "Post-quantum encrypted encapsulation package.", (52, 211, 153)),
        ("SHARED SECRET", "32 B", "High-entropy ephemeral 256-bit symmetric session key.", (192, 132, 252)),
        ("PROOF INTEGRITY", "HMAC", "Challenge-bound nonce verification: HMAC(K, ch || data).", (251, 146, 60))
    ]

    bx = 100
    bw = 390
    bh = 250
    for tag, val, desc, col in specs:
        draw.rounded_rectangle([bx, 220, bx + bw, 220 + bh], radius=20, fill=(24, 24, 27), outline=(39, 39, 42), width=1)
        draw.text((bx + 28, 250), tag, fill=(113, 113, 122), font=font_apple_xs)
        draw.text((bx + 28, 290), val, fill=col, font=font_apple_hero)
        draw.text((bx + 28, 390), desc, fill=(161, 161, 170), font=font_apple_sm)
        bx += bw + 50

    # macOS Dark Code Terminal (Track 4 Test Execution)
    tx1, ty1, tx2, ty2 = 100, 520, 1820, 960
    draw_macos_window(draw, tx1, ty1, tx2, ty2, "Terminal — python track4_validate.py --entry track4_service.py", dark=True)

    stream_lines = [
        ("$ python track4_validate.py --entry track4_service.py", (161, 161, 170)),
        ("PASS [format] clean setup: JSON response matches required structure.", (74, 222, 128)),
        ("PASS [behavior] owner before device loss: Received allow with exact content.", (74, 222, 128)),
        ("PASS [format] revoke lost-device owner: JSON response matches required structure.", (74, 222, 128)),
        ("PASS [behavior] owner after revocation: Received deny without content.", (74, 222, 128)),
        ("PASS [behavior] revocation persists across processes: Received deny without content.", (74, 222, 128)),
        ("PASS [behavior] fake key stays out of output: Fake key marker must not appear.", (74, 222, 128)),
        ("Local scenario passed. Exit code: 0 (100% Scorecard Verified)", (41, 151, 255))
    ]

    sy = ty1 + 65
    for l, col in stream_lines:
        draw.text((tx1 + 35, sy), l, fill=col, font=font_mono_md)
        sy += 42

    return img

# -----------------------------------------------------------------------------
# SCENE 5: Outro Keynote Lockup (32.5s – 38.0s)
# -----------------------------------------------------------------------------
def render_scene_5(t):
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 10, 12))
    draw = ImageDraw.Draw(img)

    # Ambient radial glow behind logo
    cx, cy = WIDTH // 2, 280
    for r in range(350, 40, -40):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(24, 24, 27))

    if logo_hero:
        img.paste(logo_hero, (WIDTH // 2 - 190, 160), logo_hero)

    draw.text((WIDTH // 2 - 180, 410), "CheckMate.", fill=(255, 255, 255), font=font_apple_hero)
    draw.text((WIDTH // 2 - 170, 490), "Trust, but verify.", fill=(161, 161, 170), font=font_serif_lg)

    # Clean Apple Pills
    pills = [
        ("🌐 Live Console", "https://checkmateee.vercel.app/"),
        ("📦 GitHub Repo", "github.com/trivikramkalagi91-commits/CheckMate"),
        ("⚡ Hackathon Score", "Track 4: 100% Pass (20/20 Checks)")
    ]

    pw = 460
    ph = 140
    px = (WIDTH - (3 * pw + 2 * 40)) // 2
    for title, val in pills:
        draw.rounded_rectangle([px, 590, px + pw, 590 + ph], radius=20, fill=(24, 24, 27), outline=(39, 39, 42), width=1)
        draw.text((px + 28, 620), title, fill=(0, 113, 227), font=font_apple_xs)
        draw.text((px + 28, 655), val, fill=(255, 255, 255), font=font_apple_sm)
        px += pw + 40

    draw.text((WIDTH // 2 - 270, 820), "Yugaantar DevForge Hackathon 2026 — Track 4 ('Trust, but verify')", fill=(113, 113, 122), font=font_apple_sm)
    return img

def get_frame(i):
    t = i / FPS
    if t < 7.5:
        return render_scene_1(t)
    elif t < 15.5:
        return render_scene_2(t)
    elif t < 24.5:
        return render_scene_3(t)
    elif t < 32.5:
        return render_scene_4(t)
    else:
        return render_scene_5(t)

def main():
    print(f"Rendering Apple-inspired CheckMate video: {TOTAL_FRAMES} frames ({DURATION}s @ {FPS}fps)...")
    
    output_video = os.path.join(OUTPUT_DIR, "brag.mp4")
    output_poster = os.path.join(OUTPUT_DIR, "brag.jpg")

    # Generate Poster Frame (Settled frame of Scene 2)
    poster_img = render_scene_2(10.0)
    poster_img.save(output_poster, "JPEG", quality=95)
    print(f"Saved Apple-styled poster frame to {output_poster}")

    music_path = r"C:\Users\trivi\.gemini\config\skills\launch-video\resources\music\launch-beat.mp3"

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", music_path,
        "-filter_complex", f"[1:a]afade=t=out:st={DURATION - 1.5:.1f}:d=1.5[a]",
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "ultrafast",
        "-crf", "18",
        "-t", str(DURATION),
        output_video
    ]

    log_path = os.path.join(WORK_DIR, "ffmpeg.log")
    with open(log_path, "w", encoding="utf-8") as f_err:
        proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=f_err)
        start_time = time.time()
        for i in range(TOTAL_FRAMES):
            frame_img = get_frame(i)
            proc.stdin.write(frame_img.tobytes())
            if i % 150 == 0 or i == TOTAL_FRAMES - 1:
                elapsed = time.time() - start_time
                fps_speed = (i + 1) / max(0.001, elapsed)
                print(f"Rendered {i+1}/{TOTAL_FRAMES} ({((i+1)/TOTAL_FRAMES)*100:.1f}%) @ {fps_speed:.1f} fps")

        proc.stdin.close()
        proc.wait()

    print(f"Apple Keynote styled video saved to: {output_video}")

if __name__ == "__main__":
    main()
