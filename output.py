import json


def main():
    data = open("data/cleaned.json", "r")
    data_json = json.load(data)
    data.close()
    parse_fakultas(data_json)
    # for index, fakultas in enumerate(data_json):
    #   for prodi in data_json[fakultas]:
    #       print(prodi)


def parse_fakultas(data):
    f = open("data/fakultas_shorthand.json", "r")
    fakutlas_shorthand_map_json = json.load(f)
    f.close()
    print(fakutlas_shorthand_map_json)

    f = open("data/fakultas.json", "r")
    fakultas_map = json.load(f)
    f.close()
    print(fakultas_map)

    to_write = f'insert into public.faculties (id, institution_id, "name", code) values '
    ctr = 1
    for fakultas in data:
        try:
            kode_fakultas = fakutlas_shorthand_map_json[fakultas]
            for kode in kode_fakultas:
                to_write += f"({ctr}, 1, '{fakultas_map[kode]}', {int(kode)}),\n"
                ctr += 1
        except KeyError:
            pass
    
    sql_statement = to_write[:-2] + ';'
    f = open("sql/fakultas.sql", "w")
    f.write(sql_statement)
    f.close()


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


def parse_prodi_to_sql(data):
    prodi_namaprodi = {}
    SQL_STR = f"INSERT INTO"
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
