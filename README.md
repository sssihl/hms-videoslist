Aum Sri Sai Ram

## Installation

1. Just run the following command to install all the required dependencies

```shell
pip install -r requirements.txt
```

2. rename the `.env.example` file to `.env` and fill in the options (contact Database Admin for setup)

3. in the `config.json` file set `"videoDevice"` variable to `0`,`1`,`2` (integer) experiment till it works. These numbers represent the video devices connected to the system. In case of multiple devices, you will have to check which is the exact device that you want to record from.

4. Run the `main.py` file

## Actions

[*] POST: **Patient ID**
[*] FETCH: Name Age Sex (to be displayed for validation)
[*] INPUT: **Date of Visit**
[*] INPUT: (select) **source of video output** (OCT/MRI/CT)
[*] ACTIONS: (RECORD) (STOP) (SAVE)
[*] DATABASE table
| Patient ID | Date | Video Type | Filename |
| ---------- | ------------- | ---------- | ------------------------------------ |
| (ID) | (Date format) | (OCT/CT) | (fullpath of file in windows server) |
[] ACTION: Copy to windows server
