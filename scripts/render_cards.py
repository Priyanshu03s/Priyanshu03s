#!/usr/bin/env python3
"""
render_cards.py
Generates high-definition, animated SVG cards for Priyanshu Thakur's GitHub profile.
Theme: Cyber Dark (#0B0F19) with Neon Cyan (#00F0FF) and Violet (#8B5CF6) accents.
"""

import os
import sys
import json
import argparse
from pathlib import Path
import urllib.request
import urllib.error

GITHUB_USER = "Priyanshu03s"

def fetch_github_data(username=GITHUB_USER):
    headers = {"User-Agent": "Mozilla/5.0"}
    user_data = None
    repos_data = []

    try:
        req = urllib.request.Request(f"https://api.github.com/users/{username}", headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            user_data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"Notice: Using fallback user data ({e})")
        user_data = {
            "name": "Priyanshu Thakur",
            "login": username,
            "public_repos": 5,
            "followers": 10,
            "bio": "AI Engineer building RAG systems, AI applications & scalable software"
        }

    try:
        req = urllib.request.Request(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            repos_data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"Notice: Using fallback repos data ({e})")
        repos_data = [
            {"name": "3D-Portfolio", "language": "JavaScript", "stargazers_count": 0},
            {"name": "CONSTRUCTION-LIBRARY", "language": "HTML", "stargazers_count": 1},
            {"name": "fishbone-diagram", "language": "TypeScript", "stargazers_count": 1},
            {"name": "netflix-clone-", "language": "CSS", "stargazers_count": 1},
            {"name": "Practice-Program", "language": "Java", "stargazers_count": 0}
        ]

    return user_data, repos_data


def generate_hero_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 240" width="100%" height="240">
  <defs>
    <linearGradient id="hero-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF" />
      <stop offset="50%" stop-color="#8B5CF6" />
      <stop offset="100%" stop-color="#00F0FF" />
    </linearGradient>
    <linearGradient id="hero-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070B14" />
      <stop offset="50%" stop-color="#0B0F19" />
      <stop offset="100%" stop-color="#0E1626" />
    </linearGradient>
    <radialGradient id="glow" cx="80%" cy="20%" r="60%">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.18" />
      <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="cyan-glow" cx="20%" cy="80%" r="50%">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#00F0FF" stop-opacity="0" />
    </radialGradient>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#1F293D" stroke-width="0.5" stroke-opacity="0.5" />
    </pattern>
    <style>
      .title { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-weight: 800; font-size: 32px; fill: #FFFFFF; letter-spacing: 1px; }
      .badge-text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-weight: 700; font-size: 13px; fill: #00F0FF; letter-spacing: 1.5px; }
      .subtitle { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 16px; fill: #94A3B8; font-weight: 400; }
      .meta { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 13px; fill: #CBD5E1; font-weight: 500; }
      .pulse-dot { animation: pulse 2s infinite ease-in-out; }
      @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.35; transform: scale(0.85); } }
    </style>
  </defs>

  <!-- Background -->
  <rect width="900" height="240" rx="16" fill="url(#hero-bg)" />
  <rect width="900" height="240" rx="16" fill="url(#grid)" />
  <rect width="900" height="240" rx="16" fill="url(#glow)" />
  <rect width="900" height="240" rx="16" fill="url(#cyan-glow)" />

  <!-- Outer Border -->
  <rect x="1" y="1" width="898" height="238" rx="15" fill="none" stroke="url(#hero-border)" stroke-width="1.5" stroke-opacity="0.8" />

  <!-- Status Chip -->
  <g transform="translate(40, 36)">
    <rect width="185" height="28" rx="14" fill="#0E1E38" stroke="#00F0FF" stroke-width="1" stroke-opacity="0.4" />
    <circle cx="16" cy="14" r="5" fill="#10B981" class="pulse-dot" />
    <text x="30" y="18" class="badge-text" fill="#00F0FF" style="font-size: 11px;">SYSTEM: ACTIVE &amp; BUILDING</text>
  </g>

  <!-- Title & Headline -->
  <text x="40" y="104" class="title">PRIYANSHU THAKUR</text>
  <text x="375" y="104" class="badge-text" fill="#8B5CF6" style="font-size: 14px;">// AI ENGINEER</text>

  <!-- Subtitle -->
  <text x="40" y="142" class="subtitle">Architecting RAG Systems • Enterprise Spring Boot • Scalable Full-Stack Architectures</text>

  <!-- Location & Focus Badges -->
  <g transform="translate(40, 175)">
    <!-- Location Pill -->
    <rect width="165" height="30" rx="8" fill="#151D2E" stroke="#334155" stroke-width="1" />
    <text x="14" y="20" class="meta">📍 Delhi NCR, India</text>

    <!-- Focus Pill -->
    <rect x="180" width="220" height="30" rx="8" fill="#151D2E" stroke="#334155" stroke-width="1" />
    <text x="194" y="20" class="meta">⚡ LLMs, Agents &amp; Cloud Systems</text>

    <!-- Status Pill -->
    <rect x="415" width="235" height="30" rx="8" fill="#151D2E" stroke="#8B5CF6" stroke-width="1" stroke-opacity="0.5" />
    <text x="429" y="20" class="meta" fill="#A78BFA">🚀 Open to High-Impact Roles</text>
  </g>
</svg>"""


def generate_pillars_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 130" width="100%" height="130">
  <defs>
    <linearGradient id="card-border" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0.6" />
    </linearGradient>
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0E1626" />
      <stop offset="100%" stop-color="#090D17" />
    </linearGradient>
    <style>
      .col-title { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 700; font-size: 14px; fill: #F8FAFC; letter-spacing: 0.8px; }
      .col-desc { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; fill: #94A3B8; font-weight: 400; line-height: 1.5; }
      .icon-box { fill: #1E293B; stroke: #334155; }
    </style>
  </defs>

  <!-- Pillar 1: AI & RAG -->
  <g transform="translate(0, 0)">
    <rect width="288" height="130" rx="12" fill="url(#card-bg)" stroke="url(#card-border)" stroke-width="1" />
    <circle cx="36" cy="36" r="16" fill="#1E293B" stroke="#00F0FF" stroke-width="1" stroke-opacity="0.8" />
    <text x="28" y="42" font-size="16">🧠</text>
    <text x="64" y="36" class="col-title" fill="#00F0FF">AI &amp; RAG SYSTEMS</text>
    <text x="64" y="52" class="col-desc" fill="#64748B" style="font-size: 11px;">Context Retrieval &amp; Agents</text>
    <text x="24" y="85" class="col-desc">Vector Search • Embeddings</text>
    <text x="24" y="105" class="col-desc">LangChain • LlamaIndex • Agents</text>
  </g>

  <!-- Pillar 2: Enterprise Backend -->
  <g transform="translate(306, 0)">
    <rect width="288" height="130" rx="12" fill="url(#card-bg)" stroke="url(#card-border)" stroke-width="1" />
    <circle cx="36" cy="36" r="16" fill="#1E293B" stroke="#8B5CF6" stroke-width="1" stroke-opacity="0.8" />
    <text x="28" y="42" font-size="16">⚙️</text>
    <text x="64" y="36" class="col-title" fill="#A78BFA">ENTERPRISE BACKEND</text>
    <text x="64" y="52" class="col-desc" fill="#64748B" style="font-size: 11px;">Scalable Microservices</text>
    <text x="24" y="85" class="col-desc">Java • Spring Boot • Hibernate</text>
    <text x="24" y="105" class="col-desc">REST APIs • Microservices • SQL</text>
  </g>

  <!-- Pillar 3: Immersive Web -->
  <g transform="translate(612, 0)">
    <rect width="288" height="130" rx="12" fill="url(#card-bg)" stroke="url(#card-border)" stroke-width="1" />
    <circle cx="36" cy="36" r="16" fill="#1E293B" stroke="#38BDF8" stroke-width="1" stroke-opacity="0.8" />
    <text x="28" y="42" font-size="16">🎨</text>
    <text x="64" y="36" class="col-title" fill="#38BDF8">IMMERSIVE CLIENTS</text>
    <text x="64" y="52" class="col-desc" fill="#64748B" style="font-size: 11px;">Interactive 3D &amp; Modern UI</text>
    <text x="24" y="85" class="col-desc">Angular • TypeScript • Three.js</text>
    <text x="24" y="105" class="col-desc">Reactive Interfaces • Modern Web</text>
  </g>
</svg>"""


def generate_stats_svg(user_data=None, repos_data=None):
    repos_count = user_data.get("public_repos", 5) if user_data else 5

    # Language breakdown logic
    lang_counts = {}
    if repos_data:
        for r in repos_data:
            lang = r.get("language")
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + 1

    top_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    if not top_langs:
        top_langs = [("Python", 4), ("Java", 3), ("TypeScript", 3), ("JavaScript", 2), ("HTML/CSS", 2)]

    total_shares = sum(count for _, count in top_langs) or 1
    
    # Generate language distribution bar segments
    colors = ["#00F0FF", "#8B5CF6", "#38BDF8", "#F59E0B", "#10B981"]
    bar_x = 0
    bar_elements = []
    legend_elements = []
    
    for i, (lang, count) in enumerate(top_langs):
        color = colors[i % len(colors)]
        pct = (count / total_shares) * 100
        width = (count / total_shares) * 440
        bar_elements.append(f'<rect x="{380 + bar_x:.1f}" y="85" width="{width:.1f}" height="10" rx="3" fill="{color}" />')
        bar_x += width
        
        # Legend item
        leg_x = 380 + (i % 3) * 155
        leg_y = 125 + (i // 3) * 24
        legend_elements.append(
            f'<circle cx="{leg_x}" cy="{leg_y - 4}" r="4" fill="{color}" />'
            f'<text x="{leg_x + 10}" y="{leg_y}" font-family="sans-serif" font-size="12" fill="#94A3B8">{lang} <tspan fill="#F1F5F9" font-weight="600">{pct:.0f}%</tspan></text>'
        )

    bars_svg = "\n    ".join(bar_elements)
    legends_svg = "\n    ".join(legend_elements)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 170" width="100%" height="170">
  <defs>
    <linearGradient id="stats-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B0F19" />
      <stop offset="100%" stop-color="#0E172A" />
    </linearGradient>
    <style>
      .stat-num {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 26px; font-weight: 800; fill: #00F0FF; }}
      .stat-label {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; font-weight: 500; fill: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; }}
      .header-title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; font-weight: 700; fill: #F8FAFC; letter-spacing: 1px; }}
    </style>
  </defs>

  <rect width="900" height="170" rx="14" fill="url(#stats-bg)" stroke="#1E293B" stroke-width="1.5" />

  <!-- Left: Activity Metrics -->
  <g transform="translate(30, 25)">
    <text x="0" y="16" class="header-title" fill="#8B5CF6">📊 GITHUB ACTIVITY &amp; STATS</text>

    <!-- Metric 1 -->
    <g transform="translate(0, 45)">
      <text x="0" y="24" class="stat-num">{repos_count}</text>
      <text x="0" y="44" class="stat-label">Public Repositories</text>
    </g>

    <!-- Metric 2 -->
    <g transform="translate(130, 45)">
      <text x="0" y="24" class="stat-num" fill="#8B5CF6">Active</text>
      <text x="0" y="44" class="stat-label">Building &amp; Shipping</text>
    </g>

    <!-- Metric 3 -->
    <g transform="translate(235, 45)">
      <text x="0" y="24" class="stat-num" fill="#10B981">Daily</text>
      <text x="0" y="44" class="stat-label">Actions Sync</text>
    </g>
  </g>

  <!-- Divider line -->
  <line x1="345" y1="25" x2="345" y2="145" stroke="#1E293B" stroke-width="1.5" />

  <!-- Right: Top Languages Distribution -->
  <text x="380" y="41" class="header-title" fill="#00F0FF">⚡ TOP REPOSITORY LANGUAGES</text>
  <rect x="380" y="85" width="480" height="10" rx="3" fill="#1E293B" />
  <g>
    {bars_svg}
  </g>
  <g>
    {legends_svg}
  </g>
</svg>"""


def generate_tech_matrix_svg():
    categories = [
        {
            "name": "AI, RAG &amp; ML",
            "color": "#00F0FF",
            "skills": ["Python", "LangChain", "Vector DBs", "RAG Pipelines", "FastAPI", "HuggingFace"]
        },
        {
            "name": "ENTERPRISE BACKEND",
            "color": "#8B5CF6",
            "skills": ["Java", "Spring Boot", "Hibernate", "RESTful APIs", "Microservices", "SQL/PostgreSQL"]
        },
        {
            "name": "FRONTEND &amp; GRAPHICS",
            "color": "#38BDF8",
            "skills": ["Angular", "TypeScript", "JavaScript", "Three.js (3D)", "HTML5 / CSS3", "Tailwind"]
        },
        {
            "name": "TOOLS &amp; ARCHITECTURE",
            "color": "#10B981",
            "skills": ["Git", "GitHub Actions", "Docker", "Linux", "Postman", "CI/CD Workflows"]
        }
    ]

    svg_rows = []
    y_offset = 55

    for cat in categories:
        pill_elements = []
        x_offset = 200
        for skill in cat["skills"]:
            pill_width = len(skill) * 7.5 + 20
            pill_elements.append(
                f'<rect x="{x_offset}" y="{y_offset - 16}" width="{pill_width:.0f}" height="24" rx="6" fill="#151D2E" stroke="{cat["color"]}" stroke-width="0.8" stroke-opacity="0.4" />'
                f'<text x="{x_offset + 10}" y="{y_offset}" font-family="sans-serif" font-size="11" fill="#E2E8F0" font-weight="500">{skill}</text>'
            )
            x_offset += pill_width + 8

        pills_str = "\n    ".join(pill_elements)
        svg_rows.append(f"""
  <!-- {cat["name"]} -->
  <g>
    <rect x="25" y="{y_offset - 16}" width="160" height="24" rx="6" fill="#0E1626" stroke="{cat["color"]}" stroke-width="1" />
    <text x="35" y="{y_offset}" font-family="sans-serif" font-size="11" font-weight="700" fill="{cat["color"]}">{cat["name"]}</text>
    {pills_str}
  </g>""")
        y_offset += 38

    categories_svg = "\n".join(svg_rows)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 215" width="100%" height="215">
  <defs>
    <linearGradient id="matrix-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B0F19" />
      <stop offset="100%" stop-color="#080C14" />
    </linearGradient>
  </defs>

  <rect width="900" height="215" rx="14" fill="url(#matrix-bg)" stroke="#1E293B" stroke-width="1.5" />
  <text x="25" y="28" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700" fill="#F8FAFC" letter-spacing="1px">🛠️ TECHNICAL ARCHITECTURE MATRIX</text>
  {categories_svg}
</svg>"""


def generate_spotlight_cards():
    cards = {}

    # Card 1: RAG & AI Systems
    cards["card-rag.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 290 160" width="100%" height="160">
  <defs>
    <linearGradient id="card1-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B132B" />
      <stop offset="100%" stop-color="#070A12" />
    </linearGradient>
  </defs>
  <rect width="290" height="160" rx="12" fill="url(#card1-bg)" stroke="#00F0FF" stroke-width="1" stroke-opacity="0.6" />
  <circle cx="28" cy="28" r="14" fill="#1C2541" />
  <text x="22" y="33" font-size="14">🤖</text>
  <text x="50" y="32" font-family="sans-serif" font-weight="700" font-size="13" fill="#00F0FF">RAG &amp; AI AGENTS</text>
  <text x="20" y="65" font-family="sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">AI Knowledge Retrieval</text>
  <text x="20" y="85" font-family="sans-serif" font-size="11" fill="#94A3B8">Semantic Search &amp; Embeddings</text>
  <text x="20" y="102" font-family="sans-serif" font-size="11" fill="#94A3B8">Autonomous LLM Workflows</text>
  <rect x="20" y="122" width="70" height="20" rx="5" fill="#1E293B" />
  <text x="28" y="136" font-family="sans-serif" font-size="10" fill="#00F0FF">Python</text>
  <rect x="98" y="122" width="85" height="20" rx="5" fill="#1E293B" />
  <text x="106" y="136" font-family="sans-serif" font-size="10" fill="#38BDF8">Vector DBs</text>
</svg>"""

    # Card 2: Enterprise Spring Boot
    cards["card-enterprise.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 290 160" width="100%" height="160">
  <defs>
    <linearGradient id="card2-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1A0B2E" />
      <stop offset="100%" stop-color="#0A0612" />
    </linearGradient>
  </defs>
  <rect width="290" height="160" rx="12" fill="url(#card2-bg)" stroke="#8B5CF6" stroke-width="1" stroke-opacity="0.6" />
  <circle cx="28" cy="28" r="14" fill="#2E1065" />
  <text x="22" y="33" font-size="14">⚡</text>
  <text x="50" y="32" font-family="sans-serif" font-weight="700" font-size="13" fill="#A78BFA">SPRING BOOT CORE</text>
  <text x="20" y="65" font-family="sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">Enterprise Services</text>
  <text x="20" y="85" font-family="sans-serif" font-size="11" fill="#94A3B8">Employee Communication</text>
  <text x="20" y="102" font-family="sans-serif" font-size="11" fill="#94A3B8">Secure Microservice APIs</text>
  <rect x="20" y="122" width="60" height="20" rx="5" fill="#2E1065" />
  <text x="28" y="136" font-family="sans-serif" font-size="10" fill="#A78BFA">Java</text>
  <rect x="88" y="122" width="90" height="20" rx="5" fill="#2E1065" />
  <text x="96" y="136" font-family="sans-serif" font-size="10" fill="#C084FC">Spring Boot</text>
</svg>"""

    # Card 3: 3D Portfolio & Web Apps
    cards["card-3d.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 290 160" width="100%" height="160">
  <defs>
    <linearGradient id="card3-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0A192F" />
      <stop offset="100%" stop-color="#050B14" />
    </linearGradient>
  </defs>
  <rect width="290" height="160" rx="12" fill="url(#card3-bg)" stroke="#38BDF8" stroke-width="1" stroke-opacity="0.6" />
  <circle cx="28" cy="28" r="14" fill="#0F2942" />
  <text x="22" y="33" font-size="14">🌐</text>
  <text x="50" y="32" font-family="sans-serif" font-weight="700" font-size="13" fill="#38BDF8">3D &amp; INTERACTIVE UI</text>
  <text x="20" y="65" font-family="sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">3D Web Portfolio</text>
  <text x="20" y="85" font-family="sans-serif" font-size="11" fill="#94A3B8">WebGL &amp; Three.js Rendering</text>
  <text x="20" y="102" font-family="sans-serif" font-size="11" fill="#94A3B8">Dynamic Angular Systems</text>
  <rect x="20" y="122" width="80" height="20" rx="5" fill="#0F2942" />
  <text x="28" y="136" font-family="sans-serif" font-size="10" fill="#38BDF8">JavaScript</text>
  <rect x="108" y="122" width="85" height="20" rx="5" fill="#0F2942" />
  <text x="116" y="136" font-family="sans-serif" font-size="10" fill="#7DD3FC">Angular / 3D</text>
</svg>"""

    return cards


def main():
    parser = argparse.ArgumentParser(description="Render animated SVG profile cards for GitHub")
    parser.add_argument("--user", default=GITHUB_USER, help="GitHub username")
    parser.add_argument("--output-dir", default=None, help="Cards output directory")
    args = parser.parse_args()

    # Determine cards path
    if args.output_dir:
        cards_dir = Path(args.output_dir)
    else:
        # Default to ../cards relative to this script
        cards_dir = Path(__file__).resolve().parent.parent / "cards"

    spotlight_dir = cards_dir / "spotlight"
    cards_dir.mkdir(parents=True, exist_ok=True)
    spotlight_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching GitHub data for {args.user}...")
    user_data, repos_data = fetch_github_data(args.user)

    print("Generating cards...")
    (cards_dir / "hero.svg").write_text(generate_hero_svg(), encoding="utf-8")
    print("✓ hero.svg")

    (cards_dir / "pillars.svg").write_text(generate_pillars_svg(), encoding="utf-8")
    print("✓ pillars.svg")

    (cards_dir / "stats.svg").write_text(generate_stats_svg(user_data, repos_data), encoding="utf-8")
    print("✓ stats.svg")

    (cards_dir / "tech_matrix.svg").write_text(generate_tech_matrix_svg(), encoding="utf-8")
    print("✓ tech_matrix.svg")

    spotlight_cards = generate_spotlight_cards()
    for name, content in spotlight_cards.items():
        (spotlight_dir / name).write_text(content, encoding="utf-8")
        print(f"✓ spotlight/{name}")

    print("\nAll SVG profile cards generated successfully!")


if __name__ == "__main__":
    main()
