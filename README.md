# cokolwiek

#### instalowanie zależności

Dobrze jest używać [vitrualenva](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)

Żeby zainstalować zależności, wystarczy w terminalu wykonać komendę:

```
pip install -r requirements.txt
```

#### uruchamianie testów

```
python -m unittest discover
```

Testy zakładają, że w katalogu `tests/TestData` są odpowiednie pliki testowe.
