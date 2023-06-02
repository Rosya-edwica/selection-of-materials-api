import psycopg2
import csv

def get_vuzes_from_csv() -> list[str]:
    vuzes: list[str] = []
    with open("неопознанные вузы.csv", mode="r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for index, item in enumerate(reader):
            if index == 0: continue
            vuzes.append(item[0])
    return vuzes


def get_vuzes_id_from_postgres(names: list[str]):
    ids: list[str] = []
    db = psycopg2.connect(user="edwica_root", password="9k35XQ&s", host="94.250.253.88", port=5432, database="education")
    cursor = db.cursor()
    query = ",".join(f"'{name}'" for name in names)
    q = f"""SELECT academkin_specialization.id, academkin_vuz.full_name, name, form, duration, level, profession, academkin_specialization.url
    FROM academkin_specialization
    LEFT JOIN academkin_vuz ON academkin_vuz.id = vuz_id
    WHERE academkin_vuz.full_name IN ({query})"""
    cursor.execute(q)
    result = [i for i in cursor.fetchall()]    
    db.close()
    return result


def save_result(result: list[list]):
    with open("result.csv", encoding="utf-8", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("spec_id", "vuz", "spec", "form", "duration", "level", "profession", "spec_url"))
        writer.writerows(result)
if __name__ == "__main__":
    vuzes = get_vuzes_from_csv()
    result = get_vuzes_id_from_postgres(vuzes)
    save_result(result)