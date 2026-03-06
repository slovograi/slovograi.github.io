import json
from pathlib import Path
from collections import Counter

BASE_DIR = Path(r"C:\Users\User\Desktop\СЛОВОГРАЙ2\assets\dict")
SCRIPT_DIR = BASE_DIR / "СКРИПТ"

CORE_IN = BASE_DIR / "core.json"
HARD_IN = BASE_DIR / "hard.json"

CORE_OUT = SCRIPT_DIR / "core1.json"
HARD_OUT = SCRIPT_DIR / "hard1.json"
DUPES_OUT = SCRIPT_DIR / "dupes.txt"


def load_words(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path.name} must be JSON array (list).")
    # normalize: strip, uppercase, remove empty
    out = []
    for w in data:
        if not isinstance(w, str):
            continue
        w = w.strip()
        if not w:
            continue
        out.append(w.upper())
    return out


def save_words(path: Path, words: list[str]):
    # one word per line formatting
    txt = json.dumps(words, ensure_ascii=False, indent=2)
    path.write_text(txt + "\n", encoding="utf-8")


def main():
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    core_raw = load_words(CORE_IN)
    hard_raw = load_words(HARD_IN)

    # duplicates inside each file
    core_counts = Counter(core_raw)
    hard_counts = Counter(hard_raw)

    core_internal_dupes = sorted([w for w, c in core_counts.items() if c > 1])
    hard_internal_dupes = sorted([w for w, c in hard_counts.items() if c > 1])

    # unique lists (keep one)
    core_unique = sorted(set(core_raw))
    hard_unique = sorted(set(hard_raw))

    # duplicates between files (after internal cleanup)
    cross_dupes = sorted(set(core_unique) & set(hard_unique))

    # remove from hard all cross duplicates (keep in core)
    hard_final = sorted([w for w in hard_unique if w not in set(cross_dupes)])
    core_final = core_unique[:]  # keep everything

    # write outputs
    save_words(CORE_OUT, core_final)
    save_words(HARD_OUT, hard_final)

    # dupes report
    lines = []
    lines.append("=== DUPLICATES REPORT ===\n")
    lines.append(f"core.json total: {len(core_raw)}")
    lines.append(f"hard.json total: {len(hard_raw)}\n")

    lines.append(f"core.json internal duplicates ({len(core_internal_dupes)} unique words):")
    lines.extend([f"  {w} (x{core_counts[w]})" for w in core_internal_dupes] or ["  (none)"])
    lines.append("")

    lines.append(f"hard.json internal duplicates ({len(hard_internal_dupes)} unique words):")
    lines.extend([f"  {w} (x{hard_counts[w]})" for w in hard_internal_dupes] or ["  (none)"])
    lines.append("")

    lines.append(f"cross-file duplicates removed from hard.json ({len(cross_dupes)} words):")
    lines.extend([f"  {w}" for w in cross_dupes] or ["  (none)"])
    lines.append("")

    lines.append("=== OUTPUT ===")
    lines.append(f"core1.json words: {len(core_final)} -> {CORE_OUT}")
    lines.append(f"hard1.json words: {len(hard_final)} -> {HARD_OUT}")

    DUPES_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("OK")
    print("Saved:", CORE_OUT)
    print("Saved:", HARD_OUT)
    print("Saved:", DUPES_OUT)


if __name__ == "__main__":
    main()
