# Floydhub Deployment Demo
Serving a car brand classification model for production with FloydHub

## Prerequisites
1. Visit [Floydhub](https://www.floydhub.com/) to create an account if you do not have one.
2. Install `Floyd CLI` with pip using this command:
```bash
$ pip install floyd-cli
```

And now prepare to get your hands dirty.

<!-- ## Preparation -->

## Car brand classification

#### Used dataset
[**Stanford Car dataset**](https://ai.stanford.edu/~jkrause/cars/car_dataset.html) contains 16,185 images of 196 classes of cars. The data is split into 8,144 training images and 8,041 testing images, where each class has been split roughly in a 50-50 split. Classes are typically at the level of Make, Model, Year, e.g. 2012 Tesla Model S or 2012 BMW M3 coupe.

Citation: 
```
@inproceedings{KrauseStarkDengFei-Fei_3DRR2013,
  title = {3D Object Representations for Fine-Grained Categorization},
  booktitle = {4th International IEEE Workshop on  3D Representation and Recognition (3dRR-13)},
  year = {2013},
  address = {Sydney, Australia},
  author = {Jonathan Krause and Michael Stark and Jia Deng and Li Fei-Fei}
}
```

#### Make prediction locally on console
1. Clone the repository
2. Download [pretrained-model](https://drive.google.com/file/d/1SAq5DGwB_Y-WEnxkAs6k8y4AVz5N7fTI/view?usp=sharing)
3. Install required libs: `pip install requirements.txt`
4. Run `python inference.py`

## Deploy
1. Log your FloydHub account in with `floyd login`, then new browser tab will be opened and all you need to do next is following the instructions.
2. Create new dataset on FloydHub and upload your model (follow these [steps](https://docs.floydhub.com/guides/create_and_upload_dataset/)). Remember the dataset link you just created to use it later in the configuration file. I named it `car_model` so my model is stored at `sudohainguyen/datasets/car_model/1`.
3. Replace existing link at `source` attribute in `floyd.yml`.
4. Run `floyd run --task serve` and wait for ~1 mins before making any further requests.

## Demo
Once your Floyd project is ready, make a simple POST request to see how it actually works by the following command: 
```bash
$ curl -F "file=<local-image-path>" https://www.floydlabs.com/serve/<username>/projects/demo/predict
```
And here is what we should get back for example:
```bash
{
    "prediction": "Aston Martin Virage Coupe 2012"
}
```