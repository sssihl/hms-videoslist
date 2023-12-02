<h1 align="center">
Aum Sri Sai Ram
</h1>

## About

This app records the output of a camera device and stores it in the windows server location with a database entry to keep track of which patient the video belongs to.

## Installation

1. Just run the following command to install all the required dependencies

```bash
pip install -r requirements.txt
```

2. rename the `.env.example` file to `.env` and fill in the options (contact Database Admin for setup)

```.env
# MYSQL credentials
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=username
MYSQL_PASSWORD=password@123
MYSQL_DATABASE=dbname
MYSQL_VIDEO_TABLE=rec_save_videos # don't change unless required
MYSQL_PATIENT_TABLE=rec_save_patients 
```
> ensure you don't give any space between variable name and value (e.g. `MYSQL_HOST = localhost` is invalid

3. in the `config.json` file set `"videoDevice"` variable to `0`,`1`,`2` (integer) experiment till it works. 

```json
{
    "windowsServer": "//BOOK",
    "videoDevice": 0,
    "videoTypes": [
        "OCT",
        "MRI",
        "CT"
    ],
    "width": 1280,
    "height": 720,
    "last_source": "MRI",
    "last_patient_id": "211219"
}
```
> These numbers (`0`,`1`,`2`...) represent the video devices connected to the system. In case of multiple devices, you will have to check which is the exact device that you want to record from.

4. Run the `main.py` file to **launch the application**

## Actions

- [x] POST: **Patient ID**
- [x] FETCH: Name Age Sex (to be displayed for validation)
- [x] INPUT: **Date of Visit**
- [x] INPUT: (select) **source of video output** (OCT/MRI/CT)
- [x] ACTIONS: (RECORD) (STOP) (SAVE)
- [x] DATABASE table


- [ ] ACTION: Copy to windows server

## Database Structure

### VIDEOS:
| ID | PATIENT_ID | VIDEO_TYPE | FILENAME | CREATED | DATE_OF_VISIT|
|---|---|---|---|---|---|
| INT (AUTO) | INT (UUID) | (OCT/CT/...) | (fullpath of file in windows server) |(DATETIME format) | (DATE format)

### PATIENTS
| ID | NAME | DOB | SEX |
|---|---|---|---|
| INT (UUID) | full name (STRING) | DATE | (MALE/FEMALE) |

## Folder Structure in server (for saving)

```
\\server\location
└── PATIENT_ID
    └── DATE_OF_VISIT
        ├── OCT001.mp4
        ├── OCT002.mp4
        ├── OCT003.mp4
        └── OCT004.mp4
    └── DATE_OF_VISIT
        ├── OCT005.mp4
        ├── OCT006.mp4
        ├── OCT007.mp4
        └── OCT008.mp4
└── PATIENT_ID
    └── DATE_OF_VISIT
        ├── MRI001.mp4
        ├── MRI002.mp4
        ├── MRI003.mp4
```

Syntax `\\server\location\PATIENT_ID\DATE_OF_VISIT\VIDEO_TYPE00x.mp4`
