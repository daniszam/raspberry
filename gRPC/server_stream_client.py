import grpc

import gRPC.proto.grpc_pb2 as pb2
import gRPC.proto.grpc_pb2_grpc as pb2_grpc


class ServerStreamClient(object):
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

    def get_url(self):
        """
        Client function to call the rpc for GetServerResponse
        """
        message = pb2.Message(message="hello from client")
        messages = self.stub.response_stream(message)

        for feature in messages:
            print(feature)


if __name__ == '__main__':
    client = ServerStreamClient()
    client.get_url()
