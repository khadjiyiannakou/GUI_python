for i in `ls *webm`
do
    FIL=`echo "$i" | cut -f1 -d'.'`
    ffmpeg -i $FIL.webm -q:a 0 -map a $FIL.mp3
done
