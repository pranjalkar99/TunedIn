## Prerequisites

Make sure you have the following software installed:

- Python (version 3.6 or above)

## Installation

1. Clone the repository:

   ```shell
   $ git clone https://github.com/pranjalkar99/TunedIn.git
    
    ```

2. Then Install python Virtual environment:
 
    ```shell
    $ python -m venv env
    ```

    Activate the Virtual Environment:
    If you have Windows:
    ```shell
    $ ./env/Scripts/Activate
    ```
    If you have Mac/Linux:
    ```shell
    $ source /env/bin/activate
 
    ```
3. Install the dependencies:


```shell
$ pip install -r requirements.txt
```

4. Usage:

```shell
$ uvicorn main:app --reload --port 8000
```

                Then go to /docs for proper documentations of the apis



OR



To run and create Docker(Still in testing ):
```shell
docker-compose build
```
```shell
docker-compose up
```