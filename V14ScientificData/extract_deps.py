from __future__ import annotations

import re
from pathlib import Path


def collect_includegraphics(tex: str) -> list[str]:
    pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
    return sorted({m.group(1).strip() for m in pattern.finditer(tex)})


def collect_bibliography(tex: str) -> list[str]:
    pattern = re.compile(r"\\bibliography\{([^}]+)\}")
    bibs: set[str] = set()
    for m in pattern.finditer(tex):
        for part in m.group(1).split(","):
            part = part.strip()
            if part:
                bibs.add(part)
    return sorted(bibs)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    v10_path = repo_root / "main_englishv10_final.tex"
    v13_path = repo_root / "V13ScientificData" / "main_english_v13_final.tex"

    v10_tex = v10_path.read_text(encoding="utf-8", errors="ignore")
    v13_tex = v13_path.read_text(encoding="utf-8", errors="ignore")

    v10_assets = collect_includegraphics(v10_tex)
    v13_assets = collect_includegraphics(v13_tex)

    v10_bibs = collect_bibliography(v10_tex)
    v13_bibs = collect_bibliography(v13_tex)

    outdir = repo_root / "V14ScientificData"
    outdir.mkdir(exist_ok=True)

    (outdir / "_assets_from_v10.txt").write_text("\n".join(v10_assets) + "\n", encoding="utf-8")
    (outdir / "_assets_from_v13_final.txt").write_text("\n".join(v13_assets) + "\n", encoding="utf-8")
    (outdir / "_bibfiles_from_v10.txt").write_text("\n".join(v10_bibs) + "\n", encoding="utf-8")
    (outdir / "_bibfiles_from_v13_final.txt").write_text("\n".join(v13_bibs) + "\n", encoding="utf-8")

    print(f"v10 includegraphics: {len(v10_assets)}")
    print(f"v13_final includegraphics: {len(v13_assets)}")
    print(f"v10 bibliography files: {v10_bibs}")
    print(f"v13 bibliography files: {v13_bibs}")
    print("\nFirst 20 v10 assets:")
    for a in v10_assets[:20]:
        print("-", a)
    print("\nFirst 20 v13 assets:")
    for a in v13_assets[:20]:
        print("-", a)


if __name__ == "__main__":
    main()
