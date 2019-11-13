@echo off
for /l %%n in (1,1,3) do (
	echo %%n
	python process.py < %%n.txt > %%n.json
)