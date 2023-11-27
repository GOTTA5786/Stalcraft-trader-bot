# Stalcraft-trader-bot

Данный проект был создан для решения реальной проблемы - траты огромного кол-ва времени на мониторинг внутриигрового аукциона в STALCRAFT.

В игре есть разные способы заработка, и одним из наиболее прибыльных является перепродажа вещей на аукционе. Именно идея автоматизации этого процесса и легла в основу проекта.

Идея использование инжекторов была отброшена на этапе проектирования. Инжекторы повышают шанс на обнаружение программы и последующий бан аккаунта. Вместо этого я решил использовать компьютерное зрение и эмуляцию движения курсора.
Для машинного зрения я использовал Tesseract, а для эмуляции движения и кликов мыши использовал interseption driver т.к. програмные клики не обходили защиту игры. Программа представляет из себя бота который выполняет по кругу определенные действия.
На все действия бота есть рандомная задержка и скорость, чтобы его действия были похожи на человеческие. Бот работает довольно медленно из-за задержки и машинного зрения, его стоит использовать как помощника в режиме афк.

Алгоритм работы:
1. Пользователь вводит название и максимальную цену выкупа (можно мониторить несколько товаров).
2. Бот открывает аукцион и вводит название предмета в поле, затем фильтрует товары по возростанию цены.
3. С помощью зрения бот считывает кол-во предметов в стеке и делит конечную стоимость на кол-во.
4. Если стоимость одного предмета не превышает максимальную цену выкупа - бот выкупает лот и обновляет аукциона.
5. Если на странице не найдены подходящие лоты - скроллит вниз ровно на один экран.
6. Когда заканчивается скролл - переходит на следующую страницу.
7. После просмотра одного товара он переходит к другим. 
