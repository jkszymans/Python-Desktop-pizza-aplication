# Pizza is love, pizza is life



## Wstęp
   Cześć, przedstawiam Ci aplikcję desktopową, która sprawi że twój dzień stanie się lepszy. Tak, jak sam tytuł wskazuje, ułatwie Ci zjedzenie pizzy. Wszystko to w wybranym przez ciebie lokalu. Już nie musisz iść do restauracji, tylko po to by rozczarować się tamtejszym menu. Wszystkich niezbędnych informacji dowiesz się z samego programu. Aplikacja bazuje na wprowadzonej przez Ciebie lokalizacji i wymaga dostępu do sieci. Pisanie tego arcydzieła sprawiło mi dużo frajdy, a zarazem było okazją do doskonalenia swoich umiejętności programowania. Jak dobrze wiemy najlepszą nauką jest praktyka. Jedynym mankamentem tego cuda jest sposób otrzymywania danych jak i egzekwowanie zamówień. Wszystko opiera się na stronie ,,pizzaportal.pl". Z racji tego, iż nie posiadam żadnej licencji na operowanie danymi z tej strony, musze zagwarantować, że aplikacja nie służy jako środek jakiegokolwiek zarobku. Stworzyłem ją głównie w celach edukacyjnych. 

![3](https://user-images.githubusercontent.com/52679269/84318840-58ef0380-ab6f-11ea-8baa-876a7878214c.PNG)

## Struktura aplikacji
   Program został napisany w języku programowania `Python`. W dużym stopniu korzysta z biblioteki `Tkinter`(Interfejs graficzny aplikacji) i `Selenium Webdriver`(wykonywanie kluczowych operacji do działania programu). Ważna cechą programu jest jego architektura. Całość została stworzona na bazie wzorca `MVC`(model-view-controller). Starałem się także zachować zasady `SOLID`. Inteligentny boilerplate projektu umożliwia proste oddzielenie plików do oprawy graficznej, bazy danych itp. Poniżej zamieszczam opis kluczowych plików.

![4](https://user-images.githubusercontent.com/52679269/84318385-a454e200-ab6e-11ea-8e33-02f1674c7cf0.PNG)

### model.py
   W tym pliku znajdują się 2 klasy. Pierwsza z nich odpowiada za obsługę bazy danych, obsługującej dane klienta. Posiada kilka metod które pozwalają na łatwe wyciąganie informacji np. imię użytkownika, jak i udostępnianie interfejs zapisu danych do bazy.
  Kolejną klasą `Pizzeria`. Sama klasa inicjuję siebie jako instancję `Selenium Webdriver`. Pozwala na operowanie po stronie pizzaportal jak i webscraping danych. Wykonuje podstawowe czynności jak wybieranie pizzeri czy wpisanie adresu zamieszkania.
  
### view.py
   Jak sama nazwa wskazuje plik ten posiada kilka klas, które reprezentują poszczególne widoki programu. Inicjują siebie jako `tk.Frame` czyli instancję widgetu okna z biblioteki Tkinter. `StartPage` obrazuje nam wygląd początkowy, `RegisterPage` ekran rejestracji użytkownika, a `CallPage`, czyli największa klasa programu zawiera implementację obrazu ekranu zamówień.

### controller.py
   Plik ten posiada tylko jedną klasę, jednakże jest ona bardzo ważna dla funkcjonowania programu. To ona zarządza danymi uzyskiwanymi z pliku model.py i przekazuje je do odpowiednim widokom. Z drugiej strony, przekazuje dane wpisane w formach widoku (np. pola rejestracyjne) do odpowiednich metod modelu by ten je zapisał. Prawdziwy kontroler!
   
![pizza1](https://user-images.githubusercontent.com/52679269/84318461-c3537400-ab6e-11ea-92eb-233b2eee61df.PNG)
  
## Podsumowanie
   Podsumowując, program posiada wiele niedociągnięć które postaram się poprawić. Ogromna wadą programu jest używanie interfejsu strony ,,PizzaPortal'', lecz niestety nie znalazłem wielu API, które by udostępniły możliwość zamawiania pizzy. Jeżeli chodzi o funkcjonalność aplikacji to jest ona praktycznie zerowa z racji braku praw do używania strony w ten sposób. Można by pokusić się o stwierdzenie że ten program stworzyłem dla siebie w celu edukacyjnyma, a ja w 99% z nim się zgodzę ;)
   
![pizza2](https://user-images.githubusercontent.com/52679269/84318467-c77f9180-ab6e-11ea-95d1-3da9d3a1bda7.PNG)
