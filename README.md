<h1 align="center">
Aum Sri Sai Ram
</h1>

# About

This app records the output of a camera device and stores it in the windows server location with a database entry to keep track of which patient the video belongs to.

> [!CAUTION]
> **DO NOT USE IT FOR THE LIVE ENVIRONMENT YET!**
> 
> The app doesn't have the "COPYING to the SERVER" logic, so it is only for preview as of now. The database and the rest work

# Installation steps

1. Just run the following command to install all the required dependencies

```console
pip install -r requirements.txt
```

2. Run the `migrations/videos_table.sql` in `mysql to generate the videos table which will be used to save information about the videos and their location

> [!IMPORTANT]  
> At this point, depending on whether you have an existing `patients_table` you will have choose between the following

- **I don't have an existing `patients_table`**
  > If you don't have a `patients_table` in your database, then create one by running `migrations/patients_table.sql` file in mysql to generate the table

- **I have an existing `patients_table` called `my_patients_table`**
  > If you have an existing `my_patients_table` that you want to use with the application, you have to do two things.

  Update your `.env` variable to set the `MYSQL_PATIENT_TABLE`
  ```.env
  ...
  MYSQL_PATIENT_TABLE=my_patients_table
  ```

  Update your `config.json` with the correct field names from the patient's table (say, they are `myid`, `myname`, `mydob`, `mysex`)
  ```json
  {
    ...previous entries
  
    "patient_table_args": {
      "id": "myid",
      "name": "myname",
      "date_of_birth": "mydob",
      "sex": "mysex"
     }
  }
  ```

  
  

3. rename the `.env.example` file to `.env` and fill in the options (contact Database Admin for setup)

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

4. in the `config.json` file set `"videoDevice"` variable to `0`,`1`,`2` (integer) experiment till it works. 

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

5. Run the `main.py` file to **launch the application**

# Actions

:heavy_check_mark: `GET`: **Patient ID**

:heavy_check_mark: `FETCH`: Name Age Sex (to be displayed for validation) 

:heavy_check_mark: `INPUT`: Date of Visit

- [ ] `FEATURE`: Date Picker (currently, user has to type in the date)

:heavy_check_mark: `INPUT`: (select) **source of video output** (OCT/MRI/CT)

:heavy_check_mark: `ACTIONS`: (RECORD) (STOP) (SAVE)

:heavy_check_mark: `STRUCTURE` DATABASE table


- [ ] `ACTION`: Copy to windows server

# Database Structure

### VIDEOS:
| ID | PATIENT_ID | VIDEO_TYPE | FILENAME | CREATED | DATE_OF_VISIT|
|---|---|---|---|---|---|
| INT (AUTO) | INT (UUID) | (OCT/CT/...) | (fullpath of file in windows server) |(DATETIME format) | (DATE format)

### PATIENTS
| ID | NAME | DOB | SEX |
|---|---|---|---|
| INT (UUID) | full name (STRING) | DATE | (MALE/FEMALE) |

# Folder Structure in server (for saving)

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
