# SPECTRE

## Getting Started

### Install pyenv

[Pyenv](https://github.com/pyenv/pyenv) is a package that makes it easier to work with Python virtual environments. Follow the [installation instructions](https://github.com/pyenv/pyenv#installation) in the README.

Using [Homebrew](brew.sh) is the easiest way to install. Install brew with:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Then install pyenv:

```
brew install pyenv
```

#### Autoload pyenv

Pyenv has to be initialized when you open a terminal, so you need to add a few things to your .bash_profile file:

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
```

### Install pyenv-virtualenv

[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) is a package to help create and activate Python virtual environments within pyenv. Follow the [installation instructions](https://github.com/pyenv/pyenv-virtualenv#installation) in the README.

It is easiest to install with [Homebrew](brew.sh):

```
brew install pyenv-virtualenv
```

#### Autoload pyenv-virtualenv

Pyenv-virtualenv also has to be initialized when you open a terminal, so you need to add a few things to your .bash_profile file:

```
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
exec "$SHELL"
```

### Install Mac command line tools

```
xcode-select --install
```

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

Navigate to the [url](http://127.0.0.1:8000/) specified above in your browser. You should see a message indicating that everything is working.

### Django tutorial

If you'd like to get started with Django, visit the [tutorial](https://docs.djangoproject.com/en/2.0/intro/tutorial01/).


