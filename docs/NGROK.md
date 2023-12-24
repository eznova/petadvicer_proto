
### Windows
- Скачайте [архив ](https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip)
- Распакуйте в удобную директорию
- Запустите в командной строке
```bash
# замените токен на свой, этот используется в демонстрационных целях
.\ngrok.exe authtoken 2ZobFmUOL8eSQzD8XmCon6ouZ9m_4fGoFa3a2G3QbbQ2cgR1c
```

### Linux (Collab)
```bash
# замените токен на свой, этот используется в демонстрационных целях
! export ngrok_token="2ZobFmUOL8eSQzD8XmCon6ouZ9m_4fGoFa3a2G3QbbQ2cgR1c"
!wget -c https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
!unzip -f ngrok-stable-linux-amd64.zip
!./ngrok authtoken $ngrok_token
```

### Linux
```bash
# замените токен на свой, этот используется в демонстрационных целях
export ngrok_token="2ZobFmUOL8eSQzD8XmCon6ouZ9m_4fGoFa3a2G3QbbQ2cgR1c"
wget -c https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip -f ngrok-stable-linux-amd64.zip
./ngrok authtoken $ngrok_token
```