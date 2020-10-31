__Jak pomogłem daj gwiazdkę.__

# TextualAlgorithms
Textual algorithms implemented during laboratories
## labs
1. [String matching](./lab1.ipynb)
    - Zaimplementuj algorytmy wyszukiwania wzorców:
      - naiwny
      - automat skończony
      - algorytm KMP
    - Zaimplementuj testy porównujące szybkość działania wyżej wymienionych algorytmów.
    - Znajdź wszystkie wystąpienia wzorca "art" w załączonej ustawie, za pomocą każdego algorytmu.
    - Porównaj szybkość działania algorytmów dla problemu z p. 3.
    - Porównaj szybkość działania algorytmów poprzez wyszukanie słowa "kruszwil" we fragmencie polskiej Wikipedii
    - Zaproponuj tekst oraz wzorzec, dla którego zmierzony czas działania algorytmów 2 oraz 3 będzie co najmniej 2-krotnie krótszy niż dla algorytmu naiwnego.
    - Zaproponuj wzorzec, dla którego zmierzony czas obliczenia tablicy przejścia automatu skończonego będzie co najmniej dwukrotnie dłuższy, niż czas potrzebny na utworzenie funkcji przejścia w algorytmie KMP.

1. [Tries and prefix trees](./lab2.ipynb)
    - Przyjmij następujący zbiór danych wejściowych:
      - bbb$
      - aabbabd
      - ababcd
      - abcbccd
      - załączony plik.
    - Upewnij się, że każdy łańcuch na końcu posiada unikalny znak (marker), a jeśli go nie ma, to dodaj ten znak.
    - Zaimplementuj algorytm konstruujący strukturę trie, która przechowuje wszystkie sufiksy łańcucha danego na wejściu.
    - Zaimplementuj algorytm konstruujący drzewo sufiksów w oparciu o algorytm McCreighta.
    - Upewnij się, że powstałe struktury danych są poprawne. Możesz np. sprawdzić, czy struktura zawiera jakiś ciąg znaków i porównać wyniki z algorytmem wyszukiwania wzorców.
    - Porównaj szybkość działania algorytmów konstruujących struktury danych dla danych z p. 1 w następujących wariantach:
      - Trie (1 pkt)
      - Drzewo sufiksów bez wykorzystania procedury fast_find oraz elementów "link" (1 pkt)
      - Drzewo sufiksów z wykorzystaniem procedury fast_find (3 pkty)
1. [Huffman encoding](./lab3.ipynb)
    - Zadanie polega na implementacji dwóch algorytmów kompresji:
      - statycznego algorytmu Huffmana (2 punkty)
      - dynamicznego algorytmu Huffmana (3 punkty)
    - Dla każdego z algorytmów należy wykonać następujące zadania:
      - Opracować format pliku przechowującego dane.
      - Zaimplementować algorytm kompresji i dekompresji danych dla tego formatu pliku.
      - Zmierzyć współczynnik kompresji (wyrażone w procentach: 1 - plik_skompresowany / plik_nieskompresowany) dla plików tekstowych o rozmiarach: 1kB, 10kB, 100kB, 1MB.
      - Zmierzyć czas kompresji i dekompresji dla plików z punktu 3.
1. [Edit distance and longest common subsequence](./lab4.ipynb)
    - Zaimplementuj algorytm obliczania odległości edycyjnej w taki sposób, aby możliwe było określenie przynajmniej jednej sekwencji edycji (dodanie, usunięcie, zmiana znaku), która pozwala w minimalnej liczbie kroków, przekształcić jeden łańcuch w drugi.
    - Na podstawie poprzedniego punktu zaimplementuj prostą wizualizację działania algorytmu, poprzez wskazanie kolejnych wersji pierwszego łańcucha, w których dokonywana jest określona zmiana. "Wizualizacja" może działać w trybie tekstowym. Np. zmiana łańcuch "los" w "kloc" może być zrealizowana następująco:
      - *k*los (dodanie litery k)
      - klo*c* (zamiana s->c)
    - Przedstaw wynik działania algorytmu z p. 2 dla następujących par łańcuchów:
      - los - kloc
      - Łódź - Lodz
      - kwintesencja - quintessence
      - ATGAATCTTACCGCCTCG - ATGAGGCTCTGGCCCCTG
    - Zaimplementuj algorytm obliczania najdłuższego wspólnego podciągu dla pary ciągów elementów.
    - Korzystając z gotowego tokenizera (np spaCy - https://spacy.io/api/tokenizer) dokonaj podziału załączonego tekstu na tokeny.
    - Stwórz 2 wersje załączonego tekstu, w których usunięto 3% losowych tokenów.
    - Oblicz długość najdłuższego podciągu wspólnych tokenów dla tych tekstów.
    - Korzystając z algorytmu z punktu 4 skonstruuj narzędzie, o działaniu podobnym do narzędzia diff, tzn. wskazującego w dwóch plikach linie, które się różnią. Na wyjściu narzędzia powinny znaleźć się elementy, które nie należą do najdłuższego wspólnego podciągu. Należy wskazać skąd dana linia pochodzi (< > - pierwszy/drugi plik) oraz numer linii w danym pliku.
    - Przedstaw wynik działania narzędzia na tekstach z punktu 6. Zwróć uwagę na dodanie znaków przejścia do nowej linii, które są usuwane w trakcie tokenizacji.
1. [2d patterns search](.lab5.ipynb)
    - Zaimplementuj algorytm wyszukiwania wzorca 2-wymiarowego
    - Znajdź w załączonym pliku "haystack.txt" wszyskie sytuacje, gdy taka sama litera występuje na tej samej pozycji w dwóch kolejnych linijkach. Zwróć uwagę, na nierówną długość linii w pliku.
    - Znajdź wszystkie wystąpienia "th" oraz "t h" w dwóch kolejnych liniach na tej samej pozycji.
    - Wybierz przynajmniej 4 litery (małe). Znajdź wszystkie wystąpienia tej litery w załączonym pliku "haystack.png"
    - Znajdź wszystkie wystąpienia słowa "p a t t e r n" w haystack.png.
    - Porównaj czas budowania automatu i czas wyszukiwania dla różnych rozmiarów wzorca
    - Podziel plik na 2, 4 i 8 fragmentów (w poziomie) i porównaj czas przeszukiwania 

