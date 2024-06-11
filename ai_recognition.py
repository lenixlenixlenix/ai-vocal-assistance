import asyncio
import time

from openai import AsyncOpenAI
from pathlib import Path

from config import Settings

settings = Settings() 


class VocalAssistance():
    def __init__(self, token):
        self.client = AsyncOpenAI(api_key=token)
                
    async def generate_assistance(self) -> str:
        assistant = await self.client.beta.assistants.create(
            name="Chat bot",
            instructions="You are a personal bot that. Answer the questions like i am silly kid.",
            model="gpt-3.5-turbo"
        )
        settings.assistant_id = assistant.id

    async def answer_question(self, question: str) -> str:
        answer: str = ""

        thread = await self.client.beta.threads.create()
        

        message = await self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )
        # changed run from create to create_and_poll
        run = await self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=settings.assistant_id,
            instructions=f"Please answer the question {question}"
        )

        while True:
            run_status = await self.client.beta.threads.runs.retrieve(thread_id=thread.id, 
                                                        run_id=run.id)
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                print("Run failed:", run_status.last_error)
                answer = "I cannot process your question"
                break
            await asyncio.sleep(0.5) 

        messages = await self.client.beta.threads.messages.list(
            thread_id=thread.id
        )
        answer = messages.data[0].content[0].text.value

        return answer


    async def speech_to_text(self, file_path: str) -> str:
        audio_file = open((file_path), "rb")
        translation = await self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return translation.text

    async def text_to_speech(self, text: str) -> None:
        file = "speech.ogg"
        response = await self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        response.stream_to_file(Path("files", file))


    




    # va = VocalAssistance(settings.open_ai_token)
    # source_text = await va.speech_to_text("test.mp3")
    # answer_text = await va.answer_question(source_text)
    # await va.text_to_speech(answer_text)







