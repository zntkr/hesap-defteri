import json
import os
from pathlib import Path
from typing import Any, Dict

_DEFAULTS: Dict[str, Any] = {"lang": "tr"}
_VALID: Dict[str, set] = {"lang": {"tr", "en"}}


def _path() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path.home() / ".config"
    return base / "HesapDefteri" / "settings.json"


def load() -> Dict[str, Any]:
    settings = dict(_DEFAULTS)
    try:
        with open(_path(), encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return settings
        for key, default in _DEFAULTS.items():
            val = data.get(key, default)
            settings[key] = val if key not in _VALID or val in _VALID[key] else default
    except (OSError, json.JSONDecodeError, ValueError):
        pass
    return settings


def save(settings: Dict[str, Any]) -> None:
    path = _path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        tmp.replace(path)  # aynı dosya sistemi → atomik işlem
    except OSError:
        pass
