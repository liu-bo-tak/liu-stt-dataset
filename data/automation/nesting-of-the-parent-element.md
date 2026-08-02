# Вкладеність батьківського елементу

**Source:** https://qalight.ua/baza-znaniy/vkladenist-batkivskogo-elementu/

---

### Події

Вкладеність батьківського елементу

Використання вкладеності від батьківського елемента:

Пошук Dropdown поля:

*.//select//option[value=’saab’]* — запит: знайти усі селекти, у яких option дорівнює ‘saab’

Пошук Radio button поля:

Особливість – працюють у групі по черзі. Може бути тільки один можливий option.

*.//input[@type=’ratio’ and @name=’group1’ and @value=’Milk’]*

Пошук Checkbox поля:

*.//input[@type=’checkbox’ and @value=’a1’]*

Пошук Input поля:

*.//input[@id=’Login’]*

Пошук Text area поля:

*.//textarea*

Пошук кнопки:

*.//button[@type=’submit’]*

Функція text():

*.//\*[text()=’Заголовок H1’] або точніше: .//h1[text()=’Заголовок H1’]*

Функція contains():

contains() дозволяє шукати за частковим входженням тексту.

*.//h1[contains(text(),’Заг’)*

*.//\*[contains(@id,’Teg’)]*

Вкладені локатори:

Ситуація використання вкладених локаторів може виникнути за наявності таблиці, яка заповнюється під час формування сторінки. Суть кейсу – знайти користувача Taras та знайти його відгук.

*.//td[contains(text(),’Taras’)]//..//td[2]*

Другий варіант пошуку за коміркою:

*.//table[@class=’table-class’]//tr[.//td[contains(text(),’Taras’)]]//td[2]*

Тут ви можете потренуватися у написанні локаторів, на наведених вище прикладах: <https://drive.google.com/file/d/0B7P46-HjBsqpM1BDOVA5cjNZMG8/view>.