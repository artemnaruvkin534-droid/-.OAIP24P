import json
import os


class ProjectManager:
    def __init__(self):
        self.filename = 'projects.json'
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.projects = json.load(f)
        else:
            self.projects = []

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.projects, f, ensure_ascii=False, indent=2)

    def show_projects(self):
        if not self.projects:
            print("\nНет проектов")
            return
        print("\nПРОЕКТЫ:")
        for i, p in enumerate(self.projects, 1):
            print(f"{i}. {p['name']} - {p['status']} (задач: {len(p['tasks'])})")

    def create_project(self):
        name = input("Название проекта: ").strip()
        if not name:
            print("Ошибка: пустое название")
            return
        print("Статус: 1-план, 2-работа, 3-готов")
        status = {'1': 'планирование', '2': 'в работе', '3': 'готов'}.get(input("Выбор: "), 'планирование')

        self.projects.append({
            'name': name,
            'status': status,
            'tasks': []
        })
        self.save()
        print(f"Проект '{name}' создан")

    def add_task(self):
        if not self.projects:
            print("Сначала создайте проект")
            return
        self.show_projects()
        try:
            num = int(input("Номер проекта: ")) - 1
            task = input("Название задачи: ").strip()
            if task:
                self.projects[num]['tasks'].append({'name': task, 'status': 'новая'})
                self.save()
                print("Задача добавлена")
        except:
            print("Ошибка")

    def show_tasks(self):
        if not self.projects:
            print("Нет проектов")
            return
        self.show_projects()
        try:
            num = int(input("Номер проекта: ")) - 1
            tasks = self.projects[num]['tasks']
            if not tasks:
                print("Нет задач")
                return
            print(f"\nЗАДАЧИ В {self.projects[num]['name']}:")
            for i, t in enumerate(tasks, 1):
                print(f"{i}. {t['name']} - {t['status']}")
        except:
            print("Ошибка")

    def change_status(self):
        if not self.projects:
            print("Нет проектов")
            return
        self.show_projects()
        try:
            num = int(input("Номер проекта: ")) - 1
            print("Статус: 1-план, 2-работа, 3-готов")
            status = {'1': 'планирование', '2': 'в работе', '3': 'готов'}.get(input("Выбор: "))
            if status:
                self.projects[num]['status'] = status
                self.save()
                print("Статус обновлен")
        except:
            print("Ошибка")


def main():
    m = ProjectManager()
    while True:
        print("\n" + "=" * 30)
        print("МЕНЮ:")
        print("1. Проекты")
        print("2. Создать проект")
        print("3. Добавить задачу")
        print("4. Задачи проекта")
        print("5. Статус проекта")
        print("6. Выход")

        c = input("Выбор: ").strip()
        if c == '1':
            m.show_projects()
        elif c == '2':
            m.create_project()
        elif c == '3':
            m.add_task()
        elif c == '4':
            m.show_tasks()
        elif c == '5':
            m.change_status()
        elif c == '6':
            break


if __name__ == "__main__":
    main()