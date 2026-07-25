# merle-core — Public Interfaces

Dies ist die vollständige öffentliche API-Oberfläche von `merle_core`. Alles hier Genannte ist via `from merle_core import ...` erreichbar.

## @tag:basebot — Bot-Lifecycle

```python
from merle_core import BaseBot


class BaseBot:
    def __init__(self, settings: Any, name: str) -> None: ...
    async def run(self) -> dict[str, Any]: ...
    async def execute(self) -> dict[str, Any]: ...  # Abstrakt — muss implementiert werden
    async def health_check(self) -> dict[str, Any]: ...
    def get_metrics(self) -> dict[str, Any]: ...
    def _on_success(self, result: dict) -> None: ...  # Hook (überschreibbar)
    def _on_failure(self, exception: Exception) -> None: ...  # Hook (überschreibbar)

    status: str  # "pending" | "running" | "success" | "failed"
    duration: float | None  # Sekunden
```

## @tag:basetask — Task-Lifecycle

```python
from merle_core import BaseTask


class BaseTask:
    def __init__(self, settings: Any, name: str) -> None: ...
    async def run(self) -> dict[str, Any]: ...
    async def execute(self) -> dict[str, Any]: ...  # Abstrakt — muss implementiert werden
    async def health_check(self) -> dict[str, Any]: ...
    def _on_success(self, result: dict) -> None: ...
    def _on_failure(self, exception: Exception) -> None: ...

    status: str
    duration: float | None
```

## @tag:task-spec — Task-Datenmodelle

```python
from merle_core import TaskSpec, TaskResult, TaskStatus, TaskError


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRY = "retry"


@dataclass
class TaskSpec:
    task_id: str
    type: str
    payload: dict[str, Any]
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict: ...
    @classmethod
    def from_dict(cls, data: dict) -> TaskSpec: ...


@dataclass
class TaskError:
    code: str
    message: str
    details: dict[str, Any] | None = None


@dataclass
class TaskResult:
    task_id: str
    status: TaskStatus
    data: dict[str, Any] | None = None
    error: TaskError | None = None
    completed_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def success(cls, task_id: str, data: dict) -> TaskResult: ...
    @classmethod
    def failure(cls, task_id: str, error: TaskError) -> TaskResult: ...
    def to_dict(self) -> dict: ...
    @classmethod
    def from_dict(cls, data: dict) -> TaskResult: ...
```

## Exceptions

```python
from merle_core import (
    MerleError,  # Basis
    RetryExhaustedError,  # Retry
    CircuitBreakerOpenError,  # Retry
    PlaywrightError,  # Browser
    BrowserLaunchError,  # Browser
    ElementNotFoundError,  # Browser
    ScreenshotFailedError,  # Browser
    DataProcessingError,  # Data
    ExcelError,  # Data
    PdfError,  # Data
    UiPathError,  # UiPath
    QueueItemError,  # UiPath
    SecretsError,  # Secrets
    SecretNotFoundError,  # Secrets
    BusinessRuleViolation,  # Business-Logik
)
```

## @tag:retry — Policies + Decorator

```python
from merle_core import with_retry, retry_with_policy
from merle_core import (
    default_http_retry,  # 3 Versuche, 1s→4s, mit Jitter
    browser_retry,  # 3 Versuche, 2s→8s, mit Jitter
    sensitive_operation_retry,  # 5 Versuche, 2s→16s, mit Jitter
    aggressive_retry,  # 5 Versuche, 0.5s→4s, mit Jitter
)


# Decorator (für async-Methoden):
@with_retry(policy=default_http_retry)
async def fetch_data(self) -> dict: ...


# Manuelle Retry-Utility:
result = await retry_with_policy(sensitive_operation_retry, some_coro, arg1, arg2)
```

## HTTP-Client

```python
from merle_core import RpaHttpClient


class RpaHttpClient:
    def __init__(self, base_url: str, bearer_token: str | None = None) -> None: ...
    async def __aenter__(self) -> RpaHttpClient: ...
    async def __aexit__(self, *args) -> None: ...
    async def get(self, path: str, **kwargs) -> httpx.Response: ...
    async def post(self, path: str, **kwargs) -> httpx.Response: ...
    async def put(self, path: str, **kwargs) -> httpx.Response: ...
    async def delete(self, path: str, **kwargs) -> httpx.Response: ...
```

## @tag:loguru — Logging

```python
from merle_core import setup_logging


def setup_logging(
    level: str = "INFO",
    json_log_file: str | None = None,
    rotation: str = "10 MB",
    retention: str = "30 days",
) -> None: ...
```

## @tag:observability — OTEL

```python
from merle_core import configure_observability, get_tracer, get_meter
from merle_core.observability import configure_loguru_otel_sink


def configure_observability(
    service_name: str,
    otlp_endpoint: str = "localhost:4317",
    enable_tracing: bool = True,
    enable_metrics: bool = True,
) -> None: ...


def get_tracer() -> Tracer: ...
def get_meter() -> Meter: ...
def configure_loguru_otel_sink() -> None: ...
```

## @tag:playwright — Browser

```python
from merle_core import (
    launch_robust_browser,
    RobustBrowser,
    robust_goto,
    safe_click,
    safe_fill,
)

BrowserEngine = Literal["chromium", "lightpanda"]


@asynccontextmanager
async def launch_robust_browser(
    engine: BrowserEngine = "chromium",
    headless: bool = True,
    screenshot_on_failure: bool = True,
    lightpanda_host: str = "localhost",
    lightpanda_port: int = 9222,
    **kwargs,
) -> AsyncIterator[RobustBrowser]: ...


class RobustBrowser:
    browser: Browser | LightpandaBrowser
    context: BrowserContext

    async def new_page(self) -> Page: ...


async def robust_goto(page: Page, url: str, timeout: int = 30000) -> None: ...
async def safe_click(page: Page, selector: str, timeout: int = 10000) -> None: ...
async def safe_fill(page: Page, selector: str, text: str, timeout: int = 10000) -> None: ...
```

## @tag:secrets — Secret-Provider

```python
from merle_core import SecretProvider, AzureKeyVaultProvider, AzureKeyVaultSettings


class SecretProvider(ABC):
    async def get_secret(self, name: str) -> str: ...
    async def get_secret_or_default(self, name: str, default: str | None = None) -> str | None: ...


class AzureKeyVaultProvider(SecretProvider):
    def __init__(self, vault_url: str) -> None: ...
    async def get_secret(self, name: str) -> str: ...
    async def close(self) -> None: ...


class AzureKeyVaultSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @classmethod
    async def from_keyvault(cls, vault_url: str) -> Self: ...
```

## @tag:nats — Messaging

```python
from merle_core import NatsClient, NatsMessage, PullConsumer


@dataclass
class NatsMessage:
    subject: str
    data: bytes
    reply: str | None = None


class NatsClient:
    def __init__(self, servers: list[str] = ["nats://localhost:4222"]) -> None: ...
    async def __aenter__(self) -> NatsClient: ...
    async def __aexit__(self, *args) -> None: ...
    async def publish(self, subject: str, data: bytes, reply: str | None = None) -> None: ...
    async def subscribe(self, subject: str, callback: Callable) -> None: ...
    async def request(self, subject: str, data: bytes, timeout: float = 30.0) -> NatsMessage: ...
    async def publish_task(self, subject: str, task: TaskSpec) -> None: ...
    async def request_task(self, subject: str, task: TaskSpec) -> TaskResult: ...
    async def publish_to_stream(self, subject: str, stream_name: str, data: bytes) -> None: ...


class PullConsumer:
    def __init__(self, client: NatsClient, stream: str, consumer: str) -> None: ...
    async def fetch(self, timeout: float = 5.0) -> NatsMessage | None: ...
    async def ack(self, msg: NatsMessage) -> None: ...
    async def nak(self, msg: NatsMessage) -> None: ...
    async def term(self, msg: NatsMessage) -> None: ...
    async def messages(self) -> AsyncIterator[NatsMessage]: ...


async def consume_tasks(client: NatsClient, stream: str, consumer: str) -> AsyncIterator[TaskSpec]: ...
```

## Data — Excel / PDF / Email

```python
from merle_core import ExcelReader, ExcelWriter, PdfExtractor, EmailClient


class ExcelReader:
    def __init__(self, filepath: str) -> None: ...
    def read_sheet(self, sheet_name: str = "Sheet1") -> DataFrame: ...


class ExcelWriter:
    def __init__(self, filepath: str) -> None: ...
    def write_sheet(self, df: DataFrame, sheet_name: str = "Sheet1") -> None: ...


class PdfExtractor:
    @staticmethod
    def extract_text(filepath: str) -> str: ...
    @staticmethod
    def extract_tables(filepath: str) -> list[list[list[str]]]: ...


class EmailClient:
    @staticmethod
    async def download_attachments(
        imap_server: str, username: str, password: str, download_dir: str, folder: str = "INBOX"
    ) -> list[str]: ...
    @staticmethod
    async def send_email(
        smtp_server: str,
        sender: str,
        recipients: list[str],
        subject: str,
        body: str,
        html: bool = False,
        attachments: list[str] | None = None,
    ) -> None: ...
```

## @tag:uipath-hybrid — UiPath Integration

```python
from merle_core import UiPathOrchestratorClient, UiPathQueueHelper


class UiPathOrchestratorClient:
    def __init__(self, base_url: str, tenant: str, client_id: str, client_secret: str) -> None: ...
    async def authenticate(self) -> None: ...
    async def start_job(self, release_key: str, parameters: dict | None = None) -> dict: ...
    async def get_job_status(self, job_id: int) -> dict: ...


class UiPathQueueHelper:
    def __init__(self, client: UiPathOrchestratorClient) -> None: ...
    async def add_queue_item(self, queue_name: str, data: dict) -> dict: ...
    async def get_queue_items(self, queue_name: str, filter_str: str | None = None) -> list[dict]: ...
```
