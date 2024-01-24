>Не импортирован модуль datetime.
><br/>
> Добавлена строка:
> <br/>
> import datetime

>В методе get_age неправильно выситывался возраст.
> <br/>
> Было:
>  <br/>
> return self.yob - now.year
>   <br/>
> Исправлено:
>  <br/>
>return now.year - self.yob

>В методе set_name неправильно присваивалось имя.
> <br/>
> Было:
>  <br/>
>self.name = self.name
>   <br/>
> Исправлено:
>  <br/>
>self.name = name

>В методе set_address неправильно присваивался адрес.
> <br/>
> Было:
>  <br/>
> self.address == address
>   <br/>
> Исправлено:
>  <br/>
>  self.address = address

> Ошибка в методе is_homeless. Изменено условие ответа
><br/>
> Было:
><br/>
> ```   return address is None ```
> <br/>
> Исправлено:
><br/>
> ````
> if self.address is None or self.address == '':
>   return True
> else:
>   return True
> ````