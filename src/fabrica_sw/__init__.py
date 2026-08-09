"""Componentes compartidos de la fábrica de software."""

from .state import (
    ArchitectureBlueprint,
    FactoryState,
    create_initial_state,
    validate_factory_state,
)
from .persistence import (
    FACTORY_STATE_DB,
    build_persistence_config,
    build_thread_config,
    open_checkpoint_saver,
    resolve_database_path,
)
from .workflow_policy import (
    MAX_ITERATIONS,
    ROUTE_DEVELOPER,
    ROUTE_DEPLOY,
    ROUTE_STOP,
    evaluate_workflow_router,
    evaluate_workflow_route,
)
from .git_policy import ensure_commit_approved
from .git_tools import git_secure_commit_tool
from .github_safe_pusher import github_secure_push_tool
from .auth_security import hash_password_secure, validate_password_complexity
from .safe_paths import WORKSPACE_DIR, validate_safe_path
from .architect import ARCHITECT_SYSTEM_PROMPT, architect_node
from .auditor import AUDITOR_SYSTEM_PROMPT, auditor_node
from .developer import (
    DEVELOPER_SYSTEM_PROMPT,
    LocalToolNode,
    ROUTE_EXECUTE_TOOLS,
    ROUTE_POST_PROCESS,
    build_tool_executor_node,
    developer_node,
    should_continue_router,
    tool_executor_node,
)
from .safe_factory_tools import (
    SAFE_DEVELOPMENT_TOOLS,
    execute_test_command,
    graphify_query_tool,
    graphify_shortest_path_tool,
    list_directory_tool,
    read_file_tool,
    write_file_tool,
)
from .workflow import LocalAutonomousFactory, build_autonomous_factory, deploy_and_sync_node
from .runner import FactoryRunRequest, FactoryRunResult, run_factory

__all__ = [
    "SAFE_DEVELOPMENT_TOOLS",
    "ARCHITECT_SYSTEM_PROMPT",
    "architect_node",
    "AUDITOR_SYSTEM_PROMPT",
    "auditor_node",
    "DEVELOPER_SYSTEM_PROMPT",
    "LocalToolNode",
    "ROUTE_EXECUTE_TOOLS",
    "ROUTE_POST_PROCESS",
    "build_tool_executor_node",
    "developer_node",
    "should_continue_router",
    "tool_executor_node",
    "ArchitectureBlueprint",
    "FactoryState",
    "create_initial_state",
    "validate_factory_state",
    "FACTORY_STATE_DB",
    "build_persistence_config",
    "build_thread_config",
    "open_checkpoint_saver",
    "resolve_database_path",
    "MAX_ITERATIONS",
    "ROUTE_DEVELOPER",
    "ROUTE_DEPLOY",
    "ROUTE_STOP",
    "evaluate_workflow_route",
    "evaluate_workflow_router",
    "ensure_commit_approved",
    "git_secure_commit_tool",
    "github_secure_push_tool",
    "hash_password_secure",
    "validate_password_complexity",
    "WORKSPACE_DIR",
    "validate_safe_path",
    "read_file_tool",
    "write_file_tool",
    "list_directory_tool",
    "execute_test_command",
    "graphify_query_tool",
    "graphify_shortest_path_tool",
    "LocalAutonomousFactory",
    "build_autonomous_factory",
    "deploy_and_sync_node",
    "FactoryRunRequest",
    "FactoryRunResult",
    "run_factory",
]
from .model_factory import (
    ModelConfig,
    ModelConfigurationError,
    ModelFactoryError,
    create_model,
    create_models,
    load_model_config,
)

__all__ = [
    "ModelConfig",
    "ModelConfigurationError",
    "ModelFactoryError",
    "create_model",
    "create_models",
    "load_model_config",
]
