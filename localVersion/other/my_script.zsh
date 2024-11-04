rm -rf utils/documentation/requirements.txt
rm -rf utils/documentation/tree.txt


cd ../..

pip3 freeze > utils/documentation/requirements.txt


tree > utils/documentation/tree.txt