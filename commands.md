__Aby uruchomić program, użyj polecenia:__ python -u „link do archiwum zip” -n „ścieżka do zapisu pliku”

__Aby uruchomić program jako docker kontener, użyj:__

1) docker build -t "Nazwa docker image" "Scieżka do pliku Docker"
2) docker run --name "Nazwa kontenera" -dt --env URL="Link do datasetu COCO" --mount type=bind,source="Scieżka do katalogu",target=/srv/coco/csv "Nazwa docker image"