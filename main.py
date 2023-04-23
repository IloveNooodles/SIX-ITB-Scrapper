import argparse
import json
from typing import List

import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(
    prog="SIX Parser",
    description="Parse matakuliah, dosen, and sks in SIX",
)
parser.add_argument('-n', '--nim',
                    help="Your nim in ITB",
                    type=str,
                    required=True
                    )

parser.add_argument('-c', '--cookie',
                    help="Your cookie auth in your browser",
                    type=str,
                    required=True
                    )

args = parser.parse_args()
NIM = args.nim
"""
Your NIM in ITB
"""

BASE_URL = f"https://akademik.itb.ac.id/app/K/mahasiswa:{NIM}+2022-2/kelas/jadwal/kuliah"
"""
BASE URL for the scrapping
"""


HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
    "User-agent": "Bot",
    "upgrade-insecure-requests": "1",
}
"""
Accepted Header for the page 
"""


COOKIE_VAL = args.cookie
"""
COOKIE_VAL is your auth cookie in the browser 
"""

COOKIE = {"khongguan": COOKIE_VAL, "nissin": "ina"}
"""
COOKIE is the needed cookie in order to get the result\n
"khongguan" is cookie we got from SSO \n
"nissin" is language we used\n
"""


class MatkulDosens:
    """
    Object representation of matakuliah and dosen instance
    """

    def __init__(self, list_dosen: List[str], kode_matkul: str, nama_matkul: str, sks: str, fakultas: str, prodi: str) -> None:
        self.list_dosen = list_dosen
        self.kode_matkul = kode_matkul
        self.nama_matkul = nama_matkul
        self.sks = sks
        self.fakultas = fakultas
        self.kode_prodi = prodi[0]
        self.nama_prodi = prodi[1]

    def __str__(self) -> str:
        return f"Dosen: {str(self.list_dosen)}\nkode_matkul: {self.kode_matkul}\nnama_matkul: {self.nama_matkul}\nsks: {self.sks}\nfakultas: {self.fakultas}\nkode prodi: {self.kode_prodi}\nnama prodi: {self.nama_prodi}"

    def to_obj(self) -> dict:
        return {
            "list_dosen": self.list_dosen,
            "kode_matkul": self.kode_matkul,
            "nama_matkul": self.nama_matkul,
            "fakultas": self.fakultas,
            "kode_prodi": self.kode_prodi,
            "nama_prodi": self.nama_prodi,
            "sks": self.sks
        }


def create_params(fakultas: str, prodi: int) -> str:
    """
    To create query params for search
    """
    params = f"?fakultas={fakultas}&prodi={prodi}&pekan=&kegiatan="
    return params


def main():
    res = {}
    list_fakultas = get_all_fakultas()
    for fakultas in list_fakultas:
        list_prodi = get_prodi_by_fakultas(fakultas)
        res[fakultas] = {}
        for prodi in list_prodi:
            result = get_dosen_matkul_by_fakultas_prodi(fakultas, prodi)
            res[fakultas][prodi[0]] = result
            print(f"Finish scrapped {fakultas} - {prodi[0]} - {prodi[1]}")
        print(f"Finish scrapped {fakultas}")

    saved = json.dumps(res)
    f = open("saved.json", "w")
    f.write(saved)
    f.close()


def get_all_fakultas() -> List[str]:
    """
    Get all available fakultas in ITB
    """
    r = requests.get(BASE_URL, headers=HEADERS, cookies=COOKIE)
    bs = BeautifulSoup(r.content, "html.parser")
    list_fakultas = bs.find("select", {"id": "fakultas"})
    list_fakultas_string = []
    for fakultas in list_fakultas:
        val = fakultas['value']
        if val == "":
            continue
        list_fakultas_string.append(fakultas['value'])

    return list_fakultas_string


def get_prodi_by_fakultas(fakultas: str) -> List[str]:
    """
    Get all prodi from fakultas in ITB
    """
    URL = f"{BASE_URL}?fakultas={fakultas}"
    r = requests.get(URL, headers=HEADERS, cookies=COOKIE)
    bs = BeautifulSoup(r.content, "html.parser")
    prodi_element = bs.find("select", {"id": "prodi"})
    list_prodi = prodi_element.find_all("option")
    list_prodi_string = []
    for prodi in list_prodi:
        val = prodi['value']
        if val == "":
            continue

        to_add = [prodi['value'], prodi.text.strip().split(" - ")[1]]
        list_prodi_string.append(to_add)

    return list_prodi_string


def get_dosen_matkul_by_fakultas_prodi(fakultas, prodi):
    """
    Get all available dosen and matkul given fakultas and prodi in ITB
    """
    URL = f"{BASE_URL}{create_params(fakultas, prodi[0])}"
    r = requests.get(URL, headers=HEADERS, cookies=COOKIE)
    bs = BeautifulSoup(r.content, "html.parser")
    dosen_matkul = bs.find_all("tr")

    arr_of_matkul_dosens = []

    for element in dosen_matkul:
        dosen = element.find("ul", class_="list-unstyled")
        sks = element.find("td", class_="text-center")

        if dosen is None or sks is None:
            continue

        list_nama_dosen = [x.text.strip() for x in dosen.find_all("li")]

        matkul = sks.find_previous_sibling("td")
        kode_matkul = matkul.find_previous_sibling("td")

        matkulDosen = MatkulDosens(
            list_nama_dosen, kode_matkul.text.strip(), matkul.text.strip(), sks.text.strip(), fakultas, prodi)

        arr_of_matkul_dosens.append(matkulDosen.to_obj())

    return arr_of_matkul_dosens


if __name__ == "__main__":
    main()