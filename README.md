# Foodgram project
Продуктовый помощник. Онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список избранного, а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект находится в стадии разработки.

В настоящее время реализовано:
* регистрация и аутентификация пользователей;
* рецепты:
  * создание, редактирование и удаление рецепта;
  * фильтрация по тегам;
  * постраничное отображениие;
* получение файла со списком покупок;
* API:
  * получение списка ингредиентов;
  * добавление рецепта в список избранного;
  * добавление рецепта в список покупок;
  * подписка на автора.

## Техническое описание:
#### Сервисы и страницы проекта:
* Главная страница: 

  Список рецептов, отсортированных по дате публикации.

* Страница рецепта:

  Полное описание рецепта, возможность добавить рецепт в избранное и в список покупок, возможность подписаться на автора рецепта.

* Страница пользователя:

  Имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя.

* Подписка на авторов:

  Подписка на публикации доступна только авторизованному пользователю. Страница подписок доступна только владельцу.
  * Пользователь переходит на страницу другого пользователя или на страницу рецепта и подписывается на публикации автора кликом по кнопке «Подписаться на автора».
  * Пользователь переходит на страницу «Мои подписки» и просматривает список рецептов, опубликованных теми авторами, на которых он подписался.
  * Сортировка записей — по дате публикации от новых к старым.
  * При необходимости пользователь может отказаться от подписки на автора: переходит на страницу автора или на страницу его рецепта и нажимает «Отписаться от автора».

* Список избранного:

  Работа со списком избранного доступна только авторизованному пользователю. Список избранного может просматривать только его владелец.
  * Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в избранное».
  * Пользователь переходит на страницу «Список избранного» и просматривает персональный список избранных рецептов.
  * При необходимости пользователь может удалить рецепт из избранного.

* Список покупок:

  Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец. Список покупок скачивается в текстовом формате. При скачивании списка покупок для нескольких рецептов одновременно, ингредиенты в результирующем списке не дублируются, количество каждого уникального ингридиетса суммируется.
  * Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
  * Пользователь переходит на страницу Список покупок, там доступны все добавленные в список рецепты.
  * Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
  * При необходимости пользователь может удалить рецепт из списка покупок.

* Фильтрация по тегам:

  При нажатии на название тега выводится список рецептов, отмеченных этим тегом. Фильтрация может проводится по нескольким тегам в комбинации «или»: если выбраны несколько тегов — в результате должны быть показаны рецепты, которые отмечены хотя бы одним из этих тегов. При фильтрации на странице пользователя фильтруются только рецепты выбранного пользователя. Такой же принцип соблюдается при фильтрации списка избранного.

#### Уровни доступа пользователей:
* Неавторизованный пользователь:
  * Создать аккаунт.
  * Просматривать рецепты на главной странице.
  * Просматривать отдельные страницы рецептов.
  * Просматривать страницы пользователей.
  * Фильтровать рецепты по тегам.

* Авторизованный пользователь:
  * Входить в систему под своим логином и паролем.
  * Выходить из системы.
  * Восстанавливать свой пароль.
  * Менять свой пароль.
  * Создавать/редактировать/удалять собственные рецепты.
  * Просматривать рецепты на главной странице.
  * Просматривать страницы пользователей.
  * Просматривать отдельные страницы рецептов.
  * Фильтровать рецепты по тегам.
  * Работать с персональным списком избранного: добавлять/удалять чужие рецепты, просматривать свою страницу избранных рецептов.
  * Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл со количеством необходимых ингредиентов для рецептов из списка покупок.
  * Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

* Администратор обладает всеми правами авторизованного пользователя. Плюс к этому он может:
  * Изменять пароль любого пользователя.
  * Создавать/блокировать/удалять аккаунты пользователей.
  * Редактировать/удалять любые рецепты.
  * Добавлять/удалять/редактировать ингредиенты.

## Технологии:
* [Python](https://www.python.org/) версия 3.9.2
* [Django Framework](https://www.djangoproject.com/) версия 3.1.6
* [Django REST Framework](https://www.django-rest-framework.org/) версия 3.12.2
* Gunicorn
* PostgreSQL
* Nginx
* Docker

## Автор
[Dmitriy Peretoka](https://github.com/dmitriyperetoka)
