# Подготовка к сдаче в Canvas — Task 2, Task 3 и SS10

**Исследование:** The Impact of Generative AI Tools on Employee Productivity and Work Quality in Knowledge-Based Office Tasks
**Команда:** Muratbek Ramazan / Tasbolatkyzy Zhanerke
**GitHub:** https://github.com/ramazanmuratbek-a11y/genai-productivity-benchmark

## 1. Что сдавать по Task 2

Подготовлен файл **`Task_2_Final_Updated_SS5_SS6_SS7.pdf`**, описывающий экспериментальный дизайн, fair baseline, гипотезы, метрики, проверяемость и техническое дополнение SS7. Если Canvas разрешает дополнительный текст/ссылку, приложите GitHub и укажите `docs/protocol.md`, `docs/evaluation_rubric.md`, `docs/task_sets.md`.

**Важно:** это *план эксперимента*; реальных участников пока не было. Уточняйте у преподавателя, действительно ли SS7 относится к Task 2 (в нашем проекте он оформлен как дополнительный блок).

## 2. Что сдавать по Task 3

Для отдельной загрузки подготовлен **`Task_3_Final_Submission_Report.pdf`**: цель, происхождение синтетических данных, схема анализа, таблицы, графики, ограничения и источники. Приложите ссылку на GitHub. Материалы, на которые можно сослаться в поле комментария Canvas:

- `docs/domain_model.md` — формулы и определения.
- `data/processed/metrics_summary.csv` — сводка демонстрационного сравнения задач (минуты).
- `data/processed/ss8_software_metrics_summary.csv` — сводка технических измерений (миллисекунды).
- `notebooks/01_data_analysis.ipynb`, `notebooks/02_ss8_software_log_analysis.ipynb` — выполняемые блокноты.
- `reports/figures/` — четыре графика, каждый в PNG и PDF.
- `src/process_data.py`, `src/process_ss7_logs.py`, `src/visualize.py`, `src/visualize_ss7_logs.py` — обработка/визуализация.
- `reports/paper_section_4.md` — воспроизводимый научный раздел Results & Discussion.
- `data/sample/ss7_software_benchmark_demo.jsonl` — открытые **синтетические** JSONL-логи.

`data/raw/test_run.jsonl` появляется локально после запуска `python src/collector.py --config configs/collector.yaml`, но по соображениям конфиденциальности **исключён из Git**. Если задание буквально требует raw JSONL в публичном репозитории, сначала обсудите с преподавателем безопасную публикацию исключительно синтетического материала.

**Числа не перепутать:** 4 вымышленные пары — время человека в минутах; 100 запусков программы — миллисекунды. Нельзя говорить, что работа с реальными сотрудниками завершена.

## 3. Что сдавать по SS10 / Overleaf

В Overleaf проект IEEE уже открыт и успешно скомпилирован. Скачайте **PDF именно из Overleaf**. Репозиторий содержит `overleaf/main.tex`, `overleaf/sections/`, `overleaf/references.bib`, `docs/SS10_OVERLEAF.md`.

Если SS10 сдаётся отдельно, приложите PDF или ZIP проекта в соответствии с конкретным заданием; **не добавляйте SS10 вместо Task 3**, если Canvas ожидает разные работы.

## 4. Проверка перед отправкой

Откройте в Canvas **каждое задание отдельно**: проверьте формат (PDF / MD / ZIP / ссылка), сроки и статус отправки. После загрузки откройте предпросмотр PDF, убедитесь, что файлы и имя команды указаны правильно, и только затем нажмите `Submit Assignment`.

После финального README-обновления желательно создать Git-тег на `main`, если преподаватель требует release:

```powershell
git switch main
git pull --ff-only origin main
git tag -a task3-final-2026 -m "Final research methods submission - synthetic demo"
git push origin task3-final-2026
```

Не создавайте тег второй раз, если он уже существует. Сначала убедитесь, что README-обновление **merged** и GitHub Actions на `main` зелёный.

## 5. Краткое объяснение преподавателю

**На английском:** "We designed a randomized counterbalanced crossover study of professional writing with and without GenAI. The human-study dataset is synthetic and contains four fictional paired participants; no real participants have been tested. We also built a separate reproducible SS7–SS8 software-runtime pipeline with 100 measured runs. The repository contains validation, uncertainty analysis, publication-quality figures, an IEEE Overleaf manuscript, 44 passing local tests and successful GitHub Actions. The reported demonstration figures are not empirical evidence of an AI productivity effect."
