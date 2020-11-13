import sys

from flask_server import app
import logging



application = app.create_app()



def main():
    
    host = '0.0.0.0' if len(sys.argv) <= 1 else sys.argv[1]
    application.run(host=host, port='12345', debug=True, threaded=True,
                    ssl_context=('certificates/cert.pem',
                                 'certificates/key.pem'))

if __name__ == '__main__':
    log_handler = logging.FileHandler('flask_server.log')
    log_handler.setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').addHandler(log_handler)

    application.logger.addHandler(log_handler)
    application.logger.setLevel(logging.DEBUG)
    main()
