# Python Based Station-Slave Program

This is a python based program that has a multi-thread supported server as well as client. 
It is designed for the purpose of handling multiple raspberrypi with a single server.
It is also integrated with rollbar and logger to report if encourter any problem.

It has the following functionalities:

1. The Server can connect to multiple clients.
2. The Server can receive multiple requests from different clients without waiting.
3. The clients can receive responses from server without being in holding state.
4. The Server can broadcast responses to all clients.
5. The Server can send response to a specific client as well.
