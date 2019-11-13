for i in {0..3}
do
    python3 process.py < $i.txt >$i.json
done
