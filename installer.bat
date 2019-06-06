pyinstaller --name tetris ^
    --onefile --nowindow ^
    --add-data="img;img" ^
    --add-data="sounds;sounds" ^
    --add-data="bgm;bgm" ^
	--icon=img\tetrisIcon.ico ^
    main.py