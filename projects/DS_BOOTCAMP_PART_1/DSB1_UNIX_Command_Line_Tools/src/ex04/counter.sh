JUNIOR=0
MIDDLE=0
SENIOR=0
echo $JUNIOR > temp_jun.txt
echo $MIDDLE > temp_mid.txt
echo $SENIOR > temp_sen.txt


echo "name","count" > hh_uniq_positions.csv
tail -n+2 ../ex03/hh_positions.csv | while read line; do
    elem3="$(echo "$line" | awk -F ',' '{print $3}')"

    case $elem3 in
        *"Junior"*)
            JUNIOR=$(($JUNIOR+1))
            echo $JUNIOR > temp_jun.txt
            ;;
        *"Middle"*)
            MIDDLE=$(($MIDDLE+1))
            echo $MIDDLE > temp_mid.txt
            ;;
        *"Senior"*)
            SENIOR=$(($SENIOR+1))
            echo $SENIOR > temp_sen.txt
            ;;
    esac
done 


JUNIOR="$(cat temp_jun.txt)"
MIDDLE="$(cat temp_mid.txt)"
SENIOR="$(cat temp_sen.txt)"
rm -f temp_jun.txt temp_mid.txt temp_sen.txt
echo "\"Junior\",$JUNIOR" >> hh_uniq_positions.csv
echo "\"Middle\",$MIDDLE" >> hh_uniq_positions.csv
echo "\"Senior\",$SENIOR" >> hh_uniq_positions.csv

