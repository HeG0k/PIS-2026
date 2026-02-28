# 🚀 Quick Start Guide - Лабораторная работа №1

Быстрый старт для выполнения лабораторной работы "Сценарий транзакции".

---

## ✅ Шаг 1: Проверьте установленные инструменты

Откройте PowerShell/Terminal и выполните:

```powershell
# Проверка Git
git --version
# Ожидается: git version 2.x.x или выше

# Проверка Java (для PlantUML)
java -version
# Ожидается: java version "17.x.x" или выше
```

### ❌ Если что-то не установлено:

**Git не найден?**
- Скачать: https://git-scm.com/download/win
- После установки перезапустите PowerShell

**Java не найден?**
- Скачать OpenJDK: https://adoptium.net/
- Выберите: JRE 17 LTS (или новее)
- После установки перезапустите PowerShell

---

## ✅ Шаг 2: Создайте fork и клонируйте репозиторий

### 1. Создайте fork репозитория на GitHub

1. Откройте в браузере: https://github.com/brstu/PIS-2026
2. Нажмите кнопку **Fork** в правом верхнем углу
3. Выберите свой аккаунт GitHub
4. Дождитесь создания копии репозитория в вашем аккаунте

**Результат:** У вас появится репозиторий `https://github.com/ваш-username/PIS-2026`

### 2. Клонируйте СВОЙ fork

```powershell
# Создайте папку для лабораторных (если ещё нет)
mkdir C:\University\PIS
cd C:\University\PIS

# Клонируйте СВОЙ fork (замените ваш-username на ваш логин GitHub)
git clone https://github.com/ваш-username/PIS-2026.git

# Перейдите в папку лабораторной №1
cd PIS-2026\labs\01_transaction_scenario
```

**⚠️ Важно:** Клонируйте именно СВОЙ fork, а не оригинальный репозиторий brstu/PIS-2026!

### 3. Настройте upstream (для получения обновлений)

```powershell
# Добавьте оригинальный репозиторий как upstream
git remote add upstream https://github.com/brstu/PIS-2026.git

# Проверьте настройку
git remote -v
# Должно быть:
# origin    https://github.com/ваш-username/PIS-2026.git (fetch)
# origin    https://github.com/ваш-username/PIS-2026.git (push)
# upstream  https://github.com/brstu/PIS-2026.git (fetch)
# upstream  https://github.com/brstu/PIS-2026.git (push)
```

---

## ✅ Шаг 3: Установите плагины VS Code

Откройте VS Code и установите расширения:

1. **PlantUML** (для диаграмм)
   - `Ctrl+Shift+X` → найти "PlantUML"
   - Установить расширение от **jebbs**
   - ID: `jebbs.plantuml`

2. **Cucumber (Gherkin) Full Support** (для `.feature` файлов)
   - `Ctrl+Shift+X` → найти "Cucumber"
   - Установить "Cucumber (Gherkin) Full Support"
   - ID: `alexkrechik.cucumberautocomplete`

3. **Markdown All in One** (для отчётов)
   - `Ctrl+Shift+X` → найти "Markdown All in One"
   - Установить от **Yu Zhang**
   - ID: `yzhang.markdown-all-in-one`

---

## ✅ Шаг 4: Проверьте примеры

```powershell
# Откройте папку в VS Code
code .

# Откройте файл с диаграммой
code examples\diagrams\sequence-happy.puml
```

**В VS Code:**
1. Откройте файл `examples/diagrams/sequence-happy.puml`
2. Нажмите `Alt+D` для предпросмотра
3. Должна отобразиться диаграмма последовательности

**✅ Если диаграмма видна - всё настроено правильно!**

**❌ Если диаграмма не видна:**
- Проверьте, что Java установлена: `java -version`
- Перезагрузите VS Code
- Проверьте, что плагин PlantUML установлен: `Ctrl+Shift+X` → "PlantUML"

---

## ✅ Шаг 5: Изучите примеры

Откройте и изучите готовые примеры:

### 📄 Use-case описание
```powershell
code examples\use-case.md
```
Пример детального описания бизнес-сценария.

### 🧪 Gherkin-сценарии
```powershell
code examples\scenarios.feature
```
14 сценариев тестирования (успешные + ошибочные).

### 📊 Анализ транзакций
```powershell
code examples\analysis.md
```
Таблицы транзакционных границ и обработка ошибок.

### 🎨 Диаграммы
```powershell
code examples\diagrams\sequence-happy.puml
code examples\diagrams\sequence-error-notification.puml
```
PlantUML диаграммы для успешного сценария и error case.

---

## ✅ Шаг 6: Выберите свой вариант

```powershell
# Откройте файл с вариантами
code ..\..\ВАРИАНТЫ_ЛАБОРАТОРНЫХ.md
```

Выберите один из 40 вариантов предметных областей (например, #7 «Фитнес-треккер "Прокач мозг"»).

---

## ✅ Шаг 7: Создайте свой отчёт

### Создайте папку для вашей работы:

```powershell
# Вернитесь в корень репозитория (если вы в папке labs)
cd ..\..

# Создайте ветку для вашей работы (замените на свои данные)
git checkout -b lab01-group123-ivanov

# Создайте папку для вашей работы (замените Ivanov_Ivan на свою фамилию и имя)
mkdir students\Ivanov_Ivan\lab-01
cd students\Ivanov_Ivan\lab-01
```

**⚠️ Важно:** 
- Название ветки: `lab01-группа-фамилия` (латиницей, строчными буквами)
- Папка студента: `Фамилия_Имя` (с заглавной буквы, кириллицей или латиницей)

### Скопируйте макет отчёта:

```powershell
# Скопируйте макет
copy ..\..\..\labs\01_transaction_scenario\Макет_отчета.md Отчет.md

# Создайте структуру файлов
mkdir diagrams
New-Item use-case.md -ItemType File
New-Item scenarios.feature -ItemType File
New-Item analysis.md -ItemType File
```

### Откройте в VS Code:

```powershell
code .
```

---

## ✅ Шаг 8: Заполните отчёт и отправьте на проверку

### Заполните все файлы:

1. Откройте `Отчет.md`
2. Замените все плейсхолдеры `<...>` и `[...]` на свои данные
3. Создайте `use-case.md` по примеру
4. Создайте `scenarios.feature` с Gherkin-сценариями
5. Создайте диаграммы `.puml` в папке `diagrams/`
6. Заполните `analysis.md` с транзакционными границами
7. Экспортируйте диаграммы в PNG

### Зафиксируйте изменения:

```powershell
# Добавьте все файлы
git add .

# Сделайте commit
git commit -m "feat: add lab-01 report for Ivanov Ivan"

# Отправьте в СВОЙ fork
git push origin lab01-group123-ivanov
```

### Создайте Pull Request:

1. Откройте СВОЙ fork на GitHub: `https://github.com/ваш-username/PIS-2026`
2. Нажмите кнопку **Compare & pull request**
3. Заполните описание PR:
   - **Заголовок:** `[Lab-01] Фамилия Имя, Группа`
   - **Описание:** Кратко опишите, что выполнено
4. Нажмите **Create pull request**
5. Дождитесь проверки преподавателем

**✅ Готово!** Ваша работа отправлена на проверку.

---

## 📚 Полезные команды VS Code

| Команда | Действие |
|---------|----------|
| `Alt+D` | Предпросмотр PlantUML диаграммы |
| `Ctrl+Shift+P` → "PlantUML: Export" | Экспорт диаграммы в PNG |
| `Ctrl+Shift+V` | Предпросмотр Markdown |
| `Ctrl+K V` | Открыть Markdown preview рядом |
| `Ctrl+Space` | Автодополнение в Gherkin |

---

## 🆘 Частые проблемы

### Проблема: Забыл сделать fork, уже клонировал brstu/PIS-2026

**Решение:**
```powershell
# Удалите неправильный клон
cd ..
rm -rf PIS-2026

# Вернитесь к Шагу 2 и сделайте fork, затем клонируйте СВОЙ fork
```

### Проблема: Нет доступа к GitHub / нет аккаунта

**Решение:**
1. Создайте аккаунт на GitHub: https://github.com/signup
2. Подтвердите email
3. Вернитесь к Шагу 2

### Проблема: PlantUML не показывает диаграммы

**Решение:**
1. Проверьте Java: `java -version`
2. Перезагрузите VS Code
3. Попробуйте онлайн: https://www.plantuml.com/plantuml/uml/

### Проблема: Gherkin без подсветки

**Решение:**
1. Убедитесь, что файл имеет расширение `.feature`
2. Установите плагин Cucumber: `Ctrl+Shift+X` → "Cucumber"

### Проблема: Не могу экспортировать PNG

**Решение:**
1. `Ctrl+Shift+P` → "PlantUML: Export Current Diagram"
2. Выберите формат PNG
3. Файл создастся в той же папке, где `.puml`

### Проблема: git push выдаёт ошибку "permission denied"

**Решение:**
1. Убедитесь, что вы клонировали СВОЙ fork, а не brstu/PIS-2026
2. Проверьте: `git remote -v` - должен быть `origin` с вашим username
3. Если неправильно:
   ```powershell
   git remote set-url origin https://github.com/ваш-username/PIS-2026.git
   ```

---

## 📞 Где получить помощь?

- **Примеры:** [examples/](examples/) - готовые артефакты
- **Инструкция:** [README.md](README.md) - полное описание лабораторной
- **Макет отчёта:** [Макет_отчета.md](Макет_отчета.md) - что заполнить

---

## ✨ Готово к работе?

Если вы прошли все шаги и примеры открываются корректно - можете начинать выполнение лабораторной работы! 🚀

**Удачи! 💪**
