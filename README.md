
## SkyFall : Gesture Controlled Web based Game using Tensorflow Object Detection Api

> Control the game paddle by waving your hand in from of a web cam.

Skyfall is a physics based game in which users can control an onscreen paddle simply by moving their hands in front of a web cam. Light weight Convolutional Neural Networks are used to detect the users hands which is then mapped to the controls of the game. The structure of the interaction supports multiple players (provided they can be accommodated in the field of view of the camera). The system demonstrates how the integration of a well-trained and light weight hand detection model (treated as a first-class object in the interaction design) is used to robustly track player hands and enable “body as an input” interaction in real-time (~30 fps).

This approach can be expanded beyond the capabilities shown within SkyFall (which is a very early prototype). First it can be extended to allow integration of other types of models such as light-weight speech, language generation, generative models etc. The approach can leverage benefits from continuous improvements (better data, better optimizations) in each of these models. Finally, the approach can be expanded to allow for simultaneous integration of multiple pre-trained community models – e.g. a model trained to detect hands in addition to a model trained to detect raccoons in implementing a “raccoon catcher game on live video”.

## Installation

Install requirements.

```
pip install -r requirements.txt
```

## Run  Application

```
python webserver.py
```

View the game in your browser - `http://localhost:5005` 
