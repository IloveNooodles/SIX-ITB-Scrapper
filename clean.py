import json

DATA = None


def main():
    """
    removed unavailable matakuliah
    """
    f = open("saved.json", "r")
    data = json.load(f)
    f.close()

    new_data = {}
    for fakultas in data:
        new_data[fakultas] = {}
        for prodi in data[fakultas]:
            list_matkul_dosen = data[fakultas][prodi]
            to_add = []
            for matkul_dosen in list_matkul_dosen:
                list_dosen = matkul_dosen["list_dosen"]
                found_empty = False
                for dosen in list_dosen:
                    if "\n" in dosen:
                        found_empty = True
                        break

                if not found_empty:
                    to_add.append(matkul_dosen)

            new_data[fakultas][prodi] = to_add

    clean_data = json.dumps(new_data)
    cleaned_data = open("data/cleaned.json", "w")
    cleaned_data.write(clean_data)
    cleaned_data.close()


if __name__ == "__main__":
    main()
