import json


def main():
    data = open("data/cleaned.json", "r")
    data_json = json.load(data)
    data.close()
    parse_dosen_matkul(data_json)
    # for index, fakultas in enumerate(data_json):
    #   for prodi in data_json[fakultas]:
    #       print(prodi)


def parse_dosen_matkul(data):
    list_all_dosen = {}
    list_all_matkul = {}
    for index, fakultas in enumerate(data):
        for index, prodi in enumerate(data[fakultas]):
            list_data = data[fakultas][prodi]
            for dosen_matkul in list_data:
                nama_matkul = dosen_matkul['nama_matkul']
                kode_matkul = dosen_matkul['kode_matkul']
                nama_prodi = dosen_matkul['nama_prodi']
                kode_prodi = dosen_matkul['kode_prodi']
                sks = dosen_matkul['sks']

                if kode_prodi.startswith("1"):
                    nama_prodi = f"Sarjana - {nama_prodi}"
                elif kode_prodi.startswith("2"):
                    nama_prodi = f"Magister - {nama_prodi}"
                elif kode_prodi.startswith("3"):
                    nama_prodi = f"Doktor - {nama_prodi}"
                # Dosen
                for dosen in dosen_matkul['list_dosen']:
                    if dosen not in list_all_dosen.keys():
                        list_all_dosen[dosen] = {}
                        list_all_dosen[dosen]['list_matkul'] = set()
                        list_all_dosen[dosen]['kode_prodi'] = kode_prodi
                        list_all_dosen[dosen]['nama_prodi'] = nama_prodi
                        list_all_dosen[dosen]['list_matkul'].add(nama_matkul)
                    else:
                        list_all_dosen[dosen]['list_matkul'].add(nama_matkul)

                    # Matkul
                    if nama_matkul not in list_all_matkul.keys():
                        list_all_matkul[nama_matkul] = {}
                        list_all_matkul[nama_matkul]['sks'] = sks
                        list_all_matkul[nama_matkul]['kode_matkul'] = kode_matkul
                        list_all_matkul[nama_matkul]['kode_prodi'] = kode_prodi
                        list_all_matkul[nama_matkul]['nama_prodi'] = nama_prodi
                        list_all_matkul[nama_matkul]["list_dosen"] = set()
                        list_all_matkul[nama_matkul]["list_dosen"].add(dosen)
                    else:
                        list_all_matkul[nama_matkul]["list_dosen"].add(dosen)
    # Dosen
    for dosen in list_all_dosen:
        list_all_dosen[dosen]['list_matkul'] = list(
            list_all_dosen[dosen]['list_matkul'])

    to_write = json.dumps(list_all_dosen)
    f = open("data/dosen_matkul_map.json", "w")
    f.write(to_write)
    f.close()

    for matkul in list_all_matkul:
        list_all_matkul[matkul]['list_dosen'] = list(
            list_all_matkul[matkul]['list_dosen'])

    # Matkul
    to_write = json.dumps(list_all_matkul)
    f = open("data/matkul_dosen_map.json", "w")
    f.write(to_write)
    f.close()


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


FAKULTAS_MAPPING = {
    "FMIPA": 1,
    "SITH": [2, 3],
    "SF": 4,
    "FITB": 5,
    "STEI": 6,
    "FTTM": 7,
    "FTSL": 8,
    "FTI": 9,
    "FTMD": 10,
    "SAPPK": 11,
    "FSRD": 12,
    "SBM": 13
}


def parse_prodi_to_sql(data):
    sql_statement = f'insert into public.majors (id, faculty_id, "name", code) values '
    ctr = 1
    id_prodi_map = {}
    for fakultas in data:
        for prodi in data[fakultas]:
            list_data = data[fakultas][prodi]
            if not list_data:
                continue
            nama_prodi = list_data[0]['nama_prodi']
            kode_prodi = list_data[0]['kode_prodi']
            try:
                faculty_id = FAKULTAS_MAPPING[fakultas]
            except:
                continue
            if fakultas == "SITH":
                if "Rekayasa" in nama_prodi:
                    faculty_id = faculty_id[1]
                else:
                    faculty_id = faculty_id[0]

            if kode_prodi.startswith("1"):
                nama_prodi = f"Sarjana - {nama_prodi}"
            elif kode_prodi.startswith("2"):
                nama_prodi = f"Magister - {nama_prodi}"
            elif kode_prodi.startswith("3"):
                nama_prodi = f"Doktor - {nama_prodi}"

            sql_statement += f"({ctr}, {faculty_id}, '{nama_prodi}', {kode_prodi}),\n"
            id_prodi_map[kode_prodi] = ctr
            ctr += 1

    # id_prodi = json.dumps(id_prodi_map)
    sql_statement = sql_statement[:-2] + ';'
    f = open("data/prodi.sql", "w")
    f.write(sql_statement)
    f.close()


if __name__ == "__main__":
    main()
