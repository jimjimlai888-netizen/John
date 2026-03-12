#!/usr/bin/env python3
"""
organize_desktop.py - 自動整理桌面檔案 (Auto-organize desktop files)

Usage:
    python organize_desktop.py [desktop_path]

If no path is provided, the script will use the current user's Desktop folder.
"""

import shutil
import sys
from pathlib import Path

# File type categories and their extensions
FILE_CATEGORIES = {
    "圖片 (Images)": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp",
        ".tiff", ".tif", ".ico", ".heic", ".raw",
    ],
    "影片 (Videos)": [
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
        ".m4v", ".mpeg", ".mpg", ".3gp",
    ],
    "音樂 (Music)": [
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
        ".opus", ".aiff",
    ],
    "文件 (Documents)": [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".txt", ".odt", ".ods", ".odp", ".rtf", ".csv", ".md",
    ],
    "壓縮檔 (Archives)": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
        ".tar.gz", ".tar.bz2", ".tar.xz",
    ],
    "程式 (Programs)": [
        ".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".app",
        ".apk", ".sh", ".bat", ".cmd",
    ],
    "程式碼 (Code)": [
        ".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp",
        ".h", ".cs", ".go", ".rs", ".php", ".rb", ".swift", ".kt",
        ".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ],
    "字型 (Fonts)": [
        ".ttf", ".otf", ".woff", ".woff2", ".eot",
    ],
}


def get_category(file_extension: str) -> str:
    """Return the category name for a given file extension."""
    ext = file_extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "其他 (Others)"


def get_file_extension(path: Path) -> str:
    """
    Return the full extension of a file, including compound extensions.

    For example, ``archive.tar.gz`` returns ``".tar.gz"`` instead of just ``".gz"``.
    """
    suffixes = path.suffixes
    if len(suffixes) >= 2:
        compound = "".join(suffixes[-2:]).lower()
        # Check if the compound extension is explicitly listed
        for extensions in FILE_CATEGORIES.values():
            if compound in extensions:
                return compound
    return path.suffix


def get_desktop_path() -> Path:
    """Return the default desktop path for the current user."""
    home = Path.home()
    # Support both Windows and Unix-like systems
    candidates = [
        home / "Desktop",
        home / "桌面",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    # Fall back to home directory if Desktop is not found
    return home


def organize(desktop_path: Path, dry_run: bool = False) -> dict:
    """
    Organize files on the desktop into categorized subdirectories.

    Args:
        desktop_path: Path to the desktop directory.
        dry_run: If True, only print actions without moving files.

    Returns:
        A dict mapping category names to lists of moved file paths.
    """
    if not desktop_path.exists():
        raise FileNotFoundError(f"目錄不存在: {desktop_path}")

    moved: dict[str, list[str]] = {}

    for item in sorted(desktop_path.iterdir()):
        # Skip directories and hidden files
        if item.is_dir() or item.name.startswith("."):
            continue

        category = get_category(get_file_extension(item))
        target_dir = desktop_path / category

        if not dry_run:
            target_dir.mkdir(exist_ok=True)

        target_path = target_dir / item.name

        # Avoid overwriting existing files
        if target_path.exists():
            stem = item.stem
            suffix = item.suffix
            counter = 1
            while target_path.exists():
                target_path = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

        print(f"{'[預覽] ' if dry_run else ''}移動: {item.name} → {category}/")
        if not dry_run:
            shutil.move(str(item), str(target_path))

        moved.setdefault(category, []).append(str(target_path))

    return moved


def print_summary(moved: dict) -> None:
    """Print a summary of all moved files."""
    if not moved:
        print("桌面已整齊，沒有需要移動的檔案。")
        return

    total = sum(len(files) for files in moved.values())
    print(f"\n整理完成！共移動 {total} 個檔案：")
    for category, files in sorted(moved.items()):
        print(f"  {category}: {len(files)} 個檔案")


def main() -> None:
    """Entry point for the script."""
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    paths = [a for a in args if not a.startswith("--")]

    if paths:
        desktop_path = Path(paths[0]).expanduser().resolve()
    else:
        desktop_path = get_desktop_path()

    print(f"整理桌面: {desktop_path}")
    if dry_run:
        print("(預覽模式 - 不會實際移動檔案)\n")

    try:
        moved = organize(desktop_path, dry_run=dry_run)
        print_summary(moved)
    except FileNotFoundError as exc:
        print(f"錯誤: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
