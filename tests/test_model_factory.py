import unittest
from unittest.mock import patch

from fabrica_sw.model_factory import (
    ModelConfig,
    ModelConfigurationError,
    ModelFactoryError,
    create_model,
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

    def test_rejects_unknown_provider(self):
        with self.assertRaises(ModelConfigurationError):
            load_model_config({"FACTORY_MODEL_PROVIDER": "unknown", "OPENAI_API_KEY": "x"})

    def test_rejects_missing_provider_key(self):
        with self.assertRaises(ModelConfigurationError) as error:
            load_model_config({"FACTORY_MODEL_PROVIDER": "openai"})
        self.assertIn("OPENAI_API_KEY", str(error.exception))

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
