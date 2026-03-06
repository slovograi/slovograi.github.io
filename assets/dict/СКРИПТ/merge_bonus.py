import json
from pathlib import Path

BASE_DIR = Path(r"C:\Users\User\Desktop\СЛОВОГРАЙ2\assets\dict")
SCRIPT_DIR = BASE_DIR / "СКРИПТ"

BONUS_IN = BASE_DIR / "bonus.txt"
CORE_IN = BASE_DIR / "core.json"
HARD_IN = BASE_DIR / "hard.json"

BONUS_OUT = SCRIPT_DIR / "bonus1.txt"


def norm_word(w: str) -> str:
    return w.strip().upper()


def load_bonus_txt(path: Path) -> list[str]:
    words = []
    if not path.exists():
        raise FileNotFoundError(f"Not found: {path}")
    for line in path.read_text(encoding="utf-8").splitlines():
        w = line.strip()
        if not w:
            continue
        words.append(norm_word(w))
    return words


def load_json_words(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"Not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path.name} must be JSON array (list).")
    out = []
    for w in data:
        if isinstance(w, str):
            w = norm_word(w)
            if w:
                out.append(w)
    return out


def main():
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    bonus_words = load_bonus_txt(BONUS_IN)
    core_words = load_json_words(CORE_IN)
    hard_words = load_json_words(HARD_IN)

    bonus_set = set(bonus_words)

    # add only missing
    added = 0
    for w in core_words + hard_words:
        if w not in bonus_set:
            bonus_words.append(w)
            bonus_set.add(w)
            added += 1

    # optional: sort final output alphabetically
    final_words = sorted(bonus_set)

    BONUS_OUT.write_text("\n".join(final_words) + "\n", encoding="utf-8")

    print("OK")
    print(f"bonus.txt words: {len(set(load_bonus_txt(BONUS_IN)))}")
    print(f"core.json words: {len(set(core_words))}")
    print(f"hard.json words: {len(set(hard_words))}")
    print(f"Added from core+hard: {added}")
    print(f"Saved: {BONUS_OUT} (total {len(final_words)} words)")


if __name__ == "__main__":
    main()
