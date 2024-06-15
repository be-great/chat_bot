if [ ! -d "venv" ]; then
    echo --------------------
    echo Creating virtualenv
    echo --------------------
    virtualenv venv
fi
source venv/bin/activate

pip install -r requirements.txt
# Run rasa in the background using nohup
nohup rasa run > rasa_output.log 2>&1 &

# Run train_data.py in the background using nohup
nohup python3 train_data.py > train_data_output.log 2>&1 &

# Wait for both processes to start
sleep 2

echo "Both rasa and train_data.py are running in the background."