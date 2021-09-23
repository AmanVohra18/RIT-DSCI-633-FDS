{"metadata":{"language_info":{"name":"python","version":"3.6.4","mimetype":"text/x-python","codemirror_mode":{"name":"ipython","version":3},"pygments_lexer":"ipython3","nbconvert_exporter":"python","file_extension":".py"},"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# This Python 3 environment comes with many helpful analytics libraries installed\n# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python\n# For example, here's several helpful packages to load in \n\n# Input data files are available in the \"../input/\" directory.\n# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory\n\nfrom subprocess import check_output\nprint(check_output([\"ls\", \"../input\"]).decode(\"utf8\"))\n\n# Any results you write to the current directory are saved as output.\n\n\n# -*- coding: utf-8 -*-\n\n\n# Part 1 - Preprocessing the data\n\n# Importing the Libraries\nimport numpy as np\nimport pandas as pd\n\n\n# Importing the test dataset\ndataset_test = pd.read_csv('../input/test.csv')\n\n# Importing the training dataset\ndataset_train = pd.read_csv('../input/train.csv')\n\n# Joining both datasets\ndf1 = pd.DataFrame(dataset_train)\ndf2 = pd.DataFrame(dataset_test)\ndataset_joined = [df1, df2]\ndataset_joined = pd.concat(dataset_joined)\n\n\n# Cleaning the data\n\n# removing everything from the names before the comma and after the dot, so we have only titles\ndataset_joined['Name'] = dataset_joined['Name'].str.split(',').str[1]\ndataset_joined['Name'] = dataset_joined['Name'].str.split('.').str[0]        \n\n# droping irrelevant data\ndataset_joined.drop(['Ticket', 'Cabin' ], axis = 1, inplace = True)\n\n# Filling nan values Embarked with 'S', the most relevant data\ndataset_joined['Embarked'].fillna('S', inplace=True)\n\ndataset_joined.info()\n\n\n\n# Enconding Categorical Data\n\n# Categorizing the 'Name' data by treatment hierarquy and gender segregation\nnames = dataset_joined['Name'].copy()\nfor item in names:\n    if (item == ' Mr'):\n        names.replace(item, 1, inplace = True)\n    elif (item == ' Miss' or item == ' Mrs'):\n        names.replace(item, 0, inplace = True)\n    elif (item == ' Capt' or item == ' Col' or item == ' Don' or item == ' Dona' or item == ' Dr' or item == ' Jonkheer' or item == ' Lady' or item == ' Major' or item == ' Master' or item == ' Mile' or item == ' Mlle' or item == ' Mme' or item == ' Ms' or item == ' Rev' or item == ' Sir' or item == ' the Countess'):\n        names.replace(item, 2, inplace = True)\n    \ndataset_joined['Name'] = names\n\n\n\n\nfrom sklearn.preprocessing import LabelEncoder\n\nlabelencoder_sex = LabelEncoder()\ndataset_joined['Sex'] = labelencoder_sex.fit_transform(dataset_joined['Sex'])\n\nlabelencoder_embarked = LabelEncoder()\ndataset_joined['Embarked'] = labelencoder_embarked.fit_transform(dataset_joined['Embarked'])\n\n\n\n# Estimating and updating Age and Fare for the null values on dataset\n\n\n# Getting average Age and Fare\n# There are two genders and three passenger classes in this dataset. \n# So we create a 2 by 3 matrix to store the median values.\n \n# Create a 2 by 3 matrix of zeroes\nmedian_ages = np.zeros((2,3))\nmedian_fares = np.zeros((2,3))\n \n# For each cell in the 2 by 3 matrix\nfor i in range(0,2):\n    for j in range(0,3):\n \n    \t# Set the value of the cell to be the median of all `Age` values\n    \t# matching the criterion 'Corresponding gender and Pclass',\n    \t# leaving out all NaN values\n        median_ages[i,j] = dataset_joined[ (dataset_joined['Sex'] == i) & \\\n                               (dataset_joined['Pclass'] == j+1)]['Age'].dropna().median()\n        median_fares[i,j] = dataset_joined[ (dataset_joined['Sex'] == i) & \\\n                               (dataset_joined['Pclass'] == j+1)]['Fare'].dropna().median()\n\n# Create new columns AgeFill and FareFill to put values into. \n# This retains the state of the original data.\ndataset_joined['AgeFill'] = dataset_joined['Age']\ndataset_joined[ dataset_joined['Age'].isnull()][['Age', 'AgeFill', 'Sex', 'Pclass']]\ndataset_joined['FareFill'] = dataset_joined['Fare']\ndataset_joined[ dataset_joined['Fare'].isnull()][['Fare', 'AgeFill', 'Sex', 'Pclass']]\n\n# Put our estimates into NaN rows of new columns AgeFill and FareFill.\n# df.loc is a purely label-location based indexer for selection by label.\n \nfor i in range(0, 2):\n    for j in range(0, 3):\n \n    \t# Locate all cells in dataframe where `Sex` == i, `Pclass` == j+1\n    \t# and `Age` == null and 'Fare' == null. \n    \t# Replace them with the corresponding estimate from the matrix.\n        dataset_joined.loc[ (dataset_joined.Age.isnull()) & (dataset_joined.Sex == i) & (dataset_joined.Pclass == j+1),\\\n                 'AgeFill'] = median_ages[i,j]\t\n        dataset_joined.loc[ (dataset_joined.Fare.isnull()) & (dataset_joined.Sex == i) & (dataset_joined.Pclass == j+1),\\\n                 'FareFill'] = median_fares[i,j]\t\n        \n\n# Create a feature that records whether the Age was originally missing\ndataset_joined['AgeIsNull'] = pd.isnull(dataset_joined['Age']).astype(int)\ndataset_joined['FareIsNull'] = pd.isnull(dataset_joined['Fare']).astype(int)\ndataset_joined.head()\n\n\n# Now we remove the null values from the test dataset and we clean the columns Age and Fare\ndataset_joined.drop(['Age', 'Fare' ], axis = 1, inplace = True)\n\n# Filling no Survived data with -1\ndataset_joined['Survived'].fillna(-1, inplace=True)\n\ndataset_joined.info()\n\n\n\n# The 'Embarked', 'Name' and 'Pclass' columns has several types of data, with no value Hierarchy, so we need to\n# create dummy variables and exclude 1 one of them to avoid the dummy variable trap\n\ndataset_joined = pd.get_dummies(dataset_joined, columns=['Embarked', 'Name', 'Pclass'], drop_first=True)\n\n\n# Splitting the dataset into Train and Test\ndataset_train_revised = dataset_joined.iloc[:891, :]\ndataset_test_revised = dataset_joined.iloc[891:, :]\n\n# Splitting the dataset into the input and output\nX_train = dataset_train_revised.iloc[:,[0,2,3,5,6,9,10,11,12,13,14]]\ny_train = dataset_train_revised.iloc[:, [4]]\nX_test = dataset_test_revised.iloc[:,[0,2,3,5,6,9,10,11,12,13,14]]\n\n#getting the PassIndex for the Submission dataset\npass_index = dataset_joined.iloc[891:,1]\n\n# Feature Scaling\nfrom sklearn.preprocessing import StandardScaler\nsc = StandardScaler()\nX_train = sc.fit_transform(X_train)\nX_test = sc.fit_transform(X_test)\n\n\n\n# Part 2 - Now let's make the ANN!\n\n# Importing the Keras libraries and packages\nimport numpy\nimport keras\nfrom keras.models import Sequential\nfrom keras.layers import Dense\nfrom keras.optimizers import SGD\n\n# fix random seed for reproducibility\nseed = 7\nnumpy.random.seed(seed)\n\n# Initialising the ANN\nclassifier = Sequential()\n\n# Adding the input layer and the first hidden\nclassifier.add(Dense(15, activation = 'tanh', input_dim = 11))\n\n# Adding the output layer\nclassifier.add(Dense(1, activation = 'sigmoid'))\n\n# Compiling the ANN\noptimizer = SGD(lr = 0.01, momentum = 0.9)\nclassifier.compile(optimizer = optimizer, loss = 'binary_crossentropy', metrics = ['accuracy'])\n\n# Fitting the ANN to the Training set\nclassifier.fit(X_train, y_train, batch_size = 10, epochs = 50)\n\n\n\n\n\n# Part 3 - Making predictions and evaluating the model\n\n# Predicting the Test set results\ny_pred = classifier.predict(X_test)\n\n# We now consider any prediction >0.5 as 1 and <=0.5 as 0\ny_pred = np.round_(y_pred,0)\n\n\n\n#Part 4 - Generating Submission File\nonly_final_values = pd.read_csv('../input/test.csv')\nonly_final_values['Survived'] = y_pred\nonly_final_values = only_final_values.iloc[: , [0,11]]\nonly_final_values['Survived'] = only_final_values['Survived'].astype(np.int64)\nonly_final_values.to_csv('titanic_submission.csv', index = False)\n","metadata":{"collapsed":false,"_kg_hide-input":false,"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2021-09-23T02:55:33.952101Z","iopub.execute_input":"2021-09-23T02:55:33.952423Z","iopub.status.idle":"2021-09-23T02:55:45.207207Z","shell.execute_reply.started":"2021-09-23T02:55:33.952375Z","shell.execute_reply":"2021-09-23T02:55:45.206359Z"},"trusted":true},"execution_count":1,"outputs":[]}]}