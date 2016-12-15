while read KALE
do
    NEW=`echo $KALE | tr " " _`
    mv "$KALE" $NEW
done < <(ls *webm)
