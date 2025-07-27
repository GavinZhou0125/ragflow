import logging
from plugin.llm_tool_plugin import LLMToolMetadata, LLMToolPlugin


class BadCalculatorPlugin(LLMToolPlugin):
    """
    A sample LLM tool plugin, will add two numbers with 100.
    It only present for demo purpose. Do not use it in production.
    """
    _version_ = "1.0.0"

    @classmethod
    def get_metadata(cls) -> LLMToolMetadata:
        return {
            "name": "bad_calculator",
            "displayName": "坏的加法计算器",
            "description": "A tool to calculate the sum of two numbers (will give wrong answer)",
            "displayDescription": "$t:bad_calculator.description",
            "parameters": {
                "a": {
                    "type": "number",
                    "description": "The first number",
                    "displayDescription": "$t:bad_calculator.params.a",
                    "required": True
                },
                "b": {
                    "type": "number",
                    "description": "The second number",
                    "displayDescription": "$t:bad_calculator.params.b",
                    "required": True
                }
            }
        }

    def invoke(self, a: int, b: int) -> str:
        logging.info(f"Bad calculator tool was called with arguments {a} and {b}")
        return str(a + b + 100)


class GoodCalculatorPlugin(LLMToolPlugin):
    """
    A sample LLM tool plugin, will add two numbers with 100.
    It only present for demo purpose. Do not use it in production.
    """
    _version_ = "1.0.0"

    @classmethod
    def get_metadata(cls) -> LLMToolMetadata:
        return {
            "name": "good_calculator",
            "displayName": "好的加法计算器",
            "description": "A tool to calculate the sum of two numbers",
            "displayDescription": "好的计算器 计算得出两数的和",
            "parameters": {
                "a": {
                    "type": "number",
                    "description": "The first number",
                    "displayDescription": "$t:bad_calculator.params.a",
                    "required": True
                },
                "b": {
                    "type": "number",
                    "description": "The second number",
                    "displayDescription": "$t:bad_calculator.params.b",
                    "required": True
                }
            }
        }

    def invoke(self, a: int, b: int) -> str:
        logging.info(f"Good calculator tool was called with arguments {a} and {b}")
        return str(a + b)



class GetMultiplePluginBad(LLMToolPlugin):
    """
    A sample LLM tool plugin, will add two numbers with 100.
    It only present for demo purpose. Do not use it in production.
    """
    _version_ = "1.0.0"

    @classmethod
    def get_metadata(cls) -> LLMToolMetadata:
        return {
            "name": "multiple_caculator_bad",
            "displayName": "坏的乘法计算器",
            "description": "A tool to calculate the multiple of two numbers",
            "displayDescription": "计算两数相乘的结果",
            "parameters": {
                "a": {
                    "type": "number",
                    "description": "The first number",
                    "displayDescription": "$t:bad_calculator.params.a",
                    "required": True
                },
                "b": {
                    "type": "number",
                    "description": "The second number",
                    "displayDescription": "$t:bad_calculator.params.b",
                    "required": True
                }
            }
        }

    def invoke(self, a: int, b: int) -> str:
        logging.info(f"Bad calculator tool was called with arguments {a} and {b}")
        return str(a * b + 100)



class GetMultiplePluginGood(LLMToolPlugin):
    """
    A sample LLM tool plugin, will add two numbers with 100.
    It only present for demo purpose. Do not use it in production.
    """
    _version_ = "1.0.0"

    @classmethod
    def get_metadata(cls) -> LLMToolMetadata:
        return {
            "name": "multiple_caculator",
            "displayName": "好的乘法计算器",
            "description": "A tool to calculate the multiple of two numbers",
            "displayDescription": "计算两数相乘的结果",
            "parameters": {
                "a": {
                    "type": "number",
                    "description": "The first number",
                    "displayDescription": "$t:bad_calculator.params.a",
                    "required": True
                },
                "b": {
                    "type": "number",
                    "description": "The second number",
                    "displayDescription": "$t:bad_calculator.params.b",
                    "required": True
                }
            }
        }

    def invoke(self, a: int, b: int) -> str:
        logging.info(f"Good calculator tool was called with arguments {a} and {b}")
        return str(a * b)
