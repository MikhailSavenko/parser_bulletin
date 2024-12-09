### Название проекта: **Парсер результатов торгов СПбМТСБ**

---

### Описание проекта  
Этот проект реализован в рамках стажировки и представляет собой учебное задание. С помощью библиотеки Scrapy создан парсер, который скачивает и обрабатывает бюллетени с результатами торгов с сайта [СПбМТСБ](https://spimex.com/markets/oil_products/trades/results/) начиная с 2023 года. Полученные данные сохраняются в базу данных для последующего анализа.  

Парсер извлекает из таблицы бюллетеня только данные с единицей измерения *"Метрическая тонна"*, где в столбце **"Количество Договоров, шт."** значение больше 0.  

---

### Используемые технологии и библиотеки  
- **Python**  
- **Scrapy==2.12.0** — для работы с веб-скрапингом.  
- **xlrd==2.0.1** — для чтения Excel-файлов.  
- **pandas==2.2.3** — для обработки табличных данных.  
- **sqlalchemy==2.0.36** — для работы с базой данных.  

---

### Функциональность  
Парсер:  
1. Скачивает бюллетени торгов с сайта СПбМТСБ.  
2. Извлекает данные из таблицы *"Единица измерения: Метрическая тонна"*, где **"Количество Договоров, шт."** > 0.  
3. Обрабатывает следующие столбцы:  
   - **Код Инструмента** (exchange_product_id)  
   - **Наименование Инструмента** (exchange_product_name)  
   - **Базис поставки** (delivery_basis_name)  
   - **Объем Договоров в единицах измерения** (volume)  
   - **Объем Договоров, руб.** (total)  
   - **Количество Договоров, шт.** (count)  
4. Сохраняет данные в таблицу базы данных `spimex_trading_results` со следующей структурой:  

| Поле                | Описание                                          |
|---------------------|--------------------------------------------------|
| `id`                | Уникальный идентификатор записи.                  |
| `exchange_product_id` | Код инструмента.                                 |
| `exchange_product_name` | Наименование инструмента.                       |
| `oil_id`            | Первые 4 символа `exchange_product_id`.          |
| `delivery_basis_id` | Символы с 5 по 7 `exchange_product_id`.           |
| `delivery_basis_name` | Базис поставки.                                  |
| `delivery_type_id`  | Последний символ `exchange_product_id`.          |
| `volume`            | Объем договоров в единицах измерения.            |
| `total`             | Общая сумма договоров (руб.).                    |
| `count`             | Количество договоров.                            |
| `date`              | Дата бюллетеня.                                  |
| `created_on`        | Дата и время создания записи.                    |
| `updated_on`        | Дата и время последнего обновления записи.       |  

---

### Запуск проекта  
1. Клонируйте репозиторий.  
2. Установите зависимости:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Настройте подключение к базе данных в файле конфигурации.  
4. Запустите паука `oil`:  
   ```bash
   scrapy crawl oil
   ```  

---

### Результат  
Скачанные и обработанные данные сохраняются в базу данных для дальнейшей аналитики и использования в других системах.  

