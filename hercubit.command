#! /bin/bash
echo "Hercubit is starting up!  :)"
echo " "
cd  "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "../../../"

# 

source venv/bin/activate
echo Updating to latest version of Hercubit
# git add saved/
# git commit -m "adding raw_data"
git pull
# git push origin master

python Website2/app.py
