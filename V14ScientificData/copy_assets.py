from __future__ import annotations

import shutil
from pathlib import Path


def copy_assets(repo_root: Path, out_root: Path, list_path: Path) -> tuple[int, list[str]]:
    missing: list[str] = []
    copied = 0

    for raw in list_path.read_text(encoding="utf-8").splitlines():
        rel = raw.strip()
        if not rel:
            continue
        src = repo_root / rel
        dst = out_root / rel
        if not src.exists():
            missing.append(rel)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1

    return copied, missing


def main() -> None:
    out_root = Path(__file__).resolve().parent
    repo_root = out_root.parent

    v10_list = out_root / "_assets_from_v10.txt"
    if not v10_list.exists():
        raise SystemExit(f"Missing asset list: {v10_list}")

    copied, missing = copy_assets(repo_root=repo_root, out_root=out_root, list_path=v10_list)
    print(f"Copied {copied} assets from v10 list into {out_root.name}/")

    if missing:
        print("Missing assets (not copied):")
        for m in missing:
            print("-", m)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
