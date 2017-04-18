# pybot

Wrapper for python-telegram-bot to allow dynamic plug-in architecture, an attempt to make python-telegram-bot more hubottish.

### Execution flow

1. `bin/pybot` starts the bot with the selected adapter and using the configuration options defined in `conf/pybot.conf` or the command-line arguments.

1. The selected adapter receives the message and sends it to the `brain.py`.

1. The `brain.py` loads in runtime all the `.py` files in the `./memory` folder each time and try to execute a defined method, for example `hear(message.text)`.

1. Each module in `./memory` with that method returns a response, the `brain.py` sends it to the `pybot.py` and it sends the response back to the chat.

* As the methods are dynamically loaded, you can edit and add the files in `./memory` without need to restart `pybot.py`, and they will be reloaded on the next message. Overkill but funny.

### Makefile targets

```Makefile
usage:             Show this help
setup-venv:        Setup virtualenv
lint:              Run code linter to check code style
telegram:          Run pybot with the telegram adapter
docker-build:      Build the docker image for running pybot
docker-telegram:   Run with telegram adapter in the docker container
docker-lint:       Run pep8 in the docker container
docker-clean:      Remove the docker image
```

### Execution example

````bash
make docker-telegram
````

```
docker run -it --rm --name pybot -v /Users/rael/Code/python/pybot:/usr/src/pybot -w /usr/src/pybot 'pybot' bin/pybot telegram
Starting pybot using conf token file. CTRL-C to quit.
2017-04-17 07:35:54,392 - pybot.interfaces.telegram - INFO - Bot raelbot up and ready!
2017-04-17 07:36:39,371 - pybot.brain - INFO - 116133952, Hello world!, 53693428, 2017-04-17 07:36:39,"53693428";
```

### Contributing

Contributions of all sizes are welcome. 

### License

You may copy, distribute and modify the software provided that modifications are described and licensed for free under `LGPL-3 <https://www.gnu.org/licenses/lgpl-3.0.html>`_. Derivatives works (including modifications or anything statically linked to the library) can only be redistributed under LGPL-3, but applications that use the library don't have to be.
