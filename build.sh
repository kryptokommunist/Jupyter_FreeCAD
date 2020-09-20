sudo add-apt-repository -y ppa:freecad-maintainers/freecad-stable
sudo apt-get -y update
sudo apt-get -y install freecad-python3 python3-pivy
pip install jupyter

pip install -r requirements.txt
pip install runipy
runipy 'FreeCAD inside Jupyter Notebook - Examples.ipynb' --html report.html 
