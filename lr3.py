import uuid
from enum import Enum

# --- 1. Перелічувані типи (Enum) ---
class Priority(Enum):
    LOW = "Низький"
    MEDIUM = "Середній"
    HIGH = "Високий"

class Status(Enum):
    TODO = "До виконання"
    IN_PROGRESS = "В процесі"
    DONE = "Виконано"


# --- 2. Базовий клас ---
class Task:
    def __init__(self, title: str, base_time: int, priority: Priority):
        self._id = str(uuid.uuid4())[:8]
        self.title = title
        self.base_time = base_time
        self.priority = priority
        self.status = Status.TODO

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Назва завдання не може бути порожньою!")
        self._title = value.strip()

    @property
    def base_time(self) -> int:
        return self._base_time

    @base_time.setter
    def base_time(self, value: int):
        if value <= 0:
            raise ValueError("Базовий час має бути більше 0!")
        self._base_time = value

    # Базовий метод, який буде поліморфно перевизначено
    def calculate_time(self) -> int:
        return self.base_time

    def get_info(self) -> str:
        return f"[{self._id}] {self.title} | {self.priority.value} | Статус: {self.status.value} | Запланований час: {self.calculate_time()} год."


# --- 3. Класи-нащадки (Наслідування та Поліморфізм) ---
class DevelopmentTask(Task):
    def __init__(self, title: str, base_time: int, priority: Priority, language: str):
        super().__init__(title, base_time, priority)
        self.language = language

    def get_info(self) -> str:
        return super().get_info() + f" | [Розробка] Мова: {self.language}"


class BugTask(Task):
    def __init__(self, title: str, base_time: int, priority: Priority, severity: int):
        # Архітектурний краш-тест
        if severity < 1:
            raise ValueError("Рівень критичності багу не може бути меншим за 1!")
        
        super().__init__(title, base_time, priority)
        self.severity = severity

    # Поліморфізм: множимо час на критичність
    def calculate_time(self) -> int:
        return self.base_time * self.severity

    def get_info(self) -> str:
        return super().get_info() + f" | [Баг] Критичність: x{self.severity}"


class TestingTask(Task):
    def __init__(self, title: str, base_time: int, priority: Priority, setup_time: int):
        super().__init__(title, base_time, priority)
        self.setup_time = setup_time

    # Поліморфізм: додаємо час на налаштування
    def calculate_time(self) -> int:
        return self.base_time + self.setup_time

    def get_info(self) -> str:
        return super().get_info() + f" | [Тестування] +{self.setup_time} год. налаштування"


# --- 4. Клас-менеджер (Композиція) ---
class ProjectManager:
    def __init__(self):
        self._tasks = []

    def add_task(self, task: Task):
        self._tasks.append(task)
        print(f"Додано до проєкту: {task.title}")

    def show_all(self):
        print("\n--- Всі завдання проєкту ---")
        for t in self._tasks:
            # Викликається метод get_info(), який працює по-різному залежно від типу об'єкта
            print(t.get_info())


# --- 5. Блок демонстрації (Запуск програми) ---
if __name__ == "__main__":
    manager = ProjectManager()

    try:
        # Вхідні дані створюються одразу в коді для швидкого тестування
        t1 = DevelopmentTask("Створити API авторизації", 10, Priority.HIGH, "Python")
        t2 = TestingTask("Інтеграційне тестування API", 4, Priority.MEDIUM, 2)
        t3 = BugTask("Помилка 500 при логіні", 3, Priority.HIGH, 3)

        manager.add_task(t1)
        manager.add_task(t2)
        manager.add_task(t3)

        manager.show_all()

        print("\n[Краш-тест] Спроба створити баг з нульовою критичністю...")
        t4 = BugTask("Мінорний візуальний баг", 2, Priority.LOW, 0)

    except ValueError as e:
        print(f"[ValueError перехоплено]: {e}")
    except Exception as e:
        print(f"[Помилка]: {e}")