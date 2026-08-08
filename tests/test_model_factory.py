import unittest
from unittest.mock import patch

from fabrica_sw.model_factory import (
    ModelConfig,
    ModelConfigurationError,
    ModelFactoryError,
    create_model,
    create_models,
    load_model_config,
)


class FakeChatOpenAI:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class ModelFactoryTests(unittest.TestCase):
    def test_loads_openai_configuration(self):
        config = load_model_config(
            {
                "FACTORY_MODEL_PROVIDER": "openai",
                "FACTORY_MODEL_NAME": "gpt-test",
                "OPENAI_API_KEY": "secret",
                "FACTORY_TEMPERATURE": "0.2",
                "FACTORY_MAX_TOKENS": "512",
            }
        )
        self.assertEqual(config.provider, "openai")
        self.assertEqual(config.model, "gpt-test")
        self.assertEqual(config.temperature, 0.2)
        self.assertEqual(config.max_tokens, 512)
        self.assertIsNone(config.base_url)

    def test_loads_openrouter_configuration(self):
        config = load_model_config(
            {
                "FACTORY_MODEL_PROVIDER": "open_router",
                "FACTORY_MODEL_NAME": "deepseek/deepseek-chat",
                "OPENROUTER_API_KEY": "secret",
            }
        )
        self.assertEqual(config.provider, "openrouter")
        self.assertEqual(config.base_url, "https://openrouter.ai/api/v1")

    def test_loads_role_specific_configuration(self):
        config = load_model_config(
            {
                "FACTORY_ARCHITECT_PROVIDER": "openai",
                "FACTORY_ARCHITECT_MODEL": "gpt-5.6-luna",
                "OPENAI_API_KEY": "secret",
            },
            role="architect",
        )
        self.assertEqual(config.provider, "openai")
        self.assertEqual(config.model, "gpt-5.6-luna")

    def test_creates_one_model_per_role(self):
        env = {
            "FACTORY_ARCHITECT_PROVIDER": "openai",
            "FACTORY_ARCHITECT_MODEL": "gpt-5.6-luna",
            "FACTORY_DEVELOPER_PROVIDER": "openrouter",
            "FACTORY_DEVELOPER_MODEL": "deepseek/deepseek-v4-flash-0731",
            "FACTORY_AUDITOR_PROVIDER": "openai",
            "FACTORY_AUDITOR_MODEL": "gpt-5.6-luna",
            "OPENAI_API_KEY": "openai-secret",
            "OPENROUTER_API_KEY": "router-secret",
        }
        with patch("fabrica_sw.model_factory._load_chat_openai", return_value=FakeChatOpenAI):
            models = create_models(env=env)
        self.assertEqual(set(models), {"architect", "developer", "auditor"})
        self.assertEqual(models["developer"].kwargs["model"], "deepseek/deepseek-v4-flash-0731")
        self.assertEqual(models["developer"].kwargs["base_url"], "https://openrouter.ai/api/v1")

    def test_rejects_unknown_provider(self):
        with self.assertRaises(ModelConfigurationError):
            load_model_config({"FACTORY_MODEL_PROVIDER": "unknown", "OPENAI_API_KEY": "x"})

    def test_rejects_missing_provider_key(self):
        with self.assertRaises(ModelConfigurationError) as error:
            load_model_config({"FACTORY_MODEL_PROVIDER": "openai"})
        self.assertIn("OPENAI_API_KEY", str(error.exception))

    def test_rejects_unknown_role(self):
        with self.assertRaises(ModelConfigurationError):
            load_model_config({"OPENAI_API_KEY": "secret"}, role="operator")

    def test_creates_model_lazily(self):
        config = ModelConfig(
            provider="openai", model="gpt-test", api_key="secret", max_tokens=100
        )
        with patch("fabrica_sw.model_factory._load_chat_openai", return_value=FakeChatOpenAI):
            model = create_model(config)
        self.assertEqual(model.kwargs["model"], "gpt-test")
        self.assertEqual(model.kwargs["api_key"], "secret")
        self.assertEqual(model.kwargs["max_tokens"], 100)

    def test_reports_missing_runtime_dependency(self):
        with patch(
            "fabrica_sw.model_factory._load_chat_openai",
            side_effect=ModelFactoryError("Falta langchain-openai"),
        ):
            with self.assertRaises(ModelFactoryError):
                create_model(ModelConfig("openai", "gpt-test", "secret"))


if __name__ == "__main__":
    unittest.main()
