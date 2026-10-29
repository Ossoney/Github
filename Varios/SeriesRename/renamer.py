import re
import urllib.parse
import urllib.request
import json
from pathlib import Path
from typing import Optional, Tuple, Dict

VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.m4v', '.flv'}

# Cache to avoid repeated network lookups for the same show
_EPISODES_CACHE: Dict[str, Dict[Tuple[int, int], str]] = {}

def sanitize_filename(name: str) -> str:
    """Removes or replaces characters forbidden in Windows filenames."""
    forbidden = r'[\/:*?"<>|]'
    clean = re.sub(forbidden, '', name)
    return clean.strip()

def parse_filename(filename: str, folder_hint: str = "") -> Optional[Tuple[str, int, int]]:
    """
    Attempts to extract (show_name, season, episode) from filename.
    Supports formats like:
      - Ted Lasso - Temporada 1 [Cap.101] -> S=1, E=1
      - Ted Lasso - Temporada 3 [Cap.310] -> S=3, E=10
      - Serie.S01E05...
      - Serie 1x02...
    """
    stem = Path(filename).stem

    # Pattern 1: Temporada X ... Cap. XYY or Cap.YY
    # e.g., Temporada 1 [Hdtv][Cap.101] or [Cap. 102]
    m_cap = re.search(r'(?:Temporada\s*(\d+))?.*?(?:Cap(?:itulo|\.)?\s*(\d+))', stem, re.IGNORECASE)
    if m_cap:
        temp_str, cap_str = m_cap.groups()
        cap_num = int(cap_str)
        if temp_str:
            season = int(temp_str)
            # If cap_num is like 101, 102, 212:
            if cap_num >= 100:
                episode = cap_num % 100
            else:
                episode = cap_num
        else:
            if cap_num >= 100:
                season = cap_num // 100
                episode = cap_num % 100
            else:
                season = 1
                episode = cap_num
        
        # Extract show name from before "Temporada" or "Cap"
        show_match = re.split(r'[-_]?\s*(?:Temporada|Cap|\[)', stem, flags=re.IGNORECASE)
        show_name = show_match[0].strip(' -_') if show_match else ""
        if not show_name and folder_hint:
            show_name = folder_hint
        return sanitize_filename(show_name), season, episode

    # Pattern 2: S01E02 or s1e2
    m_se = re.search(r's(\d+)\s*e(\d+)', stem, re.IGNORECASE)
    if m_se:
        season = int(m_se.group(1))
        episode = int(m_se.group(2))
        show_match = re.split(r's\d+\s*e\d+', stem, flags=re.IGNORECASE)
        show_name = show_match[0].strip(' .-_')
        if not show_name and folder_hint:
            show_name = folder_hint
        return sanitize_filename(show_name), season, episode

    # Pattern 3: 1x02 or 01x02
    m_x = re.search(r'(?:^|[\s._-])(\d{1,2})x(\d{1,2})(?:[\s._-]|$)', stem, re.IGNORECASE)
    if m_x:
        season = int(m_x.group(1))
        episode = int(m_x.group(2))
        idx = m_x.start(1)
        show_name = stem[:idx].strip(' .-_')
        if not show_name and folder_hint:
            show_name = folder_hint
        return sanitize_filename(show_name), season, episode

    return None

def fetch_episode_titles(show_name: str) -> Dict[Tuple[int, int], str]:
    """
    Fetches episode list from TVmaze API.
    Returns mapping: (season, episode) -> title
    """
    if show_name.lower() in _EPISODES_CACHE:
        return _EPISODES_CACHE[show_name.lower()]

    mapping = {}
    try:
        url = f"https://api.tvmaze.com/singlesearch/shows?q={urllib.parse.quote(show_name)}&embed=episodes"
        req = urllib.request.Request(url, headers={'User-Agent': 'SeriesRename/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                episodes = data.get('_embedded', {}).get('episodes', [])
                for ep in episodes:
                    s = ep.get('season')
                    e = ep.get('number')
                    name = ep.get('name')
                    if s is not None and e is not None and name:
                        mapping[(s, e)] = sanitize_filename(name)
    except Exception as e:
        print(f"Error fetching metadata for {show_name}: {e}")

    _EPISODES_CACHE[show_name.lower()] = mapping
    return mapping

def generate_new_name(filepath: Path, show_override: str = "", fetch_titles: bool = True) -> Optional[str]:
    """Generates the new name in format '1x01 Nombre Serie - Nombre Episodio.ext'"""
    if filepath.suffix.lower() not in VIDEO_EXTENSIONS:
        return None

    folder_hint = filepath.parent.name
    parsed = parse_filename(filepath.name, folder_hint=folder_hint)
    if not parsed:
        return None

    raw_show, season, episode = parsed
    show_name = show_override.strip() if show_override.strip() else (raw_show or folder_hint)

    ep_title = ""
    if fetch_titles and show_name:
        titles_map = fetch_episode_titles(show_name)
        ep_title = titles_map.get((season, episode), "")

    # Format: 1x01 Nombre Serie - Nombre Episodio.ext
    # or: 1x01 Nombre Serie.ext (if no episode title found)
    if ep_title:
        new_stem = f"{season}x{episode:02d} {show_name} - {ep_title}"
    else:
        new_stem = f"{season}x{episode:02d} {show_name}"

    return f"{new_stem}{filepath.suffix}"
