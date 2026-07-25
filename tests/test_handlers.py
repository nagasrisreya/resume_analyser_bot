import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from bot import handlers


class ReceiveQuestionTests(unittest.TestCase):
    def setUp(self):
        handlers.ask_mode_users.clear()
        handlers.analysis_results.clear()

    def test_receive_question_answers_using_saved_analysis(self):
        update = SimpleNamespace(
            effective_user=SimpleNamespace(id=42),
            message=SimpleNamespace(text="Who has the highest CGPA?"),
        )
        context = SimpleNamespace()
        handlers.ask_mode_users.add(42)
        handlers.analysis_results[42] = {"jd": {}, "resumes": []}

        update.message.reply_text = AsyncMock()

        with patch("bot.handlers.ask_resume_question", return_value="Answer") as mock_answer:
            import asyncio
            asyncio.run(handlers.receive_question(update, context))

        mock_answer.assert_called_once_with("Who has the highest CGPA?", handlers.analysis_results[42])
        update.message.reply_text.assert_awaited_once_with("Answer")


if __name__ == "__main__":
    unittest.main()
