// Some definitions presupposed by pandoc's typst output.
#let blockquote(body) = [
  #set text( size: 0.92em )
  #block(inset: (left: 1.5em, top: 0.2em, bottom: 0.2em))[#body]
]

#let horizontalrule = line(start: (25%,0%), end: (75%,0%))

#let endnote(num, contents) = [
  #stack(dir: ltr, spacing: 3pt, super[#num], contents)
]

#show terms: it => {
  it.children
    .map(child => [
      #strong[#child.term]
      #block(inset: (left: 1.5em, top: -0.4em))[#child.description]
      ])
    .join()
}

// Some quarto-specific definitions.

#show raw.where(block: true): set block(
    fill: luma(230),
    width: 100%,
    inset: 8pt,
    radius: 2pt
  )

#let block_with_new_content(old_block, new_content) = {
  let d = (:)
  let fields = old_block.fields()
  fields.remove("body")
  if fields.at("below", default: none) != none {
    // TODO: this is a hack because below is a "synthesized element"
    // according to the experts in the typst discord...
    fields.below = fields.below.abs
  }
  return block.with(..fields)(new_content)
}

#let empty(v) = {
  if type(v) == str {
    // two dollar signs here because we're technically inside
    // a Pandoc template :grimace:
    v.matches(regex("^\\s*$")).at(0, default: none) != none
  } else if type(v) == content {
    if v.at("text", default: none) != none {
      return empty(v.text)
    }
    for child in v.at("children", default: ()) {
      if not empty(child) {
        return false
      }
    }
    return true
  }

}

// Subfloats
// This is a technique that we adapted from https://github.com/tingerrr/subpar/
#let quartosubfloatcounter = counter("quartosubfloatcounter")

#let quarto_super(
  kind: str,
  caption: none,
  label: none,
  supplement: str,
  position: none,
  subrefnumbering: "1a",
  subcapnumbering: "(a)",
  body,
) = {
  context {
    let figcounter = counter(figure.where(kind: kind))
    let n-super = figcounter.get().first() + 1
    set figure.caption(position: position)
    [#figure(
      kind: kind,
      supplement: supplement,
      caption: caption,
      {
        show figure.where(kind: kind): set figure(numbering: _ => numbering(subrefnumbering, n-super, quartosubfloatcounter.get().first() + 1))
        show figure.where(kind: kind): set figure.caption(position: position)

        show figure: it => {
          let num = numbering(subcapnumbering, n-super, quartosubfloatcounter.get().first() + 1)
          show figure.caption: it => {
            num.slice(2) // I don't understand why the numbering contains output that it really shouldn't, but this fixes it shrug?
            [ ]
            it.body
          }

          quartosubfloatcounter.step()
          it
          counter(figure.where(kind: it.kind)).update(n => n - 1)
        }

        quartosubfloatcounter.update(0)
        body
      }
    )#label]
  }
}

// callout rendering
// this is a figure show rule because callouts are crossreferenceable
#show figure: it => {
  if type(it.kind) != str {
    return it
  }
  let kind_match = it.kind.matches(regex("^quarto-callout-(.*)")).at(0, default: none)
  if kind_match == none {
    return it
  }
  let kind = kind_match.captures.at(0, default: "other")
  kind = upper(kind.first()) + kind.slice(1)
  // now we pull apart the callout and reassemble it with the crossref name and counter

  // when we cleanup pandoc's emitted code to avoid spaces this will have to change
  let old_callout = it.body.children.at(1).body.children.at(1)
  let old_title_block = old_callout.body.children.at(0)
  let old_title = old_title_block.body.body.children.at(2)

  // TODO use custom separator if available
  let new_title = if empty(old_title) {
    [#kind #it.counter.display()]
  } else {
    [#kind #it.counter.display(): #old_title]
  }

  let new_title_block = block_with_new_content(
    old_title_block, 
    block_with_new_content(
      old_title_block.body, 
      old_title_block.body.body.children.at(0) +
      old_title_block.body.body.children.at(1) +
      new_title))

  block_with_new_content(old_callout,
    block(below: 0pt, new_title_block) +
    old_callout.body.children.at(1))
}

// 2023-10-09: #fa-icon("fa-info") is not working, so we'll eval "#fa-info()" instead
#let callout(body: [], title: "Callout", background_color: rgb("#dddddd"), icon: none, icon_color: black, body_background_color: white) = {
  block(
    breakable: false, 
    fill: background_color, 
    stroke: (paint: icon_color, thickness: 0.5pt, cap: "round"), 
    width: 100%, 
    radius: 2pt,
    block(
      inset: 1pt,
      width: 100%, 
      below: 0pt, 
      block(
        fill: background_color, 
        width: 100%, 
        inset: 8pt)[#text(icon_color, weight: 900)[#icon] #title]) +
      if(body != []){
        block(
          inset: 1pt, 
          width: 100%, 
          block(fill: body_background_color, width: 100%, inset: 8pt, body))
      }
    )
}



#let article(
  title: none,
  subtitle: none,
  authors: none,
  date: none,
  abstract: none,
  abstract-title: none,
  cols: 1,
  margin: (x: 1.25in, y: 1.25in),
  paper: "us-letter",
  lang: "en",
  region: "US",
  font: "libertinus serif",
  fontsize: 11pt,
  title-size: 1.5em,
  subtitle-size: 1.25em,
  heading-family: "libertinus serif",
  heading-weight: "bold",
  heading-style: "normal",
  heading-color: black,
  heading-line-height: 0.65em,
  sectionnumbering: none,
  pagenumbering: "1",
  toc: false,
  toc_title: none,
  toc_depth: none,
  toc_indent: 1.5em,
  doc,
) = {
  set page(
    paper: paper,
    margin: margin,
    numbering: pagenumbering,
  )
  set par(justify: true)
  set text(lang: lang,
           region: region,
           font: font,
           size: fontsize)
  set heading(numbering: sectionnumbering)
  if title != none {
    align(center)[#block(inset: 2em)[
      #set par(leading: heading-line-height)
      #if (heading-family != none or heading-weight != "bold" or heading-style != "normal"
           or heading-color != black or heading-decoration == "underline"
           or heading-background-color != none) {
        set text(font: heading-family, weight: heading-weight, style: heading-style, fill: heading-color)
        text(size: title-size)[#title]
        if subtitle != none {
          parbreak()
          text(size: subtitle-size)[#subtitle]
        }
      } else {
        text(weight: "bold", size: title-size)[#title]
        if subtitle != none {
          parbreak()
          text(weight: "bold", size: subtitle-size)[#subtitle]
        }
      }
    ]]
  }

  if authors != none {
    let count = authors.len()
    let ncols = calc.min(count, 3)
    grid(
      columns: (1fr,) * ncols,
      row-gutter: 1.5em,
      ..authors.map(author =>
          align(center)[
            #author.name \
            #author.affiliation \
            #author.email
          ]
      )
    )
  }

  if date != none {
    align(center)[#block(inset: 1em)[
      #date
    ]]
  }

  if abstract != none {
    block(inset: 2em)[
    #text(weight: "semibold")[#abstract-title] #h(1em) #abstract
    ]
  }

  if toc {
    let title = if toc_title == none {
      auto
    } else {
      toc_title
    }
    block(above: 0em, below: 2em)[
    #outline(
      title: toc_title,
      depth: toc_depth,
      indent: toc_indent
    );
    ]
  }

  if cols == 1 {
    doc
  } else {
    columns(cols, doc)
  }
}

#set table(
  inset: 6pt,
  stroke: none
)
#import "@preview/fontawesome:0.5.0": *

#show: doc => article(
  title: [Лекция 1. Введение и простые решения],
  lang: "ru",
  sectionnumbering: "1.1.1",
  pagenumbering: "1",
  toc: true,
  toc_title: [Оглавление],
  toc_depth: 2,
  cols: 1,
  doc,
)

версия 0.5 от 15.09.2025

Хабибуллин Ринат

#block[
```python
print('hello')
```

#block[
```
hello
```

]
]
= Введение в дисциплину. Моделирование при исследовании скважин и пластов
<введение-в-дисциплину.-моделирование-при-исследовании-скважин-и-пластов>
== Картинки и код для проверки
<картинки-и-код-для-проверки>
#set math.equation(numbering: "(1)")
#let nonumeq = math.equation.with(block: true, numbering: none)
#let dm(x) = box[#nonumeq[#x]]
#let dfrac(x,y) = math.frac(dm(x),dm(y))

$ frac(a,b) $
Часто для анализа уравнений неустановившейся фильтрации используются безразмерные переменные. Мы будем использовать переменные в виде:

$ r_D = r / r_w $

Обычная дробь в строке: $a \/ b$, а вот крупная дробь: \#frac(a, b).

$ f_D = (d / s) / a $

A large inline fraction is shown here: \$ x = (display(frac(1,2))) \$

$ t_D = frac(k t, phi mu c_t r_w^2) $

$ p_D = frac(2 pi k h, q_s B mu) (p_i - p_(w f)) $

$ q_D = q / q_(r e f) $

Здесь использованы единицы измерения СИ.

- $q_s$ - дебит скважины на поверхности, приведенный к нормальным условиям м3/с
- $phi$ - пористость, доли единиц
- $mu$ - вязкость нефти в пласте, Па с
- $B$ - объемный коэффициент нефти, м3/м3
- $p_i$ - начальное давление в пласте, Па
- $p_(w f)$ - давление забойное, Па
- $c_t$ - общая сжимаемость системы в пласте, 1/Па

Использование безразмерных переменных позволяет упростить уравнение фильтрации, которое примет вид

$ frac(partial p_D, partial t_D) = 1 / r_D frac(partial (r_D frac(partial p_D, partial r_D)), partial r_D) $

$ frac(partial p_D, partial t_D) = 1 / r_D [frac(partial, partial r_D) (r_D frac(partial p_D, partial r_D))] $

Решение этого уравнения - функция безразмерного давления от безразмерных времени и расстояния $p_D (r_D \, t_D)$

Для практических расчетов удобнее бывает использовать безразмерные переменные полученные для практических метрических единиц измерения.

#block[
#callout(
body: 
[
$ r_D = r / r_w $

$ t_D = frac(0.00036 k t, phi mu c_t r_w^2) $

$ p_D = frac(k h, 18.4 q_s B mu) (p_i - p_(w f)) $

$ q_D = q / q_(r e f) $

Здесь использованы практические метрические единицы измерения.

- $q_s$ - дебит скважины на поверхности, приведенный к нормальным условиям м3/сут
- $phi$ - пористость, доли единиц
- $mu$ - вязкость нефти в пласте, сП
- $B$ - объемный коэффициент нефти, м3/м3
- $p_i$ - начальное давление в пласте, атм
- $p_(w f)$ - давление забойное, атм
- $c_t$ - общая сжимаемость системы в пласте, 1/атм

]
, 
title: 
[
Определение безразмерных переменных в практических метрических единицах
]
, 
background_color: 
rgb("#ccf1e3")
, 
icon_color: 
rgb("#00A047")
, 
icon: 
fa-lightbulb()
, 
body_background_color: 
white
)
]
== Расчет решения с использованием python
<расчет-решения-с-использованием-python>
Для работы с решениями уравнения фильтрации удобно использовать язык программирования python. Расчет на python может быть реализован на основе библиотек numpy scipy.

#block[
```python
"""
Импортируем библиотеки для расчетов. 
numpy - для работы с массивами и подготовки данных 
matplotlib - для построения графиков
scipy - для решения линейных уравнений
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy
```

]
Для удобства дальнейшего изложения и использования расчетных функций при создании функций и переменных на языке python названия формируются по следующим принципам:

- сначала указывается, что расчитывается в функции, в данном случае - давление `p` или `dp`
- потом указываются пояснения - в данном случае `dp_ss` - steady state pressure
- в конце указывается размерность в которой ожидается получаение ответа - в данном случае `atma` - абсолютные атмосферы.

#block[
```python
"""
Определим функции для расчета стационарного решения
"""
def dp_ss_atm(q_liq_sm3day = 50,
               mu_cP = 1,
               b_m3m3 = 1.2,
               kh_mDm = 40,
               r_e_m = 240,
               r_m = 0.1):
  """
  функция расчета перепада давления в произвольной точке пласта 
  на расстоянии r_m от центра скважины для стационарного решения
  - q_liq_sm3day - дебит жидкости на поверхности в стандартных условиях
  - mu_cP - вязкость нефти (в пластовых условиях)
  - B_m3m3 - объемный коэффициент нефти 
  - kh_mDm - kh пласта
  - r_e_m - радиус контрура питания, м  
  - r_m - расстояние на котором проводится расчет, м
  """
  return 18.42 * q_liq_sm3day * mu_cP * b_m3m3/ kh_mDm * np.log(r_e_m/r_m)

def p_ss_atma(p_res_atma = 250,
              q_liq_sm3day = 50,
              mu_cP = 1,
              b_m3m3 = 1.2,
              k_mD = 40,
              h_m = 10,
              r_e_m = 240,
              r_m = 0.1):
  """
  функция расчета давления в произвольной точке пласта 
  на расстоянии r_m от центра скважины для стационарного решения 
  - p_res_atma - пластовое давление, давление на контуре питания
  - q_liq_sm3day - дебит жидкости на поверхности в стандартных условиях
  - mu_cP - вязкость нефти (в пластовых условиях)
  - B_m3m3 - объемный коэффициент нефти 
  - k_mD - проницаемость пласта
  - h_m - мощность пласта, м
  - r_e_m - радиус контрура питания, м  
  - r_m - расстояние на котором проводится расчет, м
  """
  return p_res_atma - dp_ss_atm(q_liq_sm3day = q_liq_sm3day,
                                mu_cP = mu_cP,
                                b_m3m3 = b_m3m3,
                                kh_mDm = k_mD * h_m,
                                r_e_m = r_e_m,
                                r_m = r_m)
```

]
Функции расчетов могут быть использованы для построения графиков, например с использованием matplotlib

```python
"""
Построим график распределения давления в пласте
"""
# формируем массив расстояний для которых будем проводить расчет
r_arr = np.linspace(0.1, 100, 500) 

# рассчитываем массив давлений на соответствующих расстояниях
# для расчета используется векторный расчет numpy - нет необходимости делать цикл в явном виде
# для примера показана передача всех аргументов созданной функции
p_arr = p_ss_atma(p_res_atma = 250,
                  q_liq_sm3day = 50,
                  mu_cP = 1,
                  b_m3m3 = 1.2,
                  k_mD = 40,
                  h_m = 10,
                  r_e_m = 240,
                  r_m = r_arr)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5,8))

# рисуем график в обычных координатах
ax1.plot(r_arr, p_arr)   # команда отрисовки графика по заданным массивам
ax1.plot(-r_arr, p_arr)   # отрицательная ветка
# настраиваем график

ax1.set_xlabel('r, m')
ax1.set_ylabel('p, atma')

# рисуем график в логарифмических координатах
ax2.plot(r_arr, p_arr)   # команда отрисовки графика по заданным массивам
ax2.plot(-r_arr, p_arr)   # отрицательная ветка
# настраиваем график
ax2.set_xlabel('r, m')
ax2.set_xscale('symlog', linthresh=0.1, linscale=0.6)
plt.show()
```

#figure([
#box(image("test_files/figure-typst/fig-stac_pressure_dist_1-output-1.svg"))
], caption: figure.caption(
position: bottom, 
[
Распределение давления в круговом пласте
]), 
kind: "quarto-float-fig", 
supplement: "Рисунок", 
)
<fig-stac_pressure_dist_1>


можно получить выражение #math.equation(block: true, numbering: "(1)", [ $ p_D (r_D \, t_D \, d Q_D) = - frac(d Q_D t_D, 2) [(1 + frac(r_D^2, 4 t_D)) E i (- frac(r_D^2, 4 t_D)) + e^(- frac(r_D^2, 4 t_D))] $ ])<eq-ei_sol_lin_rate>

где $d Q_D$ - скорость изменения дебита.

Для таблично заданных дебитов и времен можно оценить

$ d Q_(D (i)) = frac(Q_(D (i)) - Q_(D (i - 1)), t_(D (i)) - t_(D (i - 1))) $

Cравните формулу (#ref(<eq-ei_sol_lin_rate>, supplement: [])) с формулой (9.68) в книге Щелкачева "Основы неустановившейся фильтрации" @shchelkachevOsnovyPrilozheniyaTeorii1995

Тогда, используя принцип суперпозиции, можем выписать выражение для изменения давления на скважине и вокруг нее для произвольного момента времени

#math.equation(block: true, numbering: "(1)", [ $ P_(m r . D) (t_D \, r_D) = sum_i p_D (t_D - t_(D (i)) \, r_D \, d Q_(D (i + 1)) - d Q_(D (i))) dot.op cal(H) (t_D - t_(D (i))) $ ])<eq-sol_lin_superposition>

#bibliography("refs.bib")

