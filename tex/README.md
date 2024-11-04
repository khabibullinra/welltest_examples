# настройки tex для компиляции лекций

используется xetex 

поддержкa русского языка для xelatex

```
\usepackage[english,russian]{babel}   %% загружает пакет многоязыковой вёрстки
\usepackage{fontspec}      %% подготавливает загрузку шрифтов Open Type, True Type и др.
\defaultfontfeatures{Ligatures={TeX},Renderer=Basic}  %% свойства шрифтов по умолчанию
\setmainfont[Ligatures={TeX,Historic}]{Times New Roman} %% задаёт основной шрифт документа
\setsansfont{Comic Sans MS}                    %% задаёт шрифт без засечек
\setmonofont{Courier New}
```



надо следить за наличием шрифтов на машине где компилируются лекции 
- Times New Roman
- Comic Sans MS
- Courier New

при необходимости на линукс можно установить командой 

```bash
sudo apt-get install msttcorefonts
```

используется gnuplot для генерации некоторых графиков

```bash
sudo apt-get install gnuplot
```

---

надо добавить `-shell-escape` в параметрах вызова xelatex для того чтобы можно было использовать gnuplot
