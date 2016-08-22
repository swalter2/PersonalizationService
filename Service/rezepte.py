import random
class Rezept:
    rezepte = {}
    def __init__(self):
        self.create_rezept_0()
        self.create_rezept_1()
        self.create_rezept_2()


    def get_rezept(self):
        return self.rezepte[random.randint(0, 2)]

    def create_rezept_0(self):
        rezept = {}
        rezept['titel'] = 'Chilisuppe'
        rezept['url'] = 'http://www.chefkoch.de/rezepte/946161200209097/Chilisuppe.html'
        rezept['beschreibung'] = 'Die Zwiebeln mit dem Mett in einem großen Topf in Öl anbraten. ' \
                                 'Dazu das Tomatenmark geben und alles gut umrühren. Anschließend Tomatensaft, Mais, ' \
                                 'Kidneybohnen und Chilibohnen dazugeben. Mit Salz, Pfeffer und Sambal Oelek abschmecken. ' \
                                 'Zum Schluss die Brechbohnen vorsichtig unterrühren. Kurz aufkochen lassen und dann ' \
                                 'noch ca. 10 Minuten zugedeckt ziehen lassen. Dazu passen einfache Brötchen oder Baguette. '
        zutaten = {}
        mett = {'name':'Mett','menge':'1Kg','preis':'2,19','anbieter':'Real'}
        zwiebel = {'name': 'Zwiebel', 'menge': '0.5Kg', 'preis': '0.99', 'anbieter': 'Rewe'}
        tomatenmark = {'name': 'Tomatenmark', 'menge': '1 Tube', 'preis': '0.49', 'anbieter': 'Aldi'}
        tomatensaft = {'name': 'Tomatensaft', 'menge': '2 Packungen', 'preis': '3.00', 'anbieter': 'Real'}
        mais = {'name': 'Mais', 'menge': '1 Dose', 'preis': '0.49', 'anbieter': 'Lidl'}
        kidneybohnen = {'name': 'Kidneybohnen', 'menge': '1 Dose', 'preis': '0.45', 'anbieter': 'Kaufland'}
        chillibohnen = {'name': 'Chillibohnen', 'menge': '1 Dose', 'preis': '0.77', 'anbieter': 'Kaufland'}
        brechbohnen = {'name': 'Grüne Brechbohnen', 'menge': '1 Glas', 'preis': '0.89', 'anbieter': 'Aldi'}
        zutaten['mett'] = mett
        zutaten['zwiebel'] = zwiebel
        zutaten['tomatenmark'] = tomatenmark
        zutaten['tomatensaft'] =tomatensaft
        zutaten['mais'] = mais
        zutaten['kidneybohnen'] = kidneybohnen
        zutaten['chillibohnen'] = chillibohnen
        zutaten['brechbohnen'] = brechbohnen
        rezept['zutaten'] = zutaten
        self.rezepte[0] = rezept


    def create_rezept_1(self):
        rezept = {}
        rezept['titel'] = 'Käse Maccaroni'
        rezept['url'] = 'http://www.chefkoch.de/rezepte/720881174834419/Kaese-Makkaroni.html'
        rezept['beschreibung'] = 'Makkaroni im Salzwasser bissfest kochen. Den Ofen auf 200°C vorheizen. ' \
                                 'Zwiebel fein würfeln und in der Butter glasig anbraten. ' \
                                 'Mehl dazugeben, nach und nach die Milch unter ständigem Rühren dazugießen. ' \
                                 'Mit Pfeffer, Salz und etwas Muskat würzen und ca. 10 Minuten ' \
                                 'auf kleiner Flamme köcheln lassen. Die Nudeln abgießen. ' \
                                 'Die Hälfte des geriebenen Käses zur Sauce geben und darin unter ' \
                                 'Rühren schmelzen lassen. Die Nudeln unter die Käsesauce mischen ' \
                                 'und alles in eine Auflaufform füllen. Den restlichen Käse darauf streuen, ' \
                                 'ein paar Butterflöckchen darauf verteilen. In den Ofen schieben ' \
                                 'und ca. 30 Minuten backen lassen.'

        zutaten = {}
        nudeln = {'name': 'Maccaroni', 'menge': '300g', 'preis': '0.29', 'anbieter': 'Edeka'}
        zwiebel = {'name': 'Zwiebel', 'menge': '1', 'preis': '0.1', 'anbieter': 'Rewe'}
        milch = {'name': 'Milch', 'menge': '400ml', 'preis': '0.49', 'anbieter': 'Rewe'}
        butter = {'name': 'Butter', 'menge': '5 EL', 'preis': '1.49', 'anbieter': 'Aldi'}
        mehl = {'name': 'Mehl', 'menge': '3 EL', 'preis': '0.1', 'anbieter': 'Rewe'}
        kaese = {'name': 'Käse', 'menge': '200g', 'preis': '1.69', 'anbieter': 'Edeka'}
        zutaten['nudel'] = nudeln
        zutaten['zwiebel'] = zwiebel
        zutaten['milch'] = milch
        zutaten['butter'] = butter
        zutaten['mehl'] = mehl
        zutaten['kaese'] = kaese
        rezept['zutaten'] = zutaten
        self.rezepte[1] = rezept


    def create_rezept_2(self):
        rezept = {}
        rezept['titel'] = 'Spargel aus dem Ofen'
        rezept['url'] = 'http://www.chefkoch.de/rezepte/1417641246603822/Spargel-aus-dem-Ofen-ideal-fuer-Gaeste.html'
        rezept['beschreibung'] = 'Der Spargel gart im eigenen Saft und bekommt so einen wunderbar vollen Eigengeschmack.' \
                                 ' Vergleicht man gekochten damit, ist der gekochte fast schon fade. ' \
                                 'Seit ich dies hier ausprobiert habe, mag bei uns keiner mehr den Spargel ' \
                                 'anders zubereitet.Am besten nimmt man nicht zu dicken Stangen, ich ' \
                                 'bevorzuge so 1-1,5 cm dicke Stangen. Die sind schön zart und man hat wenig Abfall. ' \
                                 'Zuerst den Spargel gründlich schälen und die Enden abschneiden. ' \
                                 'Den Ofen auch 200°C oder 180°C Umluft vorheizen.Je zwei Bögen Alufolie übereinander ' \
                                 'legen und jeweils einen halben Teelöffel Butter darauf geben. 8 - 10 Stangen Spargel ' \
                                 '(je nach Dicke des Spargels, die Pakete sollten nicht zu groß sein, weil ' \
                                 'sie sonst nicht so gut garen, lieber mehrere machen - halten sich notfalls ' \
                                 'auch leichter warm) darauf legen. Jedes Bündel mit einem halben Teelöffel ' \
                                 'Zucker und einer guten Prise Salz bestreuen, dann den ersten Bogen Folie darüber ' \
                                 'verschließen und die Seiten auch - kein enges Päckchen wickeln, sondern wie eine ' \
                                 'Tüte oben umfalten. Dann den zweiten Bogen ebenso verschließen.Auf den Rost im ' \
                                 'Ofen legen und 40 - 50 Minuten warten. Ob der Spargel gar ist, kann man testen, ' \
                                 'wenn man ein Päckchen ein bisschen biegt, je leichter das geht, um so weicher ' \
                                 'ist der Spargel.Was jetzt kommt, ist sicher nicht professionell, aber hat prima ' \
                                 'funktioniert: Meine Gäste kamen ca. 40 Minuten zu spät, während dieser Zeit habe ' \
                                 'ich die Spargelpäckchen im Bett unter der Decke warm gehalten und sie dann nach ' \
                                 'und nach als wir gegessen haben, herausgeholt. Das war Klasse, so hatten wir die ' \
                                 'ganze Zeit wunderbaren heißen Spargel.Für ganz riesige Portionen: eine hohe ' \
                                 'Fettpfanne des Ofens nehmen, leicht mit Butter einpinseln, den Spargel darauf ' \
                                 'verteilen, pro Kilo 2 TL Butter, einen TL Zucker und eine gute Messerspitze Salz ' \
                                 'darauf verteilen, die Fettpfanne mit Alufolie verschließen (muss richtig dicht sein) ' \
                                 'und ab in den auf 200°C vorgeheizten Ofen (Umluft 180°C) für ca. 50 Minuten ' \
                                 '(ab 40 Minuten mal kosten, je nach Dicke braucht der Spargel mehr oder weniger Zeit).' \
                                 'Bei uns gibts dazu Nussbutter (hat nichts mit Nüssen zu tun! Siehe anderes Rezept) ' \
                                 'und neue Kartoffeln.'
        zutaten = {}
        spargel = {'name': 'Spargel', 'menge': '2Kg', 'preis': '15', 'anbieter': 'Spargel vom Drostenhof'}
        butter = {'name': 'Butter', 'menge': '4 TL ', 'preis': '1.49', 'anbieter': 'Aldi'}
        zucker = {'name': 'Rohrzucker', 'menge': '2 TL', 'preis': '1.49', 'anbieter': 'Rewe'}
        zutaten['spargel'] = spargel
        zutaten['butter'] = butter
        zutaten['zucker'] = zucker
        rezept['zutaten'] = zutaten
        self.rezepte[2] = rezept