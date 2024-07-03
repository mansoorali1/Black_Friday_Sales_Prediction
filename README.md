# Black_Friday_Sales_Prediction
This project provides an end-to-end MLOps solution for predicting Black Friday Sales. Given specific input features such as Gender, Age, Occupation and etc., the model predicts the Sales Amount. The solution is fully hosted on AWS, leveraging various AWS services for seamless deployment and scalability.

**Project is in Progress**

## Table of Contents
- [Architecture](#architecture)
- [Languages & Tools](#languages--tools)
- [Directory Structure](#directory-structure)
- [Data](#data)
- [Output](#output)

## Architecture
1. Data Ingestion: The data is stored in a MongoDB database and is fetched from there for processing.

2. Data Preprocessing: Data cleaning and transformation are performed to prepare the data for model training.

3. Model Training: Various models are trained on the preprocessed data such as Linear, Ridge, Lasso Regression, KNN Regression, Random Forest Regression, XGBoost Regression and few others.

4. Model Evaluation: Among the different models Random Forest and XGBoost were the top performers.

5. Deployment: In the deployment phase, the selected model is uploaded to an AWS S3 bucket. FastAPI is used to build the API. A containerized application is created using Github Action, and the Docker image is pushed to Amazon Elastic Container Registry (ECR). This image is then pulled into an EC2 instance, which is connected to GitHub via a self-hosted runner. Whenever code changes or new code is pushed to GitHub, the CI/CD pipeline is triggered, ensuring that the model is continuously integrated and deployed on AWS
## Languages & Tools
<div align="">
  <a href="https://www.python.org" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="60" height="60"/>
  </a>
  <a href="https://www.mongodb.com" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mongodb/mongodb-original-wordmark.svg" alt="mongodb" width="60" height="60"/>
  </a>
  <a href="https://code.visualstudio.com" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/vscode/vscode-original.svg" alt="vscode" width="60" height="60"/>
  </a>
  <a href="https://aws.amazon.com/s3/" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" alt="aws s3" width="60" height="60"/>
  </a>
  <a href="https://www.docker.com/" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="60" height="60"/>
  </a>
  <a href="https://fastapi.tiangolo.com" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/fastapi/fastapi-original.svg" alt="fastapi" width="60" height="60"/>
  </a>
  <a href="https://github.com/features/actions" target="_blank" rel="noreferrer">
    <img src="https://avatars.githubusercontent.com/u/44036562?s=200&v=4" alt="github actions" width="60" height="60"/>
  </a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/HTML" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html" width="60" height="60"/>
  </a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/CSS" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css" width="60" height="60"/>
  </a>
</div>
## Directory Structure
```
C:.
│   .dockerignore
│   .gitignore
│   app.py
│   demo.py
│   demo2.py
│   Dockerfile
│   LICENSE
│   README.md
│   requirements.txt
│   setup.py
│   template.py
│
├───.github
│   └───workflows
│           aws.yaml
│
│
├───black_friday
│   │   __init__.py
│   │
│   ├───cloud_storage
│   │       aws_storage.py
│   │       __init__.py
│   │   
│   │
│   ├───components
│   │       data_ingestion.py
│   │       data_transformation.py
│   │       data_validation.py
│   │       model_evaluation.py
│   │       model_pusher.py
│   │       model_trainer.py
│   │       __init__.py
│   │   
│   │
│   ├───configuration
│   │       aws_connection.py
│   │       mongo_db_connection.py
│   │       __init__.py
│   │   
│   │
│   ├───constants
│   │       __init__.py
│   │   
│   │
│   ├───data_access
│   │       blackfriday_data.py
│   │       __init__.py
│   │   
│   │
│   ├───entity
│   │       artifact_entity.py
│   │       config_entity.py
│   │       estimator.py
│   │       s3_estimator.py
│   │       __init__.py
│   │   
│   │
│   ├───exception
│   │       __init__.py
│   │   
│   │
│   ├───logger
│   │       __init__.py
│   │   
│   │
│   ├───pipeline
│   │       prediction_pipeline.py
│   │       training_pipeline.py
│   │       __init__.py
│   │   
│   │
│   ├───utils
│           main_utils.py
│           __init__.py
│      
│
│
├───config
│       model.yaml
│       schema.yaml
│
│
├───notebook
│       Feature_Engineering_and_Model_Training.ipynb
│       mongoDB.ipynb
│       Pipeline testing.ipynb
│       Untitled.ipynb
│
├───static
│   ├───css
│   │       style.css
│   │
│   └───images
│           bfriday_pic.jpg
│
├───templates
        blackfriday.html

```

## Data
[Dataset](https://github.com/mansoorali1/Black_Friday_Sales_Prediction/blob/main/Data/train.csv)
## Output
![Black Friday Sales_Prediction_App](https://github.com/mansoorali1/Black_Friday_Sales_Prediction/assets/73877240/925ed935-f713-4807-bc65-7d6df655c2e7)

**Youtube URL Deployment https://youtu.be/IbOM4Vc8dQo**
