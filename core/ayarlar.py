import json
import os
from pathlib import Path
from typing import Any, Dict

_DEFAULTS: Dict[str, Any] = {"lang": "tr", "ui_scale": 1.0, "theme": "light"}
_VALID: Dict[str, set] = {"lang": {"tr", "en"}, "ui_scale": {1.0, 1.15, 1.25, 1.5}, "theme": {"light", "dark"}}


def app_dir() -> Path:
    """Uygulamaya ait kullanıcı veri klasörünü döner (settings + log buraya gider)."""
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    return base / "HesapDefteri"


def _path() -> Path:
    return app_dir() / "settings.json"


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
