source ~/.zshrc
cd ~/python/frc-livescore/examples
source ../bin/activate
while true
do
   python3 -u live3.py Archimedes 55572 > Archimedes.out 2>&1 
done
