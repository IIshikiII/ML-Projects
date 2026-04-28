rm -f concatenated.csv
files="$(ls | grep .csv | sort)"
first_file="$(echo $files | awk '{print substr($0,0,14)}')"
head -n1 "$first_file" > concatenated.csv

for file in $files; do
    tail -n+2 "$file" >> concatenated.csv
done