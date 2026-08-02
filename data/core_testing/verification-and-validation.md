# Верифікація та валідація

**Source:** https://qalight.ua/baza-znaniy/verifikatsiya-ta-validatsiya/

---

### Події

Верифікація та валідація

![Validation vs Verification](https://qalight.ua/wp-content/uploads/2023/11/valvsver.png)  
Ці два поняття тісно пов’язані з процесами тестування і забезпечення якості. На жаль, їх часто плутають, хоча відмінності між ними досить істотні.

**Верифікація (Verification)** – це статична практика перевірки документів, дизайну, архітектури, коду, тощо

* **Верифікація** – це процес який включає в себе перевірку Plans, Requirement Specifications, Design Specifications, Code, Test Cases, Chek-Lists, etc.
* **Верифікація** завжди проходить без запуску коду.
* **Верифікація** використовує методи – reviews, walkthroughs, inspections, etc.
* **Верифікація** відповідає на питання “Чи робимо ми продукт правильно?”
* **Верифікація** допоможе визначити, чи є програмне забезпечення **високої якості**, але воно не гарантує, що система **корисна**. Перевірка пов’язана з тим, що система добре спроектована і безпомилкова.
* **Верифікація** відбувається до **Валідації**.

Вона містить всі активності які дозволяють досягти високої якості програмного забезпечення:

1. **Inspection** in software engineering, refers to peer review of any work product by trained individuals who look for defects using a well defined process. (**Fagan inspection**)
2. **Walkthroughs** in software engineering, a **walkthrough** or **walkthrough** is a form of software peer review «in which a designer or programmer leads members of the development team and other interested parties go through a software product, and the participants ask questions and make comments about possible errors, violation of development standards, and other problems ».
3. **Reviews** in software development, peer review is a type of software review in which a work product (document, code, or other) is examined by its author and one or more colleagues, in order to evaluate its technical content and quality.

**Валідація (validation)** – це процес оцінки кінцевого продукту, необхідно перевірити, чи відповідає програмне забезпечення очікуванням і вимогам клієнта. Це динамічний механізм перевірки та тестування фактичного продукту.

* **Валідація** завжди включає в себе запуск коду програми.
* **Валідація** використовує методи, такі як тестування Black Box, тестування White Box і нефункціональне тестування.
* **Валідіція** відповідає на питання “Чи робимо ми правильний продукт?”
* **Валідація** перевіряє, чи відповідає програмне забезпечення вимогам і очікуванням клієнта.
* **Валідація** може знайти помилки, які процес **Верифікації** не може зловити.
* **Валідація** відбувається після **Верифікації**.

На практиці, відмінності верифікації та валідації мають велике значення: замовника цікавить більшою мірою валідація (задоволення власних вимог); виконавця, в свою чергу, хвилює не тільки дотримання всіх норм якості (верифікація) при реалізації продукту, а й відповідність всіх особливостей продукту бажанням замовника.