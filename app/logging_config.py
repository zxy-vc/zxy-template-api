"""
Structured logging configuration using structlog.

- Production  → JSON output (machine-readable, suitable for Datadog/Logtail)
- Development → Human-readable colored console output
"""
import logging
import sys

import structlog


def configure_logging(environment: str = "development") -> None:
    """Call once at app startup (before first log line)."""

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if environment == "production":
        # JSON — ship to your log aggregator
        renderer = structlog.processors.JSONRenderer()
    else:
        # Colorful dev console
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(logging.INFO if environment == "production" else logging.DEBUG)


def get_logger(name: str = __name__) -> structlog.BoundLogger:
    """Return a bound structlog logger."""
    return structlog.get_logger(name)
