temp_file_name="$(sed -n '2p' ../ex03/hh_positions.csv | awk -F ',' '{print $2}')"
temp_file_name="$(echo $temp_file_name | awk '{print substr($0,2,10)}')"
echo $temp_file_name > temp.txt

tail -n+2 ../ex03/hh_positions.csv | while read line; do
    elem3="$(echo "$line" | awk -F ',' '{print $2}')"
    date_val="$(echo $elem3 | awk '{print substr($0,2,10)}')"
    if [ $date_val \> "$(cat temp.txt)" ]; then
        echo $date_val > temp.txt
    fi
    head -n1 ../ex01/hh.csv > "$(cat temp.txt).csv"
done 

temp_file_name="$(sed -n '2p' ../ex03/hh_positions.csv | awk -F ',' '{print $2}')"
temp_file_name="$(echo $temp_file_name | awk '{print substr($0,2,10)}')"
echo $temp_file_name > temp.txt

tail -n+2 ../ex03/hh_positions.csv | while read line; do
    elem3="$(echo "$line" | awk -F ',' '{print $2}')"
    date_val="$(echo $elem3 | awk '{print substr($0,2,10)}')"
    if [ $date_val \> "$(cat temp.txt)" ]; then
        echo $date_val > temp.txt
    fi
    echo "$line" >> "$(cat temp.txt).csv"
done 

rm temp.txt