head -n1 ../ex01/hh.csv > hh_positions.csv
tail -n+2 ../ex02/hh_sorted.csv | while read line; do
    elem1="$(echo "$line" | awk -F '",' '{print $1}')"
    elem2="$(echo "$line" | awk -F '",' '{print $2}')"
    elem3="$(echo "$line" | awk -F '",' '{print $3}')"
    # elem4="$(echo "$line" | awk -F ',"' '{print $4}')"
    elem5="$(echo "$line" | awk -F '",' '{print $4}')"
    # echo "$elem"
    case "$elem3" in
        *"Junior/Middle"*)
            echo "$elem1,$elem2,\"Junior/Middle\",$elem5"
            ;;
        *"Middle/Senior"*)
            echo "$elem1,$elem2,\"Middle/Senior\",$elem5"
            ;;
        *"Junior"*)
            echo "$elem1,$elem2,\"Junior\",$elem5"
            ;;
        *"Middle"*)
            echo "$elem1,$elem2,\"Middle\",$elem5"
            ;;
        *"Senior"*)
            echo "$elem1,$elem2,\"Senior\",$elem5"
            ;;
        *)
            echo "$elem1,$elem2,\"-\",$elem5"
            ;;
    esac >> hh_positions.csv
done