#!/usr/bin/env python3
"""
CheckMate Official Launch & Demo Video Generator (Antigravity Skill)
Renders high-production 1080p 30fps launch video with animated typography,
SecOps console mockups, PQC ML-KEM-768 crypto visualizations, and beat-synced audio.
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

font_serif_xl = get_font("georgiab.ttf", 60)
font_serif_lg = get_font("georgiab.ttf", 44)
font_serif_md = get_font("georgia.ttf", 30)

font_sans_xl = get_font("segoeuib.ttf", 50)
font_sans_lg = get_font("segoeuib.ttf", 34)
font_sans_md = get_font("segoeui.ttf", 25)
font_sans_sm = get_font("segoeui.ttf", 19)

font_mono_lg = get_font("consolab.ttf", 30)
font_mono_md = get_font("consola.ttf", 23)
font_mono_sm = get_font("consola.ttf", 18)

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
    logo_sm = logo_img.resize((260, 152), Image.Resampling.LANCZOS)
    logo_hero = logo_img.resize((360, 211), Image.Resampling.LANCZOS)
else:
    logo_sm = None
    logo_hero = None

def draw_header(draw, title_suffix=""):
    draw.rectangle([0, 0, WIDTH, 80], fill=(248, 250, 252, 255))
    draw.line([0, 80, WIDTH, 80], fill=(226, 232, 240), width=2)
    draw.text((80, 22), "CHECKMATE", fill=(15, 23, 42), font=font_serif_md)
    draw.rounded_rectangle([270, 26, 345, 54], radius=6, fill=(224, 231, 255))
    draw.text((282, 30), "v1.0", fill=(55, 48, 163), font=font_mono_sm)
    draw.rounded_rectangle([WIDTH - 420, 22, WIDTH - 80, 58], radius=8, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((WIDTH - 400, 29), "Yugaantar DevForge Track 4", fill=(71, 85, 105), font=font_sans_sm)
    if title_suffix:
        draw.text((380, 28), f"|  {title_suffix}", fill=(100, 116, 139), font=font_sans_md)

# -----------------------------------------------------------------------------
# SCENE 1: The Stolen Hardware & MDM Blindspot (0.0s - 7.5s)
# -----------------------------------------------------------------------------
def render_scene_1(t):
    img = Image.new("RGB", (WIDTH, HEIGHT), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # Subtle dark grid
    for x in range(0, WIDTH, 60):
        draw.line([x, 0, x, HEIGHT], fill=(30, 41, 59), width=1)
    for y in range(0, HEIGHT, 60):
        draw.line([0, y, WIDTH, y], fill=(30, 41, 59), width=1)

    draw.text((100, 90), "THE STOLEN HARDWARE & MDM BLINDSPOT", fill=(239, 68, 68), font=font_sans_lg)
    draw.text((100, 145), "Active Enterprise Sessions Are Exposed Post-Theft.", fill=(248, 250, 252), font=font_serif_xl)
    draw.text((100, 230), "Standard JWT tokens stay valid for 15-60 mins. Thieves disconnect Wi-Fi to evade MDM remote wipe.", fill=(148, 163, 184), font=font_sans_md)

    # Terminal window
    x1, y1, x2, y2 = 100, 300, 1150, 920
    draw.rounded_rectangle([x1, y1, x2, y2], radius=14, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    draw.rounded_rectangle([x1, y1, x2, y1 + 48], radius=14, fill=(51, 65, 85))
    draw.rectangle([x1, y1 + 25, x2, y1 + 48], fill=(51, 65, 85))
    draw.ellipse([x1 + 20, y1 + 17, x1 + 34, y1 + 31], fill=(239, 68, 68))
    draw.ellipse([x1 + 44, y1 + 17, x1 + 58, y1 + 31], fill=(245, 158, 11))
    draw.ellipse([x1 + 68, y1 + 17, x1 + 82, y1 + 31], fill=(16, 185, 129))
    draw.text((x1 + 105, y1 + 14), "bash — compromised-laptop (Airplane Mode)", fill=(148, 163, 184), font=font_mono_sm)

    lines = [
        ("1", "# Adversary possesses unlocked engineering workstation", (100, 116, 139)),
        ("2", "$ nmcli radio wifi off  # Disconnect networking (Faraday bag)", (226, 232, 240)),
        ("3", "$ curl -H 'Authorization: Bearer jwt_valid_for_45m' /api/data", (245, 158, 11)),
        ("4", "HTTP/1.1 200 OK  # Token accepted without live server check!", (239, 68, 68)),
        ("5", "$ ./dump_internal_keys.sh", (226, 232, 240)),
        ("6", "Extracting proprietary secrets, customer PII, database keys...", (248, 113, 113)),
        ("7", "[MDM Remote Wipe]: WAITING FOR INTERNET CONNECTION (BLINDED)", (239, 68, 68)),
    ]
    cy = y1 + 70
    for num, txt, col in lines:
        draw.text((x1 + 25, cy), num, fill=(71, 85, 105), font=font_mono_md)
        draw.text((x1 + 75, cy), txt, fill=col, font=font_mono_md)
        cy += 44

    # Right side alert cards
    if t > 1.8:
        prog1 = min(1.0, (t - 1.8) / 0.4)
        rx1 = int(1220 + (1.0 - prog1) * 80)
        draw.rounded_rectangle([rx1, 300, 1820, 510], radius=14, fill=(69, 10, 10), outline=(239, 68, 68), width=2)
        draw.text((rx1 + 30, 330), "⚠️ CRITICAL VULNERABILITY", fill=(248, 113, 113), font=font_sans_lg)
        draw.text((rx1 + 30, 390), "45-Minute Window of Exposure", fill=(255, 255, 255), font=font_serif_lg)
        draw.text((rx1 + 30, 445), "Client-side JWTs cannot be revoked offline.", fill=(254, 202, 202), font=font_sans_md)

    if t > 4.0:
        prog2 = min(1.0, (t - 4.0) / 0.4)
        rx2 = int(1220 + (1.0 - prog2) * 80)
        draw.rounded_rectangle([rx2, 540, 1820, 840], radius=14, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
        draw.text((rx2 + 30, 570), "THE HARVEST-NOW THREAT:", fill=(245, 158, 11), font=font_sans_lg)
        draw.text((rx2 + 30, 630), "✗ Classical RSA/ECDH cracked by quantum computers", fill=(226, 232, 240), font=font_mono_sm)
        draw.text((rx2 + 30, 680), "✗ Adversary intercepts and stores encrypted streams", fill=(226, 232, 240), font=font_mono_sm)
        draw.text((rx2 + 30, 730), "✗ Decrypted later with Shor's polynomial algorithm", fill=(226, 232, 240), font=font_mono_sm)
        draw.text((rx2 + 30, 780), "✗ Zero forward secrecy for long-term secrets", fill=(248, 113, 113), font=font_mono_sm)

    draw.rectangle([0, HEIGHT - 70, WIDTH, HEIGHT], fill=(15, 23, 42))
    draw.line([0, HEIGHT - 70, WIDTH, HEIGHT - 70], fill=(51, 65, 85), width=1)
    draw.text((100, HEIGHT - 46), "PROBLEM: Offline devices bypass MDM wipes while JWTs remain valid post-theft.", fill=(148, 163, 184), font=font_mono_sm)
    return img

# -----------------------------------------------------------------------------
# SCENE 2: The Solution — CheckMate (7.5s - 15.5s)
# -----------------------------------------------------------------------------
def render_scene_2(t):
    img = Image.new("RGB", (WIDTH, HEIGHT), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "The Zero-Trust Architecture")

    st = t - 7.5
    float_y = int(math.sin(st * 3.0) * 8)

    if logo_hero:
        img.paste(logo_hero, (100, 120 + float_y), logo_hero)

    draw.text((500, 130), "CHECKMATE", fill=(15, 23, 42), font=font_serif_xl)
    draw.text((500, 210), "Post-Quantum Zero-Trust Access Guard & Revocation Engine", fill=(71, 85, 105), font=font_sans_lg)
    draw.text((500, 260), "Continuous Server-Side Introspection · NIST FIPS 203 ML-KEM-768 · Sub-Millisecond Killswitch", fill=(37, 99, 235), font=font_sans_md)

    cards = [
        ("⚡ SUB-MS REVOCATION", "< 0.8 ms Killswitch", "Immediate server-side deny. Compromised devices are cut off instantly without waiting for token expiration.", (220, 38, 38), (254, 226, 226)),
        ("🔒 NIST POST-QUANTUM", "ML-KEM-768 (Kyber)", "Lattice-based key encapsulation mathematically immune to Shor's quantum computing cryptanalysis.", (37, 99, 235), (219, 234, 254)),
        ("🛡️ ZERO-TRUST INTRINSIC", "RFC 7662 OAuth 2.0", "Every access request is verified live at the gateway boundary. Offline devices receive zero plaintext.", (16, 185, 129), (209, 250, 229))
    ]

    card_w = 540
    card_h = 420
    cx = 100
    for title, metric, desc, accent, bg_tint in cards:
        draw.rounded_rectangle([cx, 350, cx + card_w, 350 + card_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.rounded_rectangle([cx, 350, cx + card_w, 350 + 60], radius=14, fill=bg_tint)
        draw.rectangle([cx, 350 + 35, cx + card_w, 350 + 60], fill=bg_tint)
        draw.text((cx + 25, 368), title, fill=accent, font=font_sans_lg)
        draw.text((cx + 25, 435), metric, fill=(15, 23, 42), font=font_serif_lg)
        
        # Word wrap description
        words = desc.split(" ")
        lines, cur = [], ""
        for w in words:
            if len(cur + " " + w) < 32:
                cur += (" " if cur else "") + w
            else:
                lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        
        dy = 510
        for l in lines:
            draw.text((cx + 25, dy), l, fill=(71, 85, 105), font=font_sans_md)
            dy += 36
        cx += card_w + 50

    draw.rectangle([0, HEIGHT - 70, WIDTH, HEIGHT], fill=(241, 245, 249))
    draw.line([0, HEIGHT - 70, WIDTH, HEIGHT - 70], fill=(203, 213, 225), width=1)
    draw.text((100, HEIGHT - 46), "SOLUTION: Sub-millisecond revocation killswitch paired with NIST FIPS 203 quantum encapsulation.", fill=(100, 116, 139), font=font_mono_sm)
    return img

# -----------------------------------------------------------------------------
# SCENE 3: Live SecOps & Killswitch in Action (15.5s - 24.5s)
# -----------------------------------------------------------------------------
def render_scene_3(t):
    img = Image.new("RGB", (WIDTH, HEIGHT), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    st = t - 15.5
    draw.text((100, 50), "SECOPS CONTROL CONSOLE & LIVE KILLSWITCH", fill=(148, 163, 184), font=font_sans_sm)
    draw.text((100, 85), "One Click Quarantines The Device Across The Fleet", fill=(248, 250, 252), font=font_serif_xl)

    # SecOps Dashboard Card (Left)
    draw.rounded_rectangle([100, 170, 980, 860], radius=14, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    draw.rounded_rectangle([100, 170, 980, 230], radius=14, fill=(51, 65, 85))
    draw.rectangle([100, 200, 980, 230], fill=(51, 65, 85))
    draw.text((130, 188), "Connected Engineering Workstations — checkmateee.vercel.app/killswitch.html", fill=(226, 232, 240), font=font_mono_sm)

    # Table of devices
    draw.text((130, 260), "ACTOR ID", fill=(148, 163, 184), font=font_sans_sm)
    draw.text((360, 260), "DEVICE & IP", fill=(148, 163, 184), font=font_sans_sm)
    draw.text((640, 260), "STATUS", fill=(148, 163, 184), font=font_sans_sm)
    draw.text((790, 260), "ACTION", fill=(148, 163, 184), font=font_sans_sm)
    draw.line([130, 290, 950, 290], fill=(51, 65, 85), width=1)

    devices = [
        ("dev_suhas", "Windows 11 (192.168.1.104)", st > 2.5),
        ("dev_priya", "macOS Sonoma (10.0.0.12)", False),
        ("ci_runner_01", "Linux AWS EC2 (172.31.8.44)", False),
    ]
    dy = 320
    for actor, dev, is_revoked in devices:
        draw.text((130, dy), actor, fill=(248, 250, 252), font=font_mono_md)
        draw.text((360, dy), dev, fill=(148, 163, 184), font=font_sans_sm)
        
        if is_revoked:
            draw.rounded_rectangle([630, dy-4, 750, dy+28], radius=6, fill=(127, 29, 29))
            draw.text((645, dy+2), "REVOKED", fill=(254, 202, 202), font=font_mono_sm)
            draw.rounded_rectangle([780, dy-4, 930, dy+28], radius=6, fill=(22, 101, 52))
            draw.text((795, dy+2), "Restore Access", fill=(220, 252, 231), font=font_sans_sm)
        else:
            draw.rounded_rectangle([630, dy-4, 750, dy+28], radius=6, fill=(6, 78, 59))
            draw.text((650, dy+2), "ACTIVE", fill=(167, 243, 208), font=font_mono_sm)
            draw.rounded_rectangle([780, dy-4, 930, dy+28], radius=6, fill=(185, 28, 28))
            draw.text((800, dy+2), "⚡ KILLSWITCH", fill=(255, 255, 255), font=font_sans_sm)
        dy += 75

    # Right Side: Client Screen (Quarantined)
    cx1, cy1, cx2, cy2 = 1040, 170, 1820, 860
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=14, fill=(15, 23, 42), outline=(239, 68, 68) if st > 2.5 else (51, 65, 85), width=2)
    
    if st > 2.5:
        # Lockout Modal
        draw.rounded_rectangle([cx1+40, cy1+80, cx2-40, cy2-80], radius=14, fill=(24, 15, 20), outline=(239, 68, 68), width=2)
        draw.text((cx1 + 180, cy1 + 140), "⛔ ACCESS DENIED BY SECURITY POLICY", fill=(239, 68, 68), font=font_sans_lg)
        draw.text((cx1 + 140, cy1 + 220), "[CHECKMATE ZERO-TRUST KILLSWITCH ENGAGED]", fill=(248, 113, 113), font=font_mono_md)
        draw.text((cx1 + 140, cy1 + 280), "Workstation Actor: dev_suhas", fill=(226, 232, 240), font=font_mono_sm)
        draw.text((cx1 + 140, cy1 + 330), "Enforcement: RFC 7662 OAuth 2.0 Introspection Revoked", fill=(248, 113, 113), font=font_mono_sm)
        draw.text((cx1 + 140, cy1 + 380), "Payload Status: Confidential Payloads & Keys Sealed", fill=(248, 113, 113), font=font_mono_sm)
        draw.text((cx1 + 140, cy1 + 450), "All requests to access internal repositories and data are forbidden.", fill=(148, 163, 184), font=font_sans_md)
        draw.rounded_rectangle([cx1 + 260, cy1 + 520, cx1 + 480, cy1 + 570], radius=8, fill=(37, 99, 235))
        draw.text((cx1 + 280, cy1 + 535), "Re-Check Clearance", fill=(255, 255, 255), font=font_sans_sm)
    else:
        draw.text((cx1 + 220, cy1 + 320), "Workstation Active & Authorized", fill=(16, 185, 129), font=font_serif_lg)
        draw.text((cx1 + 240, cy1 + 390), "Continuous introspection polling gateway...", fill=(148, 163, 184), font=font_sans_md)

    draw.rectangle([0, HEIGHT - 70, WIDTH, HEIGHT], fill=(15, 23, 42))
    draw.line([0, HEIGHT - 70, WIDTH, HEIGHT - 70], fill=(51, 65, 85), width=1)
    draw.text((100, HEIGHT - 46), "DEMO: SecOps triggers instant killswitch &rarr; client workstation locks out in < 0.8 ms.", fill=(148, 163, 184), font=font_mono_sm)
    return img

# -----------------------------------------------------------------------------
# SCENE 4: Post-Quantum Cryptographic Inspector (24.5s - 32.5s)
# -----------------------------------------------------------------------------
def render_scene_4(t):
    img = Image.new("RGB", (WIDTH, HEIGHT), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "PQC Cryptographic Inspector")

    draw.text((100, 110), "POST-QUANTUM CRYPTOGRAPHIC VERIFICATION", fill=(37, 99, 235), font=font_sans_sm)
    draw.text((100, 145), "NIST FIPS 203 ML-KEM-768 Lattice Key Encapsulation", fill=(15, 23, 42), font=font_serif_xl)

    # 4 Parameter Cards
    params = [
        ("PUBLIC KEY SIZE", "1,184 Bytes", "Standardized ML-KEM-768 vector public key bytes.", (37, 99, 235)),
        ("CIPHERTEXT SIZE", "1,088 Bytes", "Post-quantum lattice encapsulated ciphertext package.", (13, 148, 136)),
        ("SHARED SECRET", "32 Bytes (256-bit)", "Ephemeral symmetric key derived from lattice math.", (124, 58, 237)),
        ("PROOF INTEGRITY", "HMAC-SHA-256", "Challenge-bound MAC proof: HMAC(Secret, Nonce || Body).", (16, 185, 129))
    ]

    cx = 100
    cw = 390
    for title, val, desc, col in params:
        draw.rounded_rectangle([cx, 230, cx + cw, 420], radius=12, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.text((cx + 20, 255), title, fill=(100, 116, 139), font=font_sans_sm)
        draw.text((cx + 20, 300), val, fill=col, font=font_serif_lg)
        draw.text((cx + 20, 360), desc, fill=(71, 85, 105), font=font_sans_sm)
        cx += cw + 50

    # Large verification terminal
    tx1, ty1, tx2, ty2 = 100, 460, 1820, 880
    draw.rounded_rectangle([tx1, ty1, tx2, ty2], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    draw.rounded_rectangle([tx1, ty1, tx2, ty1 + 45], radius=14, fill=(30, 41, 59))
    draw.rectangle([tx1, ty1 + 25, tx2, ty1 + 45], fill=(30, 41, 59))
    draw.text((tx1 + 25, ty1 + 12), "track4_service.py --op protected_read (NIST FIPS 203 Verification Stream)", fill=(148, 163, 184), font=font_mono_sm)

    term_lines = [
        ("$ python track4_service.py", (148, 163, 184)),
        (">> {\"op\": \"protected_read\", \"actor\": \"dev_suhas\", \"asset\": \"confidential_ip\", \"challenge\": \"ch_99f2a\"}", (226, 232, 240)),
        ("<< [ML-KEM-768]: Encapsulating shared secret against recipient public key...", (56, 189, 248)),
        ("<< [Lattice Vector]: Ciphertext length = 1088 bytes | SharedSecret = 32 bytes (256 bits)", (167, 243, 208)),
        ("<< [HMAC Proof]: b47c9e10283fa8879... bound to challenge 'ch_99f2a' and body.", (250, 204, 21)),
        ("<< Decision: ALLOW | Harvest-Now-Decrypt-Later Immunity = ACTIVE ✓", (52, 211, 153))
    ]
    ty = ty1 + 65
    for txt, col in term_lines:
        draw.text((tx1 + 30, ty), txt, fill=col, font=font_mono_md)
        ty += 50

    draw.rectangle([0, HEIGHT - 70, WIDTH, HEIGHT], fill=(248, 250, 252))
    draw.line([0, HEIGHT - 70, WIDTH, HEIGHT - 70], fill=(226, 232, 240), width=1)
    draw.text((100, HEIGHT - 46), "PQC: Lattice math guarantees data remains confidential even against quantum cryptanalysis.", fill=(100, 116, 139), font=font_mono_sm)
    return img

# -----------------------------------------------------------------------------
# SCENE 5: Outro & Hackathon Deliverables (32.5s - 38.0s)
# -----------------------------------------------------------------------------
def render_scene_5(t):
    img = Image.new("RGB", (WIDTH, HEIGHT), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    for x in range(0, WIDTH, 60):
        draw.line([x, 0, x, HEIGHT], fill=(30, 41, 59), width=1)
    for y in range(0, HEIGHT, 60):
        draw.line([0, y, WIDTH, y], fill=(30, 41, 59), width=1)

    if logo_hero:
        img.paste(logo_hero, (WIDTH // 2 - 180, 110), logo_hero)

    draw.text((WIDTH // 2 - 170, 340), "CHECKMATE", fill=(255, 255, 255), font=font_serif_xl)
    draw.text((WIDTH // 2 - 340, 420), "\"Trust, but verify — continuously, cryptographically, without latency.\"", fill=(148, 163, 184), font=font_serif_md)

    # 3 Summary cards
    sc_w = 460
    sc_h = 240
    start_x = (WIDTH - (3 * sc_w + 2 * 40)) // 2
    
    cards = [
        ("⚡ LIVE SECOPS PORTAL", "https://checkmateee.vercel.app", "Interactive console, emergency killswitch, live PQC inspector.", (37, 99, 235)),
        ("📦 PUBLIC REPOSITORY", "github.com/trivikramkalagi91-commits/CheckMate", "Full source code, Adapter Contract v1, and threat model.", (16, 185, 129)),
        ("🏆 TRACK 4 VERIFIED", "100% Pass Rate (20/20)", "Passes official test validator in offline clean sandbox.", (245, 158, 11))
    ]

    for i, (head, val, desc, col) in enumerate(cards):
        x = start_x + i * (sc_w + 40)
        draw.rounded_rectangle([x, 520, x + sc_w, 520 + sc_h], radius=14, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
        draw.text((x + 25, 545), head, fill=col, font=font_sans_sm)
        draw.text((x + 25, 590), val, fill=(255, 255, 255), font=font_mono_md if len(val) > 20 else font_serif_lg)
        draw.text((x + 25, 680), desc, fill=(148, 163, 184), font=font_sans_sm)

    draw.text((WIDTH // 2 - 280, 830), "Yugaantar DevForge Hackathon 2026 — Track 4: 'Trust, but verify'", fill=(100, 116, 139), font=font_sans_md)
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
    print(f"Rendering {TOTAL_FRAMES} frames ({DURATION}s @ {FPS}fps)...")
    
    output_video = os.path.join(OUTPUT_DIR, "brag.mp4")
    output_poster = os.path.join(OUTPUT_DIR, "brag.jpg")
    output_copy = os.path.join(OUTPUT_DIR, "share-copy.txt")

    # Generate Poster Image (First Settled Frame of Scene 2)
    poster_img = render_scene_2(10.0)
    poster_img.save(output_poster, "JPEG", quality=95)
    print(f"Saved poster frame to {output_poster}")

    # Generate Share Copy
    with open(output_copy, "w", encoding="utf-8") as f:
        f.write(
            "🛡️ Introducing CheckMate — Post-Quantum Zero-Trust Access Guard & Revocation Engine!\n\n"
            "Traditional IAM fails when a laptop is stolen: JWT tokens remain valid for 15-60 mins, "
            "and thieves disconnect Wi-Fi to evade MDM remote wipes. Furthermore, classical RSA/ECDH keys "
            "are vulnerable to 'Harvest Now, Decrypt Later' quantum attacks.\n\n"
            "CheckMate solves this:\n"
            "⚡ Sub-Millisecond Actor Killswitch (< 0.8 ms)\n"
            "🔒 NIST FIPS 203 ML-KEM-768 Post-Quantum Key Encapsulation\n"
            "🛡️ RFC 7662 OAuth 2.0 Continuous Server-Side Introspection\n\n"
            "Built for Yugaantar DevForge Hackathon (Track 4: 'Trust, but verify').\n\n"
            "🌐 Live Console: https://checkmateee.vercel.app\n"
            "📦 Code: https://github.com/trivikramkalagi91-commits/CheckMate\n"
        )
    print(f"Saved share copy to {output_copy}")

    # Music path from skill
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
        "-crf", "19",
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

    print(f"Video saved to: {output_video}")
    print("Video generation complete!")

if __name__ == "__main__":
    main()
