git pull --force

if ! cmp requirements.txt requirements.super.txt >/dev/null 2>&1
then
  echo -e "\e[93mDetected changes in requirements, reinstalling packages..."
  echo -e "\e[93mCopying requirements.txt to requirements.super.txt..."
  cp requirements.txt requirements.super.txt
  echo -e "\e[92mDone"
  echo -e "\e[93mInstalling packages..."
  if pip install -r requirements.txt
  then
    echo "\e[92Done."
  fi
fi

sudo service unit reload
sudo service nginx reload