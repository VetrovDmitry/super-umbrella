export APP_MODE="prod"
source env/Scripts/activate
source .env

export FLASK_APP=app

export APP_MODE=$1

if [ $APP_MODE == "dev" ] || [ $APP_MODE == "test" ]
then
  export FLASK_DEBUG=1
  export FLASK_ENV='development'
fi


flask run