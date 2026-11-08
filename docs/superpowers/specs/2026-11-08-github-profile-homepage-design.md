# GitHub Profile Homepage Design

## Goal

Create the special profile repository `caiwei1030/caiwei1030` so its `README.md` appears on `https://github.com/caiwei1030`. The visual direction follows the dynamic garden profile made by `yuki4266`, adapted to Wei Cai's research and engineering interests while keeping maintenance simple.

## Page Structure

- Add a day/night-aware animated header using the living-scene visual system. It shows `Wei Cai` and the subtitle `Multi-agent systems, optimization, and language models`.
- Add a concise introduction describing Wei as a Software Engineering master's student at USTC and highlighting multi-agent systems, multi-objective optimization, deep learning, and LLM work.
- Add links to the personal website at `https://caiwei1030.github.io/` and GitHub at `https://github.com/caiwei1030`.
- Add four animated technology-chip groups:
  - AGENTS: Python, LangGraph, LangChain, Pydantic, FastAPI, Tool Safety.
  - AI / ML: PyTorch, Transformers, Deep Learning, LLM.
  - OPTIMIZATION: NSGA-II, Differential Evolution, K-means, Isolation Forest, Morris Analysis.
  - LEARNING: Transformer, BPE, RoPE, SwiGLU, AdamW.
- Include one compact collapsible field guide explaining the custom chip groups. Descriptions will be shorter than the reference profile.
- Add the contribution-grid snake animation generated from the repository owner's GitHub contributions.
- Add a day/night-aware seasonal garden footer and profile-view counter.

The design intentionally omits the streak card. This reduces external-service fragility while preserving the reference profile's strongest visual elements.

## Assets and Attribution

- Header and footer artwork will be derived from `yuki4266/living-scene-template`, which is part of the MIT-licensed `yuki4266/yuki4266` implementation.
- Keep visible attribution to `yuki4266/living-scene`.
- Include the applicable MIT copyright and permission notice in `LICENSE-ATTRIBUTION.md`.
- Generate technology chips locally as static SVG files so the rendered README does not depend on a badge service.

## Automation

- `scene.yml` updates weather and season every three hours and supports manual dispatch. Location is Hefei/USTC (`31.8205, 117.227`) with `Asia/Shanghai`.
- `snake.yml` runs on push, every twelve hours, and manually. It uses `Platane/snk/svg-only@v3` to publish the light and dark snake SVGs to an `output` branch.
- Both workflows use only the repository's built-in `GITHUB_TOKEN` and request contents-write permission.

## Validation

- Parse every generated SVG as XML.
- Validate all README image paths and alt text.
- Parse both workflow YAML files with SafeLoader.
- Confirm the snake workflow's owner is derived from `github.repository_owner`, not hard-coded.
- After publishing, verify the raw SVG URLs and confirm the README appears on the GitHub profile page.

## Publication

Create the public repository `caiwei1030/caiwei1030` without initializing remote files, push `main`, and manually trigger both workflows. If GitHub repository creation is unavailable from the local CLI session, provide the completed repository locally and request the user to create the empty remote repository.
