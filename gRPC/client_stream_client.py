import grpc

import gRPC.proto.grpc_pb2 as pb2
import gRPC.proto.grpc_pb2_grpc as pb2_grpc


class ClientStreamClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        # instantiate a channel
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.GRPCServiceStub(self.channel)

    def make_message(self, message):
        return pb2.Message(
            message=message
        )

    def generate_messages(self):
        messages = [
            self.make_message("First message"),
            self.make_message("Second message"),
            self.make_message("Third message"),
            self.make_message("Fourth message"),
            self.make_message("Fifth message"),
        ]

        for msg in messages:
            yield msg

    def send_message(self):
        response = self.stub.request_stream(self.generate_messages())
        print("Hello from the server received your %s" % response.message)


if __name__ == '__main__':
    client = ClientStreamClient()
    client.send_message()
