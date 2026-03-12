# John — 桌面整理工具 (Desktop Organizer)

自動將桌面上的檔案依照類型分類到子資料夾，讓桌面保持整齊。

Automatically sorts files on your Desktop into categorized sub-folders, keeping your Desktop tidy.

## 使用方法 (Usage)

### 基本用法 — 整理預設桌面 (Organize default Desktop)

```bash
python organize_desktop.py
```

### 指定資料夾 (Specify a folder)

```bash
python organize_desktop.py /path/to/folder
```

### 預覽模式，不實際移動檔案 (Dry-run — preview without moving files)

```bash
python organize_desktop.py --dry-run
python organize_desktop.py /path/to/folder --dry-run
```

## 分類規則 (Categories)

| 資料夾名稱 | 副檔名 |
|---|---|
| 圖片 (Images) | .jpg .jpeg .png .gif .bmp .svg .webp .tiff .ico .heic .raw |
| 影片 (Videos) | .mp4 .mkv .avi .mov .wmv .flv .webm .m4v .mpeg .mpg .3gp |
| 音樂 (Music) | .mp3 .wav .flac .aac .ogg .wma .m4a .opus .aiff |
| 文件 (Documents) | .pdf .doc .docx .xls .xlsx .ppt .pptx .txt .odt .ods .odp .rtf .csv .md |
| 壓縮檔 (Archives) | .zip .rar .7z .tar .gz .bz2 .xz |
| 程式 (Programs) | .exe .msi .dmg .pkg .deb .rpm .app .apk .sh .bat .cmd |
| 程式碼 (Code) | .py .js .ts .html .css .java .c .cpp .h .cs .go .rs .php .rb .swift .kt .json .xml .yaml .yml .toml .ini .cfg |
| 字型 (Fonts) | .ttf .otf .woff .woff2 .eot |
| 其他 (Others) | 其他所有副檔名 |

無法識別副檔名的檔案會被移至「其他 (Others)」資料夾。  
隱藏檔案（以 `.` 開頭）及資料夾本身不會被移動。

## 需求 (Requirements)

- Python 3.6+
- 標準函式庫（無需安裝額外套件）

## 授權 (License)

MIT