# RU
Папка [thomson](/thomson/) решения [задачи Томсона](https://en.wikipedia.org/wiki/Thomson_problem) из [The Cambridge Cluster Database](http://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html)

Папка [tri](/tri/) - триангуляция (в строке - три номера вершин из [thomson](/thomson/), составляющих треугольник), построены в [Qhull](http://www.qhull.org/) (или [hull](http://www.netlib.org/voronoi/hull.html))

Папка [g](/g/) - триангуляция в виде графа в формате [DIMACS ](http://lcs.ios.ac.cn/~caisw/Resource/about_DIMACS_graph_format.txt) (нумерация вершин из [thomson](/thomson/) сохранена)

Папка [g2](/g2/) - к ребрам из [g](/g/) добавлены ребра между вершинами на расстоянии 2

Папка [vor](/vor/) - области Вороного (отделены пустой строкой, порядок соответствует вершинам из [thomson](/thomson/)). Можно строить в [scipy.spatial.SphericalVoronoi](https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.spatial.SphericalVoronoi.html), [libdts2](https://github.com/fmi-alg/libdts2), [stripy/STRIPACK](https://github.com/underworldcode/stripy) или руками по [g](/g/)

Папка [c](/c/) - правильные раскраски в формате "l <номер вершины> <номер цвета>"

Папка [code/viz](/code/viz) - программа для визуализации на opengl, чтобы собрать, нужны boost, [freeglut](http://freeglut.sourceforge.net/), [glm](https://glm.g-truc.net/0.9.9/index.html), [gl2ps](http://geuz.org/gl2ps/)

[code/sphere.nb](code/sphere.nb) - ноутбук Mathematica с визуализацией (медленно работает)

[colorings.txt](colorings.txt) - результаты по раскраске: <имя файла> <n цветов> диапазон радиусов

[diams.txt](diams.txt)- <имя файла> <мин расстояние между областями на расстоянии 3> <макс диаметр области> <отношение>

[intervals.txt](intervals.txt) - сумма результатов

