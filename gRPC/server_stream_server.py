from concurrent import futures

import grpc

import gRPC.proto.grpc_pb2 as pb2
import gRPC.proto.grpc_pb2_grpc as pb2_grpc


class ServerStreamService(pb2_grpc.GRPCServiceServicer):

    def response_stream(self, request, context):
        messages = [
            pb2.Message(message="First response for message %s" % request.message),
            pb2.Message(message="First response for message %s" % request.message),
            pb2.Message(message="First response for message %s" % request.message),
            pb2.Message(message="First response for message %s" % request.message),
            pb2.Message(message="First response for message %s" % request.message),
        ]
        for msg in messages:
            yield msg


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_GRPCServiceServicer_to_server(ServerStreamService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
