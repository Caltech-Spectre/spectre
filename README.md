# SPECTRE

## Getting Started

### Install pyenv

[Pyenv](https://github.com/pyenv/pyenv) is a package that makes it easier to work with Python virtual environments. Follow the instructions on the github README for installing.

### Install pyenv-virtualenv

[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) is a package to help create and activate Python virtual environments within pyenv. Follow the instructions on the github README for installing.

### Install python 3

Install python 3.6.4 into pyenv:

```bash
pyenv install 3.6.4
```


### Checkout Spectre

Check out this repository onto your Mac:

```
git clone https://github.com/caltech-spectre/spectre
```

### Create a virtual environment for Spectre

Use pyenv to create a virtual environment:

```
pyenv virtualenv 3.6.4 spectre
```

In the spectre folder, activate the spectre virtual environment:

```
cd spectre
pyenv local spectre
```

### Populate the virtual environment

Install the required python modules:

```
pip install -r requirements.txt
```

### Test the install

To verify that everything is installed properly, run the Django development server:

```
python manage.py runserver
```

It will display the following information:

```
April 08, 2018 - 23:31:35
Django version 2.0.4, using settings 'spectre.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Navigate to the url specified above in your browser. You should see a message indicating that everything is working.




