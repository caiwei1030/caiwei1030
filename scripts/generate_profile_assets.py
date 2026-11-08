#!/usr/bin/env python3
"""Generate the animated SVG chips and field guides used by README.md."""

import hashlib
import html
import random
import re
import textwrap
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "chips"
LOCAL_ICONS = Path(__file__).resolve().parent / "icons"
ICON_URL = "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{}.svg"
FONT = "Segoe UI, Ubuntu, Helvetica, Arial, sans-serif"
CHIP_COLOURS = ["#E2542F", "#F4795B", "#ED8B66", "#7FA36B"]
GREY = "#8b949e"


STACK = [
    ("AGENTS", "#7FA36B", "#5E8B4F", [
        ("python", "python", "Python", "The common language across the agent runtime, evaluation scripts, and optimization pipelines."),
        ("langgraph", "langgraph", "LangGraph", "Graph orchestration for stateful agents, controllable tool calls, checkpoints, and human-in-the-loop flows."),
        ("langchain", "langchain", "LangChain", "Composition layer for prompts, retrievers, tools, and model I/O used alongside custom orchestration logic."),
        ("pydantic", "pydantic", "Pydantic", "Typed schemas and validation for agent inputs, tool contracts, configuration, and structured responses."),
        ("fastapi", "fastapi", "FastAPI", "Service boundary for exposing agent workflows with asynchronous APIs and typed request models."),
        ("tool-safety", "githubactions", "Tool Safety", "Path rules, command constraints, allowlists, timeouts, and run records for dependable agent tools."),
    ]),
    ("AI / ML", "#EEA53A", "#D98828", [
        ("pytorch", "pytorch", "PyTorch", "Foundation for model implementations, training loops, tensor operations, and architecture experiments."),
        ("transformers", "huggingface", "Transformers", "Neural sequence models for language understanding, generation, and transfer learning."),
        ("deep-learning", None, "Deep Learning", "Representation learning, anomaly detection, clustering, and end-to-end differentiable models."),
        ("llm", None, "LLM", "Language model systems for planning, code generation, orchestration, and domain-specific workflows."),
    ]),
    ("OPTIMIZATION", "#F4795B", "#E2542F", [
        ("nsga2", None, "NSGA-II", "Multi-objective evolutionary search that maintains a diverse Pareto front under simulation constraints."),
        ("differential-evolution", None, "DE", "Adaptive global search for continuous circuit variables and staged simulation control."),
        ("kmeans", "scikitlearn", "K-means", "Clustering search samples into behavioral regions before selecting promising candidates."),
        ("isolation-forest", "scikitlearn", "Isolation Forest", "Unsupervised filtering of abnormal simulations and unreliable regions of the search space."),
        ("morris", None, "Morris", "Global sensitivity analysis for retaining high-impact variables and reducing optimization dimensionality."),
    ]),
    ("LEARNING", "#9986D4", "#7361BE", [
        ("transformer-lm", None, "Transformer", "Attention-based language modeling built from tokenizer inputs through causal decoder layers."),
        ("bpe", None, "BPE", "Byte-pair encoding with streaming merges, word-level caching, and reproducible vocabulary training."),
        ("rope", None, "RoPE", "Rotary position embeddings that encode relative position inside multi-head attention."),
        ("swiglu", None, "SwiGLU", "Gated activation blocks that improve transformer feed-forward expressiveness."),
        ("adamw", None, "AdamW", "Adaptive optimization with decoupled weight decay, warmup, and cosine learning-rate schedules."),
    ]),
]


_icon_cache = {}


def icon_path(slug):
    if not slug:
        return None
    if slug not in _icon_cache:
        try:
            local_path = LOCAL_ICONS / f"{slug}.svg"
            if local_path.exists():
                source = local_path.read_text(encoding="utf-8")
            else:
                request = urllib.request.Request(
                    ICON_URL.format(slug), headers={"User-Agent": "caiwei1030-profile-assets"}
                )
                with urllib.request.urlopen(request, timeout=20) as response:
                    source = response.read().decode("utf-8")
            match = re.search(r'<path d="([^"]+)"', source)
            _icon_cache[slug] = match.group(1) if match else None
        except (OSError, UnicodeDecodeError):
            _icon_cache[slug] = None
    return _icon_cache[slug]


def svg(width, height, title, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="{FONT}">'
        f'<title>{html.escape(title)}</title>{body}</svg>\n'
    )


def flower(x, y, petal, centre, duration):
    petals = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="3.4" fill="{petal}"/>'
        for cx, cy in [(0, -6.5), (6.2, -2), (3.8, 5.3), (-3.8, 5.3), (-6.2, -2)]
    )
    return (
        f'<g transform="translate({x},{y})"><g>'
        f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" '
        f'dur="{duration}s" repeatCount="indefinite"/>{petals}</g>'
        f'<circle r="2.8" fill="{centre}"/></g>'
    )


def chip(label, icon_slug, colour):
    generator = random.Random(label)
    duration = 3.5 + generator.random()
    begin = -generator.random() * 4
    glyph = icon_path(icon_slug)
    width = int(len(label) * 7.2 + (46 if glyph else 26))

    if glyph:
        inner = (
            f'<g transform="translate(12,8) scale(0.5833)">'
            f'<path d="{glyph}" fill="{colour}"/></g>'
            f'<text x="32" y="19" font-size="12" font-weight="600" fill="{colour}">'
            f"{html.escape(label)}</text>"
        )
    else:
        inner = (
            f'<text x="{width / 2:g}" y="19" text-anchor="middle" font-size="12" '
            f'font-weight="600" fill="{colour}">{html.escape(label)}</text>'
        )

    body = (
        '<g opacity="0"><animate attributeName="opacity" from="0" to="1" '
        'begin="0s" dur="0.5s" fill="freeze"/>'
        f'<g><animateTransform attributeName="transform" type="translate" '
        f'values="0 1.2;0 -1.2;0 1.2" calcMode="spline" '
        f'keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1" '
        f'dur="{duration:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
        f'<rect x="1" y="4" width="{width - 2}" height="22" rx="11" fill="{colour}" '
        f'fill-opacity="0.07" stroke="{colour}" stroke-width="1.3"/>{inner}</g></g>'
    )
    return svg(width, 30, label, body)


def label_chip(text, petal, centre):
    width = round(33 + len(text) * 7.4)
    body = (
        flower(14, 15, petal, centre, 14)
        + f'<text x="30" y="19" font-size="11" letter-spacing="1.2" fill="{GREY}">'
        + html.escape(text)
        + "</text>"
    )
    return svg(width, 30, text, body)


def guide(row_label, petal, centre, technologies):
    row_pitch = 54
    height = 44 + len(technologies) * row_pitch
    parts = [
        f'<rect x="1" y="1" width="858" height="{height - 2}" rx="14" fill="{petal}" '
        f'fill-opacity="0.05" stroke="{petal}" stroke-opacity="0.4" stroke-width="1.2"/>',
        flower(30, 24, centre, centre, 16),
        f'<text x="48" y="28" font-size="11" letter-spacing="1.5" fill="{GREY}">'
        f"{html.escape(row_label)}</text>",
    ]

    for index, (_, icon_slug, label, description) in enumerate(technologies):
        y = 46 + index * row_pitch
        colour = CHIP_COLOURS[index % len(CHIP_COLOURS)]
        glyph = icon_path(icon_slug)
        parts.append(
            f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" '
            f'begin="{0.15 + index * 0.08:.2f}s" dur="0.5s" fill="freeze"/>'
            f'<rect x="28" y="{y + 7}" width="32" height="32" rx="9" fill="{colour}" '
            f'fill-opacity="0.12"/>'
        )
        if glyph:
            parts.append(
                f'<g transform="translate(35,{y + 15}) scale(0.7)">'
                f'<path d="{glyph}" fill="{colour}"/></g>'
            )
        else:
            parts.append(
                f'<text x="44" y="{y + 29}" text-anchor="middle" font-size="15" '
                f'font-weight="700" fill="{colour}">{html.escape(label[0])}</text>'
            )
        parts.append(
            f'<text x="74" y="{y + 19}" font-size="14" font-weight="700" '
            f'fill="{colour}">{html.escape(label)}</text>'
        )
        lines = textwrap.wrap(description, width=86)
        if len(lines) > 2:
            raise ValueError(f"Description is too long for {label}: {description}")
        for line_index, line in enumerate(lines):
            parts.append(
                f'<text x="74" y="{y + 37 + line_index * 15}" font-size="12" '
                f'fill="{GREY}">{html.escape(line)}</text>'
            )
        if index < len(technologies) - 1:
            parts.append(
                f'<path d="M74 {y + 48}H828" stroke="{colour}" '
                f'stroke-opacity="0.18" stroke-width="1"/>'
            )
        parts.append("</g>")

    return svg(860, height, f"{row_label} field guide", "".join(parts))


def image_tag(filename, alt):
    digest = hashlib.sha1((OUTPUT / filename).read_bytes()).hexdigest()[:8]
    return f'<img src="chips/{filename}?v={digest}" alt="{html.escape(alt)}" />'


def readme_block():
    rows = []
    guides = []
    for row_index, (label, petal, centre, technologies) in enumerate(STACK):
        images = [image_tag(f"label-{row_index}.svg", label)]
        images.extend(image_tag(f"{slug}.svg", tech_label) for slug, _, tech_label, _ in technologies)
        rows.append(" ".join(images))
        guides.append(image_tag(f"guide-{row_index}.svg", f"{label} field guide") + "<br/>")

    return (
        '<div align="center">\n\n'
        + "\n<br/>\n".join(rows)
        + '\n\n<details>\n<summary><b>Field guide</b> - open to read the stack</summary>\n<br/>\n<div align="center">\n'
        + "\n".join(guides)
        + '\n</div>\n</details>\n\n</div>\n'
    )


def main():
    OUTPUT.mkdir(exist_ok=True)
    keep = set()
    for row_index, (label, petal, centre, technologies) in enumerate(STACK):
        for index, (slug, _, chip_label, _) in enumerate(technologies):
            colour = CHIP_COLOURS[index % len(CHIP_COLOURS)]
            (OUTPUT / f"{slug}.svg").write_text(chip(chip_label, technologies[index][1], colour), encoding="utf-8")
            keep.add(f"{slug}.svg")
        (OUTPUT / f"label-{row_index}.svg").write_text(label_chip(label, petal, centre), encoding="utf-8")
        (OUTPUT / f"guide-{row_index}.svg").write_text(guide(label, petal, centre, technologies), encoding="utf-8")
        keep.update({f"label-{row_index}.svg", f"guide-{row_index}.svg"})

    for stale in OUTPUT.glob("*.svg"):
        if stale.name not in keep:
            stale.unlink()

    readme = ROOT / "README.md"
    source = readme.read_text(encoding="utf-8")
    source = re.sub(
        r"<!-- TECH_GARDEN_START -->.*?<!-- TECH_GARDEN_END -->",
        lambda match: "<!-- TECH_GARDEN_START -->\n" + readme_block() + "<!-- TECH_GARDEN_END -->",
        source,
        flags=re.DOTALL,
    )
    readme.write_text(source, encoding="utf-8")
    print(f"Generated {len(keep)} SVG assets.")


if __name__ == "__main__":
    main()
