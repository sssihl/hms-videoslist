Aum Sri Sai Ram

- ### GUI requirements

- POST: **Patient ID**
  - FETCH: Name Age Sex (to be displayed for validation)
- INPUT: **Date of Visit**
- INPUT: (select) **source of video output** (OCT/MRI/CT)
- ACTIONS: (RECORD) (STOP) (SAVE)
  - if you record, stop and save it gets saved
  - if you record stop and record again, the previous one gets discarded
  - save the records in a temp folder
- DATABASE table
  - | Patient ID | Date          | Video Type | Filename                             |
    | ---------- | ------------- | ---------- | ------------------------------------ |
    | (ID)       | (Date format) | (OCT/CT)   | (fullpath of file in windows server) |
-
