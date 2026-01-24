import os
from datetime import datetime


def analyze_logs():

    print("=" * 50)
    print("АНАЛИЗАТОР ЛОГ-ФАЙЛОВ")
    print("=" * 50)

    log_file = "server.log"
    report_file = "log_analysis_report.txt"
    error_log_file = "errors_only.log"

    if not os.path.exists(log_file):
        print(f"Файл '{log_file}' не найден. Создаю демо-логи...")
        create_demo_logs(log_file)

    print(f"\nЧитаю файл: {log_file}")

    total_lines = 0
    error_count = 0
    warning_count = 0
    ip_addresses = set()
    error_details = []

    try:
        with open(log_file, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                total_lines += 1

                if "ERROR" in line:
                    error_count += 1
                    error_details.append(f"Строка {line_num}: {line.strip()}")
                elif "WARNING" in line:
                    warning_count += 1

                if "IP:" in line:
                    start = line.find("IP: ") + 4
                    end = line.find(" ", start)
                    if start > 3:
                        ip = line[start:end] if end != -1 else line[start:]
                        ip_addresses.add(ip)

    except FileNotFoundError:
        print(f"Ошибка: Файл '{log_file}' не найден!")
        return
    except UnicodeDecodeError:
        print("Ошибка кодировки файла!")
        return

    print(f"\nСоздаю файл с ошибками: {error_log_file}")

    with open(log_file, 'r', encoding='utf-8') as source, \
            open(error_log_file, 'w', encoding='utf-8') as error_file:

        source.seek(0)

        for line in source:
            if "ERROR" in line:
                error_file.write(line)

    print(f"Создаю отчет: {report_file}")

    with open(report_file, 'w', encoding='utf-8') as report:
        report.write("=" * 50 + "\n")
        report.write("ОТЧЕТ АНАЛИЗА ЛОГ-ФАЙЛА\n")
        report.write(f"Сгенерирован: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write("=" * 50 + "\n\n")

        report.write(f"Анализируемый файл: {log_file}\n")
        report.write(f"Всего строк: {total_lines}\n")
        report.write(f"Ошибок (ERROR): {error_count}\n")
        report.write(f"Предупреждений (WARNING): {warning_count}\n")
        report.write(f"Уникальных IP-адресов: {len(ip_addresses)}\n\n")

        report.write("СПИСОК IP-АДРЕСОВ:\n")
        report.write("-" * 30 + "\n")
        for ip in sorted(ip_addresses):
            report.write(f"  {ip}\n")

        report.write("\nДЕТАЛИ ОШИБОК:\n")
        report.write("-" * 30 + "\n")
        if error_details:
            for error in error_details[:10]:
                report.write(f"{error}\n")
            if len(error_details) > 10:
                report.write(f"... и еще {len(error_details) - 10} ошибок\n")
        else:
            report.write("Ошибок не обнаружено\n")

    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА:")
    print("=" * 50)
    print(f"Всего строк проанализировано: {total_lines}")
    print(f"Найдено ошибок (ERROR): {error_count}")
    print(f"Найдено предупреждений (WARNING): {warning_count}")
    print(f"Уникальных IP-адресов: {len(ip_addresses)}")

    print(f"\nПервые 5 строк отчета из '{report_file}':")
    print("-" * 30)

    with open(report_file, 'r', encoding='utf-8') as report:
        for i, line in enumerate(report):
            if i < 5:
                print(line.rstrip())
            else:
                break

    print(f"\nОтчет сохранен в файле: {report_file}")
    print(f"Ошибки сохранены в файле: {error_log_file}")


def create_demo_logs(filename):

    demo_logs = [
        "2024-01-15 10:23:45 INFO: Сервер запущен. IP: 192.168.1.1\n",
        "2024-01-15 10:24:10 WARNING: Медленный ответ от базы данных\n",
        "2024-01-15 10:25:30 INFO: Пользователь вошел в систему. IP: 192.168.1.100\n",
        "2024-01-15 10:26:15 ERROR: Не удалось подключиться к внешнему API\n",
        "2024-01-15 10:27:45 INFO: Запрос обработан успешно. IP: 192.168.1.50\n",
        "2024-01-15 10:28:20 WARNING: Высокая загрузка CPU (85%)\n",
        "2024-01-15 10:29:05 INFO: Новый пользователь зарегистрирован. IP: 192.168.1.75\n",
        "2024-01-15 10:30:00 ERROR: Ошибка аутентификации пользователя\n",
        "2024-01-15 10:30:45 INFO: Резервное копирование завершено\n",
        "2024-01-15 10:31:30 ERROR: Диск почти заполнен (92%)\n",
        "2024-01-15 10:32:15 INFO: Отправлен email уведомление. IP: 192.168.1.100\n",
        "2024-01-15 10:33:00 WARNING: Высокое потребление памяти\n",
        "2024-01-15 10:33:45 INFO: Сессия пользователя завершена. IP: 192.168.1.1\n",
        "2024-01-15 10:34:30 ERROR: Сетевое соединение прервано\n",
        "2024-01-15 10:35:15 INFO: Кэш очищен\n",
    ]

    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(demo_logs)

    print(f"Создан демо-файл: {filename}")


def file_operations_demo():

    print("\n" + "=" * 50)
    print("ДОПОЛНИТЕЛЬНЫЕ ОПЕРАЦИИ С ФАЙЛАМИ")
    print("=" * 50)

    test_file = "test.txt"

    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("Первая строка\n")
        f.write("Вторая строка\n")
        print(f"Файл '{test_file}' создан и записан")

    with open(test_file, 'a', encoding='utf-8') as f:
        f.write("Третья строка (добавлена)\n")
        print(f"Добавлена строка в '{test_file}'")

    with open(test_file, 'r', encoding='utf-8') as f:
        print(f"\nСодержимое файла '{test_file}':")
        print("-" * 30)

        print("Метод read():")
        f.seek(0)
        content = f.read()
        print(content[:50] + "..." if len(content) > 50 else content)

        print("\nМетод readline():")
        f.seek(0)
        print(f"Первая строка: {f.readline().strip()}")

        print("\nМетод readlines():")
        f.seek(0)
        lines = f.readlines()
        print(f"Всего строк: {len(lines)}")

    os.remove(test_file)
    print(f"\nВременный файл '{test_file}' удален")

def main():
    print("ДЕМОНСТРАЦИЯ РАБОТЫ С ФАЙЛАМИ В PYTHON")

    analyze_logs()

    file_operations_demo()

    print("\n" + "=" * 50)
    print("ПРОГРАММА ЗАВЕРШЕНА")
    print("=" * 50)


if __name__ == "__main__":
    main()