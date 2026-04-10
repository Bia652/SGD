# Sistema de Gestão de Dados  - Trabalho Prático

We suggest that you use the [virtualenv](https://virtualenv.pypa.io/en/latest/).
You can install virtualenv, and the corresponding libraries with the following commands:

```console
$ python3 -m venv proj_sgd_env # the name of the virtualenv is proj_sgd_env, but you can change it
$ source proj_sgd_env/bin/activate
$ pip3 install flask
$ pip3 install jwt
$ pip3 install psycopg2-binary
$ python3 demo-api-sgd.py # this command is to run the flask application
--> Ctrl+C to stop
$ deactivate # to stop the virtualenv
```

The install commands are only needed when creating the virtualenv.
The following times, you just need to activate it, and run the `demo-api-sgd.py`.

* Web browser access: http://localhost:8080 (initial application page. For the remaining endpoints, use [Postman](../postman)).


## Issues with the computer architecture

Depending on the computer architecture that you have in your computer, you may face some issues installing psycopg2.
This happens especially if you have Apple M1 Pro or Apple M2 Pro.

To fix it, install the following libraries:

```
brew install openssl
brew --prefix openssl
brew install libpq
```

With the result of `brew --prefix openssl`, you will see the location that openssl was installed. 
In my case, I got `/opt/homebrew/opt/openssl@3`. 
If you have something different, replace the path in the following commands:

```
export LDFLAGS="-L/opt/homebrew/opt/openssl@3/lib -L/opt/homebrew/opt/libpq/lib"
export CPPFLAGS="-L/opt/homebrew/opt/openssl@3/include -L/opt/homebrew/opt/libpq/include"
```

After that, install the `psycopg2-library`. You may have a different python version. In that case, replace properly:

```
python3.13 -m pip install psycopg2-binary
```

This link may be useful: https://stackoverflow.com/questions/66888087/cannot-install-psycopg2-with-pip3-on-m1-mac


## Authors
* SGD 2024 Team
* University of Coimbra

