rm -rf docs/requirements.txt
rm -rf docs/tree.txt


cd ../..

pip3 freeze > docs/requirements.txt


tree > docs/tree.txt