"""Background music control for the game runtime."""

from pathlib import Path

import pygame


_MUSIC_READY = False
_MUSIC_PATH = None


def _resolve_music_path():
    """Return the first mp3 found under asset/mp3."""
    asset_dir = Path(__file__).resolve().parent.parent.parent / "asset" / "mp3"
    if not asset_dir.exists():
        return None

    mp3_files = sorted(asset_dir.glob("*.mp3"))
    return mp3_files[0] if mp3_files else None


def ensure_music_loaded():
    """Initialize the mixer and load music once if available."""
    global _MUSIC_READY, _MUSIC_PATH

    if _MUSIC_READY:
        return _MUSIC_PATH is not None

    _MUSIC_PATH = _resolve_music_path()
    if _MUSIC_PATH is None:
        _MUSIC_READY = True
        return False

    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        pygame.mixer.music.load(str(_MUSIC_PATH))
        _MUSIC_READY = True
        return True
    except (pygame.error, FileNotFoundError, OSError):
        _MUSIC_PATH = None
        _MUSIC_READY = True
        return False


def set_music_enabled(enabled, volume=0.75):
    """Start, pause, or stop the background music."""
    if not ensure_music_loaded():
        return

    safe_volume = max(0.0, min(1.0, volume))
    try:
        pygame.mixer.music.set_volume(safe_volume)
        if enabled:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
    except pygame.error:
        pass


def update_music_volume(volume):
    """Apply the current music volume if audio is available."""
    if not ensure_music_loaded():
        return

    try:
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
    except pygame.error:
        pass