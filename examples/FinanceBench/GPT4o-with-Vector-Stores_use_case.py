from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio
import signal
import logging
import aiohttp
import io
import urllib.parse

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenAIAssistant:
    """
    A class to represent an assistant using OpenAI's API.
    
    This class provides functionalities to interact with OpenAI's API for managing
    vector stores, creating assistants, and processing user inputs.
    """
    def __init__(self):
        """
        Initialize the OpenAIAssistant with necessary configurations and clients.
        """
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        self.conversation_threads = {}
        self.assistant_id = None
        self.vector_store_id = None

    async def start(self):
        """
        Start the assistant by setting up signal handlers and initializing vector store.
        """
        self.setup_signal_handler()
        await self.initialize_vector_store()

    def setup_signal_handler(self):
        """
        Set up signal handler for graceful shutdown.
        """
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        """
        Handle the SIGINT signal for graceful shutdown.
        
        Args:
            sig: Signal number.
            frame: Current stack frame.
        """
        logger.info("Deleting assistant and threads before exiting...")
        self.cleanup()
        exit(0)

    async def initialize_vector_store(self):
        """
        Initialize vector store by listing available vector stores and creating an assistant.
        """
        vector_stores = self.list_vector_stores()
        logger.info(f"Available Vector Stores: {vector_stores}")
        if vector_stores:
            self.vector_store_id = vector_stores[0].id
            self.create_assistant(self.vector_store_id)
        else:
            logger.error("No Vector Stores available. Exiting.")

    def list_vector_stores(self):
        """
        List available vector stores using OpenAI API.
        
        Returns:
            List of vector stores.
        """
        vector_stores = self.openai_client.beta.vector_stores.list()
        return vector_stores.data

    @staticmethod
    def read_instructions_from_file(file_path):
        """
        Read instructions from a specified file.
        
        Args:
            file_path: Path to the instructions file.
        
        Returns:
            Content of the instructions file.
        """

        with open(file_path, 'r') as file:
            return file.read()

    def create_assistant(self, vector_store_id):
        """
        Create an OpenAI assistant with specified vector store ID.
        
        Args:
            vector_store_id: ID of the vector store.
        """

        instructions = self.read_instructions_from_file('instructions.yaml')
        assistant = self.openai_client.beta.assistants.create(
            name="Assistant",
            model="gpt-4o",
            instructions=instructions,
            tools=[{"type": "code_interpreter"}, {"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
        )
        self.assistant_id = assistant.id
        logger.info(f"Created assistant with ID: {self.assistant_id} using Vector Store ID: {vector_store_id}")

    def cleanup(self):
        """
        Perform cleanup by deleting threads and the assistant.
        """
        self.delete_threads()
        self.delete_assistant()

    def delete_threads(self):
        """
        Delete all conversation threads.
        """
        for thread_id in self.conversation_threads.values():
            self.openai_client.beta.threads.delete(thread_id=thread_id)
            logger.info(f"Deleted thread with ID: {thread_id}")

    def delete_assistant(self):
        """
        Delete the assistant.
        """
        if self.assistant_id:
            self.openai_client.beta.assistants.delete(assistant_id=self.assistant_id)
            logger.info(f"Deleted assistant with ID: {self.assistant_id}")

    async def add_file_to_vectorstore(self, file_path_or_url):
        """
        Add a file to the vector store, determining whether it's a URL or a local file path.
        
        Args:
            file_path_or_url: Path or URL of the file.
        
        Returns:
            ID of the file batch.
        """
        try:
            if self.is_url(file_path_or_url):
                return await self.add_url_file_to_vectorstore(file_path_or_url)
            else:
                return await self.add_disk_file_to_vectorstore(file_path_or_url)
        except Exception as e:
            logger.error(f"Failed to add file to vector store: {e}")
            raise

    @staticmethod
    def is_url(path):
        """
        Check if the given path is a URL.
        
        Args:
            path: Path to check.
        
        Returns:
            True if the path is a URL, False otherwise.
        """
        return urllib.parse.urlparse(path).scheme in ('http', 'https')

    async def add_url_file_to_vectorstore(self, file_url):
        """
        Add a file from a URL to the vector store.
        
        Args:
            file_url: URL of the file.
        
        Returns:
            ID of the file batch.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                if response.status == 200:
                    file_content = await response.read()
                    file_name = self.extract_filename_from_url(file_url)
                    file_stream = self.create_file_stream(file_name, file_content)
                    return await self.upload_file_to_vectorstore(file_stream)
                else:
                    raise Exception(f"Failed to download file from URL: {file_url}")

    @staticmethod
    def extract_filename_from_url(file_url):
        """
        Extract the filename from a given URL.
        
        Args:
            file_url: URL of the file.
        
        Returns:
            Extracted filename.
        """
        parsed_url = urllib.parse.urlparse(file_url)
        return os.path.basename(parsed_url.path).split('?')[0]

    @staticmethod
    def create_file_stream(file_name, file_content):
        """
        Create a file stream from the given file content.
        
        Args:
            file_name: Name of the file.
            file_content: Content of the file.
        
        Returns:
            File stream.
        """
        file_stream = io.BytesIO(file_content)
        file_stream.name = file_name
        return file_stream

    async def add_disk_file_to_vectorstore(self, file_path):
        """
        Add a local file to the vector store.
        
        Args:
            file_path: Path to the local file.
        
        Returns:
            ID of the file batch.
        """
        if not os.path.isfile(file_path):
            raise Exception(f"File does not exist: {file_path}")
        
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as file:
            file_content = file.read()
        
        file_stream = self.create_file_stream(file_name, file_content)
        return await self.upload_file_to_vectorstore(file_stream)

    async def upload_file_to_vectorstore(self, file_stream):
        """
        Upload a file stream to the vector store.
        
        Args:
            file_stream: File stream to upload.
        
        Returns:
            ID of the file batch.
        """
        file_batch = self.openai_client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=self.vector_store_id,
            files=[file_stream]
        )
        return file_batch.id

    async def handle_user_input(self, content, file_paths_or_urls=None):
        """
        Handle user input by creating a conversation thread and processing files.
        
        Args:
            content: User input content.
            file_paths_or_urls: List of file paths or URLs.
        
        Returns:
            Response text from the assistant.
        """
        thread_id = self.get_or_create_thread("channel_id")
        content_blocks, file_batch_ids = await self.process_files(file_paths_or_urls)
        
        if not content and file_batch_ids:
            content = "Describe the uploaded files."
        
        if content:
            content_blocks.append({"type": "text", "text": content})
        else:
            return "Please provide a message or file."
        
        try:
            response_text = await self.process_user_message(thread_id, content_blocks)
            return response_text
        except Exception as e:
            logger.error(f"Error in handle_user_input: {e}")
            return "An error occurred while processing the message."

    def get_or_create_thread(self, channel_id):
        """
        Get or create a conversation thread for a given channel.
        
        Args:
            channel_id: ID of the channel.
        
        Returns:
            ID of the conversation thread.
        """
        if channel_id not in self.conversation_threads:
            thread = self.openai_client.beta.threads.create()
            self.conversation_threads[channel_id] = thread.id
            logger.info(f"Created new thread with ID: {thread.id}")
        return self.conversation_threads[channel_id]

    async def process_files(self, file_paths_or_urls):
        """
        Process a list of file paths or URLs and add them to the vector store.
        
        Args:
            file_paths_or_urls: List of file paths or URLs.
        
        Returns:
            A tuple containing content blocks and file batch IDs.
        """
        content_blocks = []
        file_batch_ids = []
        
        if file_paths_or_urls:
            logger.info("Processing files...")
            for file_path_or_url in file_paths_or_urls:
                try:
                    file_batch_id = await self.add_file_to_vectorstore(file_path_or_url)
                    file_batch_ids.append(file_batch_id)
                except Exception as e:
                    logger.error(f"Failed to add file to vector store: {e}")
                    return content_blocks, file_batch_ids

            if file_batch_ids:
                logger.info(f"{len(file_batch_ids)} file batches added to vector store.")
        
        return content_blocks, file_batch_ids

    async def process_user_message(self, thread_id, content_blocks):
        """
        Process user message by sending it to the assistant and retrieving the response.

        This method sends the user's message to the assistant, waits for the assistant's response,
        and then retrieves and processes the assistant's response to return it in a readable format.

        Args:
            thread_id (str): The ID of the conversation thread.
            content_blocks (list): A list of content blocks containing the user's message and any additional data.

        Returns:
            str: The response text from the assistant, or a message indicating that no response was found.
        """
        self.openai_client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content_blocks
        )
        logger.info(f"Added user message to thread {thread_id}")

        run = self.openai_client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        )
        logger.info(f"Created run with ID: {run.id} for thread: {thread_id}")
        logger.info(f"Prompt Tokens: {run.usage.prompt_tokens}")
        logger.info(f"Completion Tokens: {run.usage.completion_tokens}")
        logger.info(f"Total Tokens: {run.usage.total_tokens}")

        messages = self.openai_client.beta.threads.messages.list(thread_id=thread_id)
        assistant_responses = [msg for msg in messages.data if msg.role == 'assistant']

        if assistant_responses:
            first_response = assistant_responses[0]
            response_text = ''.join(
                content_block.text.value + '\n'
                for content_block in first_response.content
                if content_block.type == 'text'
            )
            return response_text.strip()
        else:
            return "No response from the assistant found."

if __name__ == "__main__":
    assistant = OpenAIAssistant()
    asyncio.run(assistant.start())

    filepath_or_url = "/Users/shrutiraghavan/shruti/aitomatic/source_code/openssa/examples/FinanceBench/.data/docs/3M_2023Q2_10Q/3M_2023Q2_10Q.pdf"
    question = "Does 3M have a reasonably healthy liquidity profile based on its quick ratio for Q2 of FY2023? If the quick ratio is not relevant to measure liquidity, please state that and explain why."

    # question = "What did the author work on growing up?"
    # filepath_or_url = "https://paulgraham.com/worked.html"

    response = asyncio.run(assistant.handle_user_input(question, [filepath_or_url]))
    
    print(response)
