import os

from openinference.instrumentation.langchain import LangChainInstrumentor
from opentelemetry import trace as trace_api
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from .settings import settings


def setup_otel():

    headers = {
        "Galileo-API-Key": settings.GALILEO_API_KEY,
        "project": settings.GALILEO_PROJECT,
        "logstream": settings.GALILEO_LOG_STREAM,
    }

    os.environ["OTEL_EXPORTER_OTLP_TRACES_HEADERS"] = ",".join(
        [f"{k}={v}" for k, v in headers.items()]
    )

    # OTEL endpoint for Galileo
    endpoint = "https://app.galileo.ai/api/galileo/otel/traces"

    # Setup tracer provider
    tracer_provider = trace_sdk.TracerProvider()
    tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint)))

    # Optional: log locally
    tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    # Register the provider
    trace_api.set_tracer_provider(tracer_provider=tracer_provider)

    # LangChain instrumentation
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

    print("LangChain OTEL tracing initialized.")
