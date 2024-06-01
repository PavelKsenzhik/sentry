Решение

Используя запрос 
```
SELECT b.colour,
       COUNT(*) as count
  FROM table_checkout as a
  INNER JOIN table_phones as b on b.id=a.phone_id
  GROUP BY b.colour
  ORDER BY count DESC;
```

Получаем ответ
```commandline
синий	500
красный	429
голубой	43
золотой	28
```

Соответственно ответ: Золотой
