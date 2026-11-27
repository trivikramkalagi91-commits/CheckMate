#!/usr/bin/env python3
"""
Generate the official 2-page Track 4 Project Brief PDF for submission.
Includes:
- Page 1: USP & System Architecture Overview
- Page 2: One-Page Threat Model, Invariants, Limitations, & Demo Video Link
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

def generate_pdf():
    pdf_filename = "CheckMate_Track4_Project_Brief.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.4 * inch,
        bottomMargin=0.4 * inch
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=10
    )
    
    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        spaceAfter=3
    )

    story = []

    # -------------------------------------------------------------
    # PAGE 1: USP & SYSTEM ARCHITECTURE
    # -------------------------------------------------------------
    story.append(Paragraph("CheckMate: Post-Quantum Zero-Trust Access Guard", title_style))
    story.append(Paragraph("Track 4: 'Trust, but verify' &mdash; 2-Page Project Brief & Architecture", subtitle_style))
    
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "Modern enterprise Identity & Access Management (IAM) architectures suffer from a critical failure window "
        "when a corporate device is lost or stolen. Traditional security models trust client-side tokens (JWTs) "
        "for 15&ndash;60 minutes post-issuance, and depend on Mobile Device Management (MDM) wipe commands that can be "
        "completely evaded by placing the device into Airplane Mode or a Faraday cage. Furthermore, classical key exchanges "
        "(RSA, ECDH) are vulnerable to 'Harvest Now, Decrypt Later' quantum attacks using Shor's algorithm.",
        body_style
    ))
    
    story.append(Paragraph("2. Unique Selling Proposition (USP)", h1_style))
    story.append(Paragraph("<b>&bull; Sub-Millisecond Revocation (&lt;1 ms):</b> Server-side zero-trust check on every single transaction immediately neutralizes stolen credentials across all nodes without waiting for token expiry.", bullet_style))
    story.append(Paragraph("<b>&bull; NIST FIPS 203 ML-KEM-768 Lattice Cryptography:</b> Quantum-immune post-quantum key encapsulation protects confidential data transfers against future cryptanalytic threats.", bullet_style))
    story.append(Paragraph("<b>&bull; Complete Offline & Air-Gapped Operation:</b> Zero external network dependencies at runtime; headless CLI filter reading JSON requests via stdin and emitting deterministic responses to stdout in under 300 ms.", bullet_style))
    story.append(Paragraph("<b>&bull; Crash-Consistent Atomic Persistence:</b> State updates (owners, contents, revocations, and audit logs) use atomic POSIX filesystem replacement (os.replace + fsync), guaranteeing zero state corruption.", bullet_style))
    story.append(Paragraph("<b>&bull; Zero-Dependency Guard SDK:</b> Lightweight drop-in middleware (checkmate_guard.py) allows any corporate codebase to enforce workstation authorization via environment secrets (.env).", bullet_style))

    story.append(Paragraph("3. System Architecture & Adapter Contract v1", h1_style))
    
    table_data = [
        [
            Paragraph("<b>Operation</b>", body_style),
            Paragraph("<b>Payload Parameters</b>", body_style),
            Paragraph("<b>Output Response</b>", body_style),
            Paragraph("<b>Security Guarantee</b>", body_style)
        ],
        [
            Paragraph("<b>setup</b>", body_style),
            Paragraph("owners, contents, disabled, key_material", body_style),
            Paragraph("{\"ready\": true}", body_style),
            Paragraph("Resets state cleanly; protects raw key_material.", body_style)
        ],
        [
            Paragraph("<b>read</b>", body_style),
            Paragraph("actor, asset, request_id", body_style),
            Paragraph("{\"decision\": \"allow\", \"body\": ...} or {\"decision\": \"deny\"}", body_style),
            Paragraph("Zero-trust owner/revocation check. Logs decision.", body_style)
        ],
        [
            Paragraph("<b>revoke</b>", body_style),
            Paragraph("actor", body_style),
            Paragraph("{}", body_style),
            Paragraph("Immediate killswitch. Atomically written to disk.", body_style)
        ],
        [
            Paragraph("<b>audit</b>", body_style),
            Paragraph("request_id", body_style),
            Paragraph("{\"request_id\": ..., \"decision\": ...}", body_style),
            Paragraph("Deterministic compliance lookup of past events.", body_style)
        ],
        [
            Paragraph("<b>protected_read</b>", body_style),
            Paragraph("actor, asset, challenge, public_key", body_style),
            Paragraph("{\"ciphertext\": ..., \"proof\": ...} or {\"decision\": \"deny\"}", body_style),
            Paragraph("ML-KEM-768 encapsulation + HMAC-SHA256 proof.", body_style)
        ]
    ]
    
    t1 = Table(table_data, colWidths=[1.1*inch, 2.3*inch, 2.0*inch, 1.8*inch])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t1)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Verification & Readiness:</b> 100% test pass rate across all 21 Adapter Contract functional tests and 9-phase end-to-end simulated lifecycle scenarios.", body_style))

    # -------------------------------------------------------------
    # PAGE 2: THREAT MODEL & LIMITATIONS
    # -------------------------------------------------------------
    story.append(PageBreak())
    
    story.append(Paragraph("CheckMate: One-Page Threat Model & Verification", title_style))
    story.append(Paragraph("Threat Surface, Attacker Capabilities, Invariants, & Submission Deliverables", subtitle_style))
    
    story.append(Paragraph("1. Protected Assets", h1_style))
    story.append(Paragraph("<b>&bull; Confidential Payloads:</b> Proprietary source code, financial records, cryptographic keys, and database credentials.", bullet_style))
    story.append(Paragraph("<b>&bull; Dynamic Session Secrets:</b> 32-byte ephemeral symmetric secrets derived via post-quantum ML-KEM-768 encapsulation.", bullet_style))
    story.append(Paragraph("<b>&bull; Immutable Audit Ledger:</b> Non-repudiable access event records indexed by deterministic request IDs.", bullet_style))

    story.append(Paragraph("2. Threat Vectors & Security Invariants", h1_style))
    
    threat_data = [
        [
            Paragraph("<b>Threat Vector</b>", body_style),
            Paragraph("<b>Attacker Model / Assumption</b>", body_style),
            Paragraph("<b>CheckMate Mitigation & Invariant</b>", body_style)
        ],
        [
            Paragraph("<b>Stolen Hardware / Active Session</b>", body_style),
            Paragraph("Attacker physically possesses workstation; extracts memory tokens.", body_style),
            Paragraph("<b>Sub-Millisecond Revocation:</b> Central registry blocks the next read immediately; no residual token trust.", body_style)
        ],
        [
            Paragraph("<b>Airplane Mode MDM Bypass</b>", body_style),
            Paragraph("Device is placed in Faraday cage; MDM remote wipe cannot reach it.", body_style),
            Paragraph("<b>Server-Side Enforcement:</b> Data access requires continuous verification at server boundary. Offline client has zero data access.", body_style)
        ],
        [
            Paragraph("<b>Harvest Now, Decrypt Later</b>", body_style),
            Paragraph("Adversary records encrypted network sessions for future quantum attack.", body_style),
            Paragraph("<b>NIST ML-KEM-768 Lattice Cryptography:</b> Resistant to quantum polynomial-time Shor's algorithm.", body_style)
        ],
        [
            Paragraph("<b>Replay & Message Tampering</b>", body_style),
            Paragraph("Attacker retransmits intercepted messages or alters recipient metadata.", body_style),
            Paragraph("<b>Challenge-Bound HMAC:</b> Challenge nonces and asset content are bound to ephemeral shared secrets; replays fail.", body_style)
        ],
        [
            Paragraph("<b>Log Tampering / Injection</b>", body_style),
            Paragraph("Malicious actor injects fake entries or attempts log boundary corruption.", body_style),
            Paragraph("<b>Structured JSON Audit Trail:</b> Requests indexed strictly by request_id. Raw string inputs cannot inject log records.", body_style)
        ]
    ]
    
    t2 = Table(threat_data, colWidths=[1.8*inch, 2.6*inch, 2.8*inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t2)

    story.append(Paragraph("3. Known Boundaries & Limitations", h1_style))
    story.append(Paragraph("<b>&bull; Endpoint Protection Scope:</b> CheckMate controls access at the application and API boundary. Data already exported to unencrypted physical disks prior to theft relies on full-disk encryption (BitLocker / FileVault).", bullet_style))
    story.append(Paragraph("<b>&bull; Shared State Boundary:</b> Multi-node enforcement assumes access to a synchronized state directory (TRACK4_STATE_DIR) or cloud policy sync endpoint.", bullet_style))

    story.append(Paragraph("4. Submission Links & Video Deliverable", h1_style))
    story.append(Paragraph("<b>Public GitHub Repository:</b> <a href='https://github.com/trivikramkalagi91-commits/CheckMate'>https://github.com/trivikramkalagi91-commits/CheckMate</a>", body_style))
    story.append(Paragraph("<b>Live Cloud Demonstration:</b> <a href='https://checkmateee.vercel.app/console.html'>https://checkmateee.vercel.app/console.html</a> (SecOps Console) & <a href='https://checkmateee.vercel.app/killswitch.html'>https://checkmateee.vercel.app/killswitch.html</a> (Emergency Killswitch)", body_style))
    story.append(Paragraph("<b>5-Minute Walkthrough Video Link:</b> <i>[Insert your unlisted YouTube or Google Drive walkthrough link here prior to submission]</i>", body_style))

    doc.build(story)
    print(f"Successfully generated {pdf_filename}!")

if __name__ == "__main__":
    generate_pdf()
