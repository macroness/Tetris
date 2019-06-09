pyinstaller --name tetris \
    --onefile --windowed \
    --add-data="img:img" \
    --add-data="sounds:sounds" \
    --add-data="bgm:bgm" \
	--add-data="fonts:fonts" \
	--icon=img\tetrisIcon.ico \
    main.py