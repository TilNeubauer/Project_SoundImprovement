# Docker Starten 

## Voraussetzungen
1. Docker Desktop
2. WSL2 + Ubuntu in WSL
3. In Docker Desktop WSL Integration für Ubuntu aktivieren 

### WSL2 + Ubuntu in WSL
1. Wenn WSL noch nicht installiert ist:\
    in PowerShell:
    ```
    wsl --install
    ```

2. Prüfen ob Ubuntu in WSL vorhanden:\
    in PowerShell als Admin:
    ```
    wsl -l -v
    ```

3. Wenn Ubuntu nicht vorhanden ist: \
    in PowerShell :
    ```
    wsl --install -d Ubuntu
    ```


4. Wenn Ubuntu in Version 1 vorhanden ist: \
    in PowerShell :
    ```
    wsl --set-version Ubuntu 2
    ```



### In Docker Desktop WSL Integration für Ubuntu aktivieren

1. Docker Desktop öffnen

2. Settings (Zahnrad) → Resources → WSL Integration

3. Aktivieren:

    ✅ Enable integration with my default WSL distro

    ✅ Ubuntu in der Liste anhaken


## Docker bauen 
In Verzeichnis des Projektes wechseln: 
```
docker build -t mygui:latest .
```

## Image laden (.tar)
1. In Verzeichniss von <mygui_latest.tar> wechseln \
    Bsp für Downlods Ordner:\
    in Bash :
    ```
    cd /mnt/c/Users/<NAME>/Downloads
    ```


2. Docker laden:\
    in Bash :
    ```
    docker load -i mygui_latest.tar
    ```

3. Prüfen ob Docker vorhanden:\
    in Bash :
    ```
    docker images
    ```


## Container starten (GUI + Audio über WSLg)
In Ubuntu (WSL) starten:

```
docker run --rm -it \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /mnt/wslg:/mnt/wslg \
    -e XDG_RUNTIME_DIR=/mnt/wslg/runtime-dir \
    -e PULSE_SERVER=unix:/mnt/wslg/PulseServer \
    mygui:latest
```

## Cotainer einfacher Start (nicht Robust): 
Mithilfe von <docker-compose.yml> \
In Ubuntu (WSL) starten:
```
docker compose up
```