from murph.service import Service
from concurrent import futures
from typing import List, Any, Optional, Tuple, Iterable
import os
import grpc


class Server:
    """The main server class. If you want more custom options, just inherit this class"""

    def __init__(
        self,
        host: Optional[str] = None,
        port: str = '50051',
        max_workers: int = 10,
        services: Optional[List[Service]] = None,
        export_protos: bool = False,
        protos_directory: str = "protobufs",
        thread_pool: Optional[futures.ThreadPoolExecutor] = None,
        handlers: Optional[List[grpc.GenericRpcHandler]] = None,
        interceptors: Optional[List[grpc.ServerInterceptor]] = None,
        options: Optional[Tuple[str, Any]] = None,
        maximum_concurrent_rpcs: Optional[int] = None,
        compression: Optional[grpc.Compression] = None,
        xds: bool = False
    ):
        """
        Initializes the server object.

        Args:
            host: An optional string specifying the host to bind to. If None, binds to all available network interfaces.
            port: A string specifying the port number to bind to.
            max_workers: An integer specifying the maximum number of worker threads to use.
            services: An optional list of Service objects to add to the server.
            export_protos: A boolean specifying whether or not to export the service definitions to proto files.
            protos_directory: A string specifying the directory where the proto files will be saved.
            thread_pool: An optional ThreadPoolExecutor object to use for running RPC handlers.
            handlers: An optional list of GenericRpcHandler objects to use for handling RPCs.
            interceptors: An optional list of ServerInterceptor objects to use for intercepting RPCs.
            options: An optional tuple specifying additional options to pass to the server.
            maximum_concurrent_rpcs: An optional integer specifying the maximum number of concurrent RPCs the server can handle.
            compression: An optional Compression object to use for compressing RPC payloads.
            xds: A boolean specifying whether or not to use the xDS protocol for service discovery.

        Returns:
            None
        """

        self._host = host
        self._port = port
        self._max_workers = max_workers

        if services:
            self._services = services
        else:
            self._services = []

        self._export_protos = export_protos
        self._protos_directory = protos_directory

        if thread_pool:
            self._thread_pool = thread_pool
        else:
            self._thread_pool = futures.ThreadPoolExecutor(max_workers=self._max_workers)

        self._handlers = handlers
        self._interceptors = interceptors
        self._options = options
        self._maximum_concurrent_rpcs = maximum_concurrent_rpcs
        self._compression = compression
        self._xds = xds
        self._port_registered = False
        self._endpoints = []
        self._ports = []

        # Create the gRPC server
        self._server = grpc.server(
            thread_pool=self._thread_pool,
            handlers=self._handlers,
            interceptors=self._interceptors,
            options=self._options,
            maximum_concurrent_rpcs=self._maximum_concurrent_rpcs,
            compression=self._compression,
            xds=self._xds,
        )

    def register_port(self, endpoint: str = None, credentials=None) -> int:
        """
            Registers a port with the gRPC server.

            Args:
                server: A gRPC server object.
                endpoint: A string specifying the port number and the host (e.g., '[::]:50051', '127.0.0.1:50051').
                credentials: A gRPC credentials object, or None if the port should be insecure.

            Returns:
                An integer port on which server will accept RPC requests.
        """

        if not endpoint:
            endpoint = self._endpoint

        if credentials is None:
            return self.add_insecure_port(endpoint)
        else:
            return self.add_secure_port(endpoint, credentials)

    def add_insecure_port(self, endpoint: str) -> int:
        """
        Adds an insecure port to the server.

        Args:
            endpoint: A string specifying the port number and the host (e.g., '[::]:50051', '127.0.0.1:50051').

        Returns:
            An integer port on which server will accept insecure RPC requests.
        """
        port = self._server.add_insecure_port(endpoint)

        self._endpoints.append(endpoint)

        if port not in self._ports:
            self._ports.append(port)

        self._port_registered = True

        return port

    def add_secure_port(self, endpoint: str, credentials) -> int:
        """
        Adds a secure port to the server.

        Args:
            endpoint: A string specifying the port number and the host (e.g., '[::]:50051', '127.0.0.1:50051').
            credentials: A credentials object to use for securing the port.

        Returns:
            An integer port on which server will accept secure RPC requests.
        """
        port = self._server.add_secure_port(endpoint, credentials)

        self._endpoints.append(endpoint)

        if port not in self._ports:
            self._ports.append(port)

        self._port_registered = True

        return port

    def add_generic_rpc_handlers(self, handlers: Iterable[grpc.GenericRpcHandler]) -> None:
        """
        Registers GenericRpcHandlers with this Server.

        This method is only safe to call before the server is started.

        Args:
            handlers: An iterable of GenericRpcHandlers that will be used to service RPCs

        Returns:
            None
        """

        self._server.add_generic_rpc_handlers(handlers)

    def add_service(self, service: Service) -> None:
        """
        Adds a murph service to the server.

        Args:
            service: A murph Service object to add to the server.

        Returns:
            None
        """
        # Set the default path to service class name
        handler_path = type(service).__name__

        # Add package to the path
        if service.package is not None or "":
            handler_path = f"{service.package}.{handler_path}"

        generic_handler = grpc.method_handlers_generic_handler(
            handler_path, service.get_handlers()
        )

        self.add_generic_rpc_handlers((generic_handler,))

        self._services.append(service)

        # Remove service duplicates
        self._services = list(set(self._services))

    def export_protos(self) -> None:
        """
        Exports services to proto files.

        Args:
            None

        Returns:
            None
        """

        # Check if the directory exists
        if not os.path.isdir(self._protos_directory):
            # Create the directory
            os.makedirs(self._protos_directory)

        for service in self._services:
            # Construct the file path
            file_prefix = ""
            if service.package:
                file_prefix = service.package.replace(".", "_")

            file_name = f"{file_prefix}_{type(service).__name__.lower()}.proto"
            file_path = os.path.join(self._protos_directory, file_name)

            # Write protobufs to file
            print(f"Writing {file_name} to {self._protos_directory} directory...")
            with open(file_path, "w") as file:
                file.write(service.get_proto_content(complete_export=True))
                print(f"{file_name} has been written succesfully!")

    @property
    def _endpoint(self) -> str:
        """
        Gets the endpoint string for the server.

        Args:
            None

        Returns:
            A string specifying the endpoint for the server.
        """

        if self._host:
            return f"{self._host}:{self._port}"
        else:
            return f"[::]:{self._port}"

    def start(self) -> None:
        """
        Starts the gRPC server.

        Args:
            None

        Returns:
            None
        """

        # Export protobuf files before starting the server
        if self._export_protos:
            self.export_protos()

        # If no port was registered by the user, register the default one
        if not self._port_registered:
            self.register_port()

        self._server.start()

        endpoints = ", ".join(self._endpoints)
        ports = ", ".join(map(str, self._ports))

        print(f"Server started on {endpoints}")
        print(f"Open ports: {ports}")

    def start_and_wait_for_termination(self) -> None:
        """
        Starts the gRPC server and waits for it to be shut down.

        Args:
            None

        Returns:
            None
        """

        self.start()
        self.wait_for_termination()

    def stop(self, grace: int = 30) -> None:
        """
        Stops the gRPC server and removes all ports.

        Args:
            grace: An integer specifying the number of seconds to wait for pending RPCs to complete before shutting down the server.

        Returns:
            None
        """

        if self._server:
            done_event = self._server.stop(grace)
            done_event.wait(grace)

    def stop_and_wait_for_termination(self, grace: int = 30) -> None:
        """
        Stops the gRPC server and waits for all RPCs to complete.

        Args:
            grace: An integer specifying the number of seconds to wait for pending RPCs to complete before shutting down the server.

        Returns:
            None
        """
        self._server.stop(grace)
        self._server.wait_for_termination()

    def wait_for_termination(self) -> None:
        """
        Waits for the server to be shut down.

        Args:
            None

        Returns:
            None
        """
        self._server.wait_for_termination()
