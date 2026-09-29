
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.db")

START_STUDENTS = [
    ("Иванов Иван", "ИСП-101", 5, 18),
    ("Петров Пётр", "ИСП-101", 4, 19),
    ("Сидоров Алексей", "ИСП-102", 3, 20),
    ("Смирнова Анна", "ИСП-102", 5, 18),
    ("Кузнецов Максим", "ИСП-101", 4, 21),
]

def init_db(conn):
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT    NOT NULL,
            group_name TEXT    NOT NULL,
            grade      INTEGER NOT NULL
        )
        """
    )

    cursor.execute("PRAGMA table_info(students)")
    columns = [row[1] for row in cursor.fetchall()]
    if "age" not in columns:
        cursor.execute("ALTER TABLE students ADD COLUMN age INTEGER")

    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        for name, group_name, grade, age in START_STUDENTS:
            cursor.execute(
                "INSERT INTO students (name, group_name, grade, age) "
                "VALUES (?, ?, ?, ?)",
                (name, group_name, grade, age),
            )
    conn.commit()

    cursor.execute("UPDATE students SET age = 18 WHERE age IS NULL")
    conn.commit()

def print_students(rows):
    """Красиво выводит список студентов в виде таблицы."""
    if not rows:
        print("Студенты не найдены.")
        return
    print(f"{'ID':<4}{'ФИО':<22}{'Группа':<10}{'Оценка':<8}{'Возраст':<8}")
    print("-" * 52)
    for student_id, name, group_name, grade, age in rows:
        print(f"{student_id:<4}{name:<22}{group_name:<10}{grade:<8}{age:<8}")


def select_all(cursor):
    cursor.execute(
        "SELECT id, name, group_name, grade, age FROM students ORDER BY id"
    )
    return cursor.fetchall()

def input_int(prompt, min_value=None, max_value=None):
    while True:
        text = input(prompt).strip()
        try:
            value = int(text)
        except ValueError:
            print("Ошибка: нужно ввести целое число.")
            continue
        if min_value is not None and value < min_value:
            print(f"Ошибка: значение не может быть меньше {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Ошибка: значение не может быть больше {max_value}.")
            continue
        return value


def input_text(prompt):
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Ошибка: строка не должна быть пустой.")

def show_all(conn):
    cursor = conn.cursor()
    print_students(select_all(cursor))


def add_student(conn):
    cursor = conn.cursor()
    name = input_text("ФИО студента: ")
    group_name = input_text("Группа: ")
    grade = input_int("Оценка (1-5): ", 1, 5)
    age = input_int("Возраст: ", 14, 100)
    cursor.execute(
        "INSERT INTO students (name, group_name, grade, age) VALUES (?, ?, ?, ?)",
        (name, group_name, grade, age),
    )
    conn.commit()
    print(f"Студент добавлен (ID = {cursor.lastrowid}).")


def find_by_group(conn):
    cursor = conn.cursor()
    group_name = input_text("Введите название группы: ")
    cursor.execute(
        "SELECT id, name, group_name, grade, age FROM students "
        "WHERE group_name = ? ORDER BY id",
        (group_name,),
    )
    print_students(cursor.fetchall())


def find_by_grade(conn):
    cursor = conn.cursor()
    grade = input_int("Введите оценку (1-5): ", 1, 5)
    cursor.execute(
        "SELECT id, name, group_name, grade, age FROM students "
        "WHERE grade = ? ORDER BY id",
        (grade,),
    )
    print_students(cursor.fetchall())


def student_exists(cursor, student_id):
    cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
    return cursor.fetchone() is not None


def update_grade(conn):
    cursor = conn.cursor()
    student_id = input_int("Введите ID студента: ")
    if not student_exists(cursor, student_id):
        print(f"Студент с ID {student_id} не найден.")
        return
    new_grade = input_int("Введите новую оценку (1-5): ", 1, 5)
    cursor.execute(
        "UPDATE students SET grade = ? WHERE id = ?", (new_grade, student_id)
    )
    conn.commit()
    print("Оценка изменена.")


def delete_student(conn):
    cursor = conn.cursor()
    student_id = input_int("Введите ID студента для удаления: ")
    if not student_exists(cursor, student_id):
        print(f"Студент с ID {student_id} не найден.")
        return
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    print("Студент удалён. Оставшиеся студенты:")
    print_students(select_all(cursor))

def older_than(conn):
    cursor = conn.cursor()
    age = input_int("Показать студентов старше (лет): ", 0, 100)
    cursor.execute(
        "SELECT id, name, group_name, grade, age FROM students "
        "WHERE age > ? ORDER BY age DESC, id",
        (age,),
    )
    print_students(cursor.fetchall())


def average_grade(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(grade) FROM students")
    avg = cursor.fetchone()[0]
    if avg is None:
        print("В таблице нет студентов.")
    else:
        print(f"Средняя оценка всех студентов: {avg:.2f}")


def count_by_group(conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT group_name, COUNT(*) FROM students GROUP BY group_name "
        "ORDER BY group_name"
    )
    rows = cursor.fetchall()
    if not rows:
        print("В таблице нет студентов.")
        return
    for group_name, count in rows:
        print(f"{group_name}: {count} студ.")


def best_student(conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, group_name, grade, age FROM students "
        "WHERE grade = (SELECT MAX(grade) FROM students) ORDER BY id"
    )
    print_students(cursor.fetchall())

MENU = """
===== УЧЁТ СТУДЕНТОВ =====
1. Показать всех студентов
2. Добавить студента
3. Найти студентов по группе
4. Найти студентов по оценке
5. Изменить оценку
6. Удалить студента
--- Дополнительно ---
7. Студенты старше указанного возраста
8. Средняя оценка всех студентов
9. Количество студентов в каждой группе
10. Студент(ы) с самой высокой оценкой
0. Выход"""

ACTIONS = {
    "1": show_all,
    "2": add_student,
    "3": find_by_group,
    "4": find_by_grade,
    "5": update_grade,
    "6": delete_student,
    "7": older_than,
    "8": average_grade,
    "9": count_by_group,
    "10": best_student,
}


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        init_db(conn)
        while True:
            print(MENU)
            try:
                choice = input("Выберите пункт меню: ").strip()
            except EOFError: 
                break
            if choice == "0":
                print("До свидания!")
                break
            action = ACTIONS.get(choice)
            if action is None:
                print("Неверный пункт меню. Введите число от 0 до 10.")
                continue
            print()
            action(conn)
    finally:
        conn.close() 


if __name__ == "__main__":
    main()
