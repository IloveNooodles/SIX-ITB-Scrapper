# Six ITB Scrapper

This repository aims to get all of available matakuliah and dosen information from all of prodi and facutly in ITB for Dosen Rank Project. Built using python

## DISCLAIMER
I do not own the data. All of the data here are owned by ITB 

## library used

1. argparse
2. bs4
3. requests

## How to run

1. Clone this repository
2. create virtual environment from python `virtualenv venv`
3. install all requirements `pip install -r requirements.txt`
4. provide your `nim` and `cookie` from ITB sso service
   1. To get your cookie, you need to logged in in SIX
   2. Right click > `inspect` > `application`
   3. Grab the `khongguan` cookie from there

## How it works
1. To get all cleaned data, first is run the `scrape.py` to get all of available data in SIX ITB
2. The data then get cleaned by using `clean.py`
3. Cleaned data then get converted to `json` or `sql` using `output.py`

## Folder structure

```md
.
├── README.md
├── clean.py 
├── data
│   ├── cleaned.json
│   ├── dosen_id_name.json   
│   ├── dosen_matkul_map.json
│   ├── fakultas.json        
│   ├── fakultas_shorthand.json
│   ├── id_prodi_map.json
│   ├── matkul_dosen_map.json
│   ├── matkul_id_name.json
│   ├── prodi.json
│   └── saved.json
├── output.py
├── requirements.txt
├── scrape.py
└── sql
    ├── dosen.sql
    ├── fakultas.sql
    ├── matkul.sql
    ├── matkul_dosen.sql
    └── prodi.sql
```
