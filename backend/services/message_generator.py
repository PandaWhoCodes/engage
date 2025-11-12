"""AI-powered message generation for engagement."""

import logging
import os
import random
from datetime import datetime
import anthropic

logger = logging.getLogger(__name__)


class EngagementMessageGenerator:
    """Generates varied engagement messages using Claude."""

    def __init__(self):
        """Initialize Claude client."""
        self.api_key = os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY not found in environment variables")

        self.client = anthropic.Anthropic(api_key=self.api_key)

        # Tone/theme variations for diversity
        self.themes = [
            "meme/internet culture",
            "sports/competition",
            "music/arts",
            "gaming/tech",
            "real talk/deep thoughts",
            "goals/ambitions",
            "funny/lighthearted",
            "challenges/support",
        ]

    def generate_with_theme(self, theme: str = "random") -> dict:
        """
        Generate an engagement message with specified theme.

        Args:
            theme: Theme to use, or "random" to pick randomly

        Returns:
            dict with keys:
                - content: The mentee engagement prompt
                - theme_used: The actual theme that was used
        """
        # Pick theme
        if theme == "random" or theme not in self.themes:
            selected_theme = random.choice(self.themes)
        else:
            selected_theme = theme

        try:
            logger.info(f"Generating engagement message with theme: {selected_theme}")

            # Create diverse examples based on theme
            theme_examples = {
                "meme/internet culture": "Use memes, TikTok references, trending topics, viral content",
                "sports/competition": "Reference sports, competitions, team spirit, challenges",
                "music/arts": "Talk about music, shows, creative projects, playlists",
                "gaming/tech": "Gaming references, tech talk, online culture, streamers",
                "real talk/deep thoughts": "Deeper questions about life, future, feelings, growth",
                "goals/ambitions": "Dreams, college prep, career thoughts, aspirations",
                "funny/lighthearted": "Jokes, funny stories, light roasting, humor",
                "challenges/support": "Struggles, stress, need for support, helping each other",
            }

            prompt = (
                f"Theme: {selected_theme}\n"
                f"Guidance: {theme_examples.get(selected_theme, 'Be creative!')}\n\n"
                f"You're creating an engagement prompt for mentors to use with Gen Z teens (13-20).\n"
                f"Be EXTREMELY creative and varied. Each message should be completely unique.\n\n"
                f"Try formats like:\n"
                f"- Interactive polls or would-you-rather scenarios\n"
                f"- Creative sharing prompts (playlists, photos, stories)\n"
                f"- Mini-challenges or games\n"
                f"- Unconventional discussion starters\n"
                f"- Tier lists or rankings\n"
                f"- Fill-in-the-blank stories\n"
                f"- Hypothetical scenarios\n\n"
                f"Output as JSON with exactly this field:\n"
                f'{{"mentee_template": "[super creative prompt for teens, 250-400 chars]"}}\n\n'
                f"The mentee_template should be FUN and ENGAGING - something teens will actually want to respond to.\n"
                f"Avoid boring generic questions. Be specific, quirky, or unexpected.\n"
                f"Date context: {datetime.now().strftime('%B %d, %Y')}"
            )

            # Use Claude API with latest Sonnet 4.5 model
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                temperature=1,
                system="You're a creative genius helping mentors connect with Gen Z teens (13-20). Every message must be WILDLY different, unexpected, and fun. Never repeat formats or ideas. Be specific, quirky, and use current teen culture references.",
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.content[0].text
            logger.debug(f"AI response: {content}")

            # Parse JSON response
            import json

            # Try to extract JSON from the response
            try:
                # Sometimes Claude wraps JSON in markdown code blocks
                if "```json" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    content = content[json_start:json_end].strip()
                elif "```" in content:
                    json_start = content.find("```") + 3
                    json_end = content.find("```", json_start)
                    content = content[json_start:json_end].strip()

                parsed = json.loads(content)
            except json.JSONDecodeError as json_error:
                logger.error(f"Failed to parse JSON. Raw content: {content}")
                logger.error(f"JSON error: {json_error}")
                raise

            return {
                "content": parsed.get("mentee_template", ""),
                "theme_used": selected_theme,
            }

        except Exception as e:
            logger.error(f"Error generating engagement message: {e}")
            logger.error(f"Full error details: {type(e).__name__}: {str(e)}")
            if hasattr(e, "__dict__"):
                logger.error(f"Error attributes: {e.__dict__}")
            # Fallback message if AI fails
            return self._get_fallback_message(selected_theme)

    def _get_fallback_message(self, theme: str) -> dict:
        """Fallback message if AI generation fails."""
        fallbacks = [
            {
                "content": (
                    "POV: You can only keep 3 apps on your phone for a month. "
                    "Which ones and why? Wrong answers only accepted too 😂"
                ),
            },
            {
                "content": (
                    "Hot take thread! Drop your most controversial (but harmless) opinion. "
                    "I'll start: Pineapple on pizza is actually elite. Fight me 🍕"
                ),
            },
            {
                "content": (
                    "If your current mood was a song, what would it be? "
                    "Bonus points if you share the actual track 🎵"
                ),
            },
            {
                "content": (
                    "Would you rather: Have to sing everything you say for a day OR "
                    "only communicate through interpretive dance? Explain your survival strategy 🕺"
                ),
            },
            {
                "content": (
                    "Rate your week using only emojis (max 5). "
                    "Then guess what happened based on someone else's emoji story 👀"
                ),
            },
            {
                "content": (
                    "Quick! You're making a time capsule to open in 5 years. "
                    "What 3 things are you putting in and what message for future you?"
                ),
            },
        ]

        result = random.choice(fallbacks)
        result["theme_used"] = theme
        return result
