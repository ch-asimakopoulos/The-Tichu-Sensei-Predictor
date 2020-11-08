# The-Tichu-Sensei-Predictor
A Grand Tichu Decision bot named Sensei based on my diploma thesis. Give him 8 cards, the current score and your willingness to risk and the Sensei will share what he would do under the same circumstances, based on his experience on watching Tichu games unfold.

https://github.com/ch-asimakopoulos/Tichu-Sensei

https://github.com/ch-asimakopoulos/The-Tichu-Sensei

# Steps To Get the Sensei to wake up from his decades-long siesta and begin predicting Grand Tichu calls

- install python3
- install flask (eg. pip install flask)
- install numpy (eg. pip install numpy)
- install scikit learn (eg. pip install scikit-learn)
- install pickle (eg. pip install pickle-mixin)
- change the app.config['SECRET_KEY'] = "YOUR_SECRET_KEY" to an API key you want (do not share the key)
- create a settings.json based on settings-example.json
- make sure the svr_pred.pkl file is in the same folder as the tichu-sensei-predictor.py file
- run the file tichu-sensei-predictor.py from your terminal
- make a GET request to the flask server/predict endpoint using the following parameters
        - apikey - this is the secret key mentioned above
        - payload - this is a JSON file containing the following 
                    - "team_score": your team's score
                    - "opponent_team_score": your opponent's team score
                    - "cards": an array of 8 cards e.g ["Dr", "Ph", "SA", "G10", "B10", "B9", "S6", "G2"]
                    - "threshold": a value between 0 and 1. The closer to 0 it gets, the more aggressive calls the predictor   will make. The closer to 1, the safer the predictor will predict.
                    e.g
                    {
                    "team_score": 200,
                    "opponent_team_score": 300,
                    "threshold": 0.2,
                    "cards": ["Dr", "Ph", "SA", "G10", "B10", "B9", "S6", "G2"]
                    }
You can check the values cards can have by giving the tichu-sensei-predictor translate_hand function a peek :)
