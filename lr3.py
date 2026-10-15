from dataclasses import dataclass
from enum import Enum
import uuid


class TaskPriority(Enum):
    LOW = "Низький"
    MEDIUM = "Середній"
    HIGH = "Високий"
    CRITICAL = "Критичний"


class TaskStatus(Enum):
    TODO = "До виконання"
    IN_PROGRESS = "У роботі"
    DONE = "Виконано"


@dataclass
class Employee:
    full_name: str
    position: str


@dataclass
class Project:
    project_name: str
    client_name: str


class Task:
    def __init__(self, title: str, employee: Employee, priority: TaskPriority, status: TaskStatus, base_hours: float):
        self._id = str(uuid.uuid4())[:8]
        self.title = title
        self.employee = employee
        self.priority = priority
        self.status = status
        self.base_hours = base_hours

    @property
    def task_id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Назва завдання повинна бути текстовим рядком!")
        if not value.strip():
            raise ValueError("Назва завдання не може бути порожнім рядком!")
        self._title = value.strip()

    @property
    def base_hours(self) -> float:
        return self._base_hours

    @base_hours.setter
    def base_hours(self, value: float):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("Базова оцінка часу повинна бути числом!")
        if value <= 0:
            raise ValueError("Базова оцінка часу має бути строго більшою за 0!")
        self._base_hours = float(value)

    def estimate_effort(self) -> float:
        return self._base_hours

    def format_details(self) -> str:
        return (
            f"Завдання [{self._id}] | Назва: {self._title} | Виконавець: {self.employee.full_name} ({self.employee.position}) | "
            f"Пріоритет: {self.priority.value} | Статус: {self.status.value} | Трудовитрати: {self.estimate_effort()} год"
        )


class DevelopmentTask(Task):
    def __init__(
        self, title: str, employee: Employee, priority: TaskPriority,
        status: TaskStatus, base_hours: float, modules_count: int
    ):
        super().__init__(title, employee, priority, status, base_hours)
        self.modules_count = modules_count

    @property
    def modules_count(self) -> int:
        return self._modules_count

    @modules_count.setter
    def modules_count(self, value: int):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("Кількість модулів повинна бути цілим числом!")
        if value <= 0:
            raise ValueError("Кількість модулів має бути більшою за 0!")
        self._modules_count = value

    def estimate_effort(self) -> float:
        return round(self.base_hours * self._modules_count + 2.0, 2)

    def format_details(self) -> str:
        return f"[Розробка] {super().format_details()} | Модулів: {self._modules_count}"


class BugTask(Task):
    def __init__(
        self, title: str, employee: Employee, priority: TaskPriority,
        status: TaskStatus, base_hours: float, severity_level: int
    ):
        super().__init__(title, employee, priority, status, base_hours)
        self.severity_level = severity_level

    @property
    def severity_level(self) -> int:
        return self._severity_level

    @severity_level.setter
    def severity_level(self, value: int):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("Рівень критичності повинен бути цілим числом!")
        if value < 1 or value > 5:
            raise ValueError("Рівень критичності має бути в діапазоні від 1 до 5!")
        self._severity_level = value

    def estimate_effort(self) -> float:
        return round(self.base_hours + (self._severity_level * 1.5), 2)

    def format_details(self) -> str:
        return f"[Дефект] {super().format_details()} | Рівень критичності: {self._severity_level}"


class TestingTask(Task):
    def __init__(
        self, title: str,
        employee: Employee,
        priority: TaskPriority,
        status: TaskStatus,
        base_hours: float,
        test_cases_count: int,
    ):
        super().__init__(title, employee, priority, status, base_hours)
        self.test_cases_count = test_cases_count

    @property
    def test_cases_count(self) -> int:
        return self._test_cases_count

    @test_cases_count.setter
    def test_cases_count(self, value: int):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("Кількість тест-кейсів повинна бути цілим числом!")
        if value <= 0:
            raise ValueError("Кількість тест-кейсів має бути більшою за 0!")
        self._test_cases_count = value

    def estimate_effort(self) -> float:
        return round(self.base_hours + (self._test_cases_count * 0.25), 2)

    def format_details(self) -> str:
        return f"[Тестування] {super().format_details()} | Тест-кейсів: {self._test_cases_count}"


class ProjectManager:
    def __init__(self, project: Project):
        self.project = project
        self._tasks: list[Task] = []

    def register_task(self, task: Task):
        self._tasks.append(task)
        print(f"\n[Успіх] Завдання зареєстровано: {task.format_details()}")

    def calculate_total_project_effort(self) -> float:
        total_effort = 0.0
        for task in self._tasks:
            total_effort += task.estimate_effort()
        return round(total_effort, 2)

    def display_project_board(self):
        print("\n" + "=" * 75)
        print(f"ПРОЄКТ: {self.project.project_name} | ЗАМОВНИК: {self.project.client_name}")
        print("=" * 75)
        if not self._tasks:
            print("Дошка завдань проєкту наразі порожня.")
        else:
            for task in self._tasks:
                print(task.format_details())
            print("-" * 75)
            total = self.calculate_total_project_effort()
            print(f"Загальні розрахункові трудовитрати за проєктом: {total} год")
        print("=" * 75)


def select_priority() -> TaskPriority:
    print("Оберіть пріоритет (1 - Низький, 2 - Середній, 3 - Високий, 4 - Критичний):")
    p_choice = input("Ваш вибір (1-4): ").strip()
    mapping = {
        "1": TaskPriority.LOW, "2": TaskPriority.MEDIUM,
        "3": TaskPriority.HIGH, "4": TaskPriority.CRITICAL,
    }
    return mapping.get(p_choice, TaskPriority.MEDIUM)


def select_status() -> TaskStatus:
    print("Оберіть статус (1 - До виконання, 2 - У роботі, 3 - Виконано):")
    s_choice = input("Ваш вибір (1-3): ").strip()
    mapping = {"1": TaskStatus.TODO, "2": TaskStatus.IN_PROGRESS, "3": TaskStatus.DONE}
    return mapping.get(s_choice, TaskStatus.TODO)


if __name__ == "__main__":
    print("=== Система управління завданнями проєкту ===")
    current_project = Project("CRM Cloud Platform", "ТОВ ІнфоТех")
    manager = ProjectManager(current_project)

    while True:
        print("\nМеню управління проєктом:")
        print("1. Додати DevelopmentTask")
        print("2. Додати BugTask")
        print("3. Додати TestingTask")
        print("4. Показати всі завдання та загальні трудовитрати проєкту")
        print("5. Вийти з програми")
        choice = input("Ваш вибір (1-5): ").strip()

        try:
            if choice in ("1", "2", "3"):
                title = input("Назва завдання: ").strip()
                emp_name = input("ПІБ виконавця: ").strip()
                emp_pos = input("Посада виконавця: ").strip()
                base_hours = float(input("Базова оцінка часу (год): "))
                priority = select_priority()
                status = select_status()
                employee = Employee(full_name=emp_name, position=emp_pos)

                if choice == "1":
                    modules = int(input("Кількість програмних модулів: "))
                    task = DevelopmentTask(title, employee, priority, status, base_hours, modules)
                elif choice == "2":
                    severity = int(input("Рівень критичності дефекту (1-5): "))
                    task = BugTask(title, employee, priority, status, base_hours, severity)
                else:
                    cases = int(input("Кількість тест-кейсів: "))
                    task = TestingTask(title, employee, priority, status, base_hours, cases)
                manager.register_task(task)
            elif choice == "4":
                manager.display_project_board()
            elif choice == "5":
                print("Завершення роботи програми.")
                break
            else:
                print("[Помилка] Некоректний пункт меню. Введіть число від 1 до 5.")
        except (ValueError, TypeError) as error:
            print(f"\n[Помилка валідації або введення даних]: {error}")
        except Exception as error:
            print(f"\n[Непередбачувана помилка]: {error}")
