for dir in *
do
    if [ -d "$dir" ]
    then
        count=1
        echo "removing duplicates from $dir"
        for line in "$(fdupes "$dir")"
        do
            if [ $((count%2)) -eq 0 ]
            then
                rm "$line"
            fi
            ((count++))
        done
    fi
done
