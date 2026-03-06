import json
from pathlib import Path

BASE_DIR = Path(r"C:\Users\User\Desktop\СЛОВОГРАЙ2\assets\dict")
SCRIPT_DIR = BASE_DIR / "СКРИПТ"

CORE_IN = BASE_DIR / "core.json"
HARD_IN = BASE_DIR / "hard.json"

CORE_OUT = SCRIPT_DIR / "core_sorted_len.json"
HARD_OUT = SCRIPT_DIR / "hard_sorted_len.json"


def norm_word(w: str) -> str:
    return w.strip().upper()


def load_json_list(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path.name} must be JSON array.")
    out = []
    for w in data:
        if isinstance(w, str):
            w = norm_word(w)
            if w:
                out.append(w)
    return out


def save_json_list(path: Path, words: list[str]):
    # красиве форматування: 1 слово = 1 рядок
    text = "[\n" + ",\n".join([f'  "{w}"' for w in words]) + "\n]\n"
    path.write_text(text, encoding="utf-8")


def sort_len_then_alpha(words: list[str]) -> list[str]:
    # прибрати дубль всередині файла
    uniq = sorted(set(words), key=lambda w: (len(w), w))
    return uniq


def main():
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    core_words = load_json_list(CORE_IN)
    hard_words = load_json_list(HARD_IN)

    core_sorted = sort_len_then_alpha(core_words)
    hard_sorted = sort_len_then_alpha(hard_words)

    save_json_list(CORE_OUT, core_sorted)
    save_json_list(HARD_OUT, hard_sorted)

    print("OK")
    print(f"core.json -> {CORE_OUT} ({len(core_sorted)} words)")
    print(f"hard.json -> {HARD_OUT} ({len(hard_sorted)} words)")


if __name__ == "__main__":
    main()
