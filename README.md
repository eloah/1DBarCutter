# 1DBarCutter
1D Bars Cutting Project. In particular, this desktop app is for cutting 6 or 12 meters long bars, but it is common 1d cutting problem which works for every case.
Written in Python 3.7, utilizes PySide lib for GUI development, reportlab for PDF creating, PuLP lib for algorithms of linear algebra and programming (not included in repository). App optimizes the cuts of bars and show how to cut the quantity defined of user with minimal waste of material. 

User have options to add the dimensions adn quantity of bars for cutting, lenght of initial material, add, remove, multiply in table content.
After algorithm beeing processed with initial data, the results are being shown on canva with series of cutting. Please note, that rules of algorithm is processing optimized cut, but without excellent optimization (~92%), so some bars can be being cut not so optimal (for example, from 10 last 2 bars could be be being cut from another bar, so visually it is not a problem to make). But algoritm is 100% optimal for quantity of bars. And after PDF is being created for user. 
