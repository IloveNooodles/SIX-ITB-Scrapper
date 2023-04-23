import json


def main():
    data = open("data/cleaned.json", "r")
    data_json = json.load(data)
    data.close()
    parse_prodi(data_json)
    # for index, fakultas in enumerate(data_json):
    #   for prodi in data_json[fakultas]:
    #       print(prodi)


SQL_STR = f"INSERT INTO"


def parse_prodi(data):
    prodi_namaprodi = {}
    for index, fakultas in enumerate(data):
        for index, prodi in enumerate(data[fakultas]):
            list_data = data[fakultas][prodi]
            if not list_data:
                continue
            nama_prodi = list_data[0]['nama_prodi']
            kode_prodi = list_data[0]['kode_prodi']
            a = ""
            if kode_prodi.startswith("1"):
                nama_prodi = f"Sarjana - {nama_prodi}"
            elif kode_prodi.startswith("2"):
                nama_prodi = f"Magister - {nama_prodi}"
            elif kode_prodi.startswith("3"):
                nama_prodi = f"Doktor - {nama_prodi}"

            prodi_namaprodi[kode_prodi] = nama_prodi

    to_write = json.dumps(prodi_namaprodi)
    f = open("data/prodi.json", "w")
    f.write(to_write)
    f.close()


if __name__ == "__main__":
    main()
