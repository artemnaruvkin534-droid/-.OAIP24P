import json
med_db = {}
def add_patient(name, **data):
    pid = len(med_db) + 1
    med_db[pid] = {"name": name, **data}
    with open("patients.json", "w") as f:
        json.dump(med_db, f)
    print(f" {name} добавлен")
    return pid
add_patient("Анна", diagnosis="Грипп")
add_patient("Дмитрий", appointment="15.02.2024", doctor="Додепович")
add_patient("Мария", allergies=["пенициллин"], phone="+79991234567")
print("\nВсе пациенты:")
for pid, data in med_db.items():
    print(f"{pid}: {data}")