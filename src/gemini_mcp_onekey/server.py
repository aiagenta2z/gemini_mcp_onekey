import logging

from typing import Deque, List, Optional, Tuple, Any, Dict, Annotated
from pydantic import BaseModel
import httpx
import mcp
from mcp.server.fastmcp import Context, FastMCP
import uuid

from pydantic.v1.schema import schema

logging.basicConfig(
    filename='server.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

class CustomFastMCP(FastMCP):
    """
    Custom FastMCP implementation Debug Purpose Only, IF used the customFastMCP,
    the default tool description will not be displaying
    """
    async def _handle_list_tools(self, context):
        # print(f"ListTools Request Details: {context.request}")
        context.info(f"ListTools _handle_list_tools Request Details: {context.request}")
        context.info(f"ListTools _handle_list_tools Request Details: {str(context.request)}")
        return await super()._handle_list_tools(context)

# Initialize FastMCP server
server = FastMCP(
    name="gemini_mcp_onekey"
)


#### Gemini MCP OneKey Server

import os
from google import genai
from google.genai import types
from google.genai.types import Modality
from dotenv import load_dotenv
from typing import Optional
import logging
import time
import uuid

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_GEMINI_3_PRO_IMAGE_PREVIEW = "gemini-3-pro-image-preview"
MODEL_GEMINI_2_5_FLASH_IMAGE = "gemini-2.5-flash-image"


script_path = os.path.abspath(__file__)
ROOT_DIR = os.path.dirname(script_path)
DEFAULT_IMAGE_DIR = os.path.join(ROOT_DIR, "img")


if GOOGLE_API_KEY is None:
    print (f"DEBUG: Input GOOGLE_API_KEY is None...")

http_options = types.HttpOptions(timeout=120000)
client = genai.Client(api_key=GOOGLE_API_KEY, http_options=http_options)


def get_temp_file_name():
    """
    """
    image_name = str(uuid.uuid4()) + ".png"
    return image_name

def run_gemini_image_api(
        model: str = "gemini-2.5-flash-image",
        prompt: str = "A detailed, cinematic image of a futuristic city.",
        image_name: str = "gemini_output_images",
        output_folder: Optional[str] = None,
        aspect_ratio: str = "16:9",
        image_size: str = "1K",
    ) -> str:
    """
        pip install mcp google-genai
        pip install --upgrade google-genai
        

        Gemini 3: https://ai.google.dev/gemini-api/docs/gemini-3?hl=zh-cn&thinking=high

        Gemini 2.5: https://ai.google.dev/api/generate-content?hl=zh-cn#image
    
        prompt = "Generate an infographic of the current weather in Tokyo."
    """
    try:
        print("Sending request...")
        logging.info(f'run_gemini_image_api input| model {model} | prompt {prompt} | image_name {image_name} | output_folder {output_folder} | aspect_ratio {aspect_ratio} | image_size {image_size}')           # 一般信息

        output_result = {}

        # 3. Correct Tool Syntax
        # The dictionary syntax {"google_search": {}} is often deprecated or incorrect in newer SDKs.
        # We use the types.Tool wrapper instead.
        search_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

        # image_size = "1K"
        # aspect_ratio = "16:9"
        full_path = ""
        if not os.path.isabs(image_name):
            ## relative path
            if output_folder is not None:
                # os.path.normpath removes the "./" and cleans up the path, image_path "./output_image_1.jpg"
                full_path = os.path.normpath(os.path.join(output_folder, image_name))
            else:
                full_path = os.path.normpath(os.path.join(ROOT_DIR, image_name))
            logging.debug(f"run_gemini_image_api output to image name and full path {image_name} output_folder {output_folder} and full_path {full_path}")

        else:
            logging.debug(f"run_gemini_image_api output to image name and full path {image_name}")

        ## Save to full_path create folder before
        full_path_dir = os.path.dirname(full_path)
        if full_path_dir and os.path.exists(full_path_dir):
            logging.debug(f"Directory full_path_dir exists: {full_path_dir}")
        else:
            os.makedirs(full_path_dir, exist_ok=True)
            logging.debug(f"Directory checked/created: {full_path_dir}")
        response = None

        start_timestamp = time.time()
        if model == MODEL_GEMINI_3_PRO_IMAGE_PREVIEW:

            response = client.models.generate_content(
                model=model,
                contents=prompt,             
                config=types.GenerateContentConfig(
                    tools=[{"google_search": {}}],
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio,
                        image_size=image_size    ## 4K 2K 1K
                    ),
                    # thinking_config=types.ThinkingConfig(thinking_level="low")
                )
            )
            logging.debug(f"run_gemini_image_api model {model}")
            
        elif model == MODEL_GEMINI_2_5_FLASH_IMAGE:

            response = client.models.generate_content(
                model = model, 
                contents=prompt,
                # response_modalities=[Modality.IMAGE, Modality.TEXT],
                # config=types.GenerateContentConfig(
                #     image_config=types.ImageConfig(
                #         aspect_ratio=aspect_ratio,
                #         image_size=image_size # Gemini 2.5 Flash Image supports up to 2K resolution
                #     ),
                # )
            )
            logging.debug(f"run_gemini_image_api model {model}")

        else:
            logging.debug(f"run_gemini_image_api Model {model} Currently Not Available!")
        end_timestamp = time.time()
        time_taken_seconds = end_timestamp - start_timestamp
        logging.info(f"run_gemini_image_api times taken seconds: {time_taken_seconds}")

        success = False
        output_message = ""
        if response is not None:
            logging.debug(f"run_gemini_image_api input response Successfully {response}")
            # Handle the image if it exists
            if response.candidates and response.candidates[0].content.parts:
                parts = response.candidates[0].content.parts
                logging.debug(f"run_gemini_image_api input response parts {parts}")
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        logging.debug(f"🖼️ Image generated: {len(part.inline_data.data)} bytes")
                        ## return success true
                        success = True
                        image_parts = [part for part in response.parts if part.inline_data]
                        if image_parts:
                            image = image_parts[0].as_image()
                            try:
                                image.save(full_path)
                                logging.info(f"run_gemini_image_api Successfully Save to Path {full_path}")
                            except Exception as e:
                                logging.error(f"run_gemini_image_api Failed to Save to Path {full_path} with error {e}")
                                full_path = os.path.join(DEFAULT_IMAGE_DIR, get_temp_file_name())
                                image.save(full_path)
                                logging.info(f"run_gemini_image_api to Save to Path Local {full_path}")
                            # image.show()
                    elif part.text:
                        logging.debug(f"📝 Text response: {part.text}")
                        output_message += part.text
            else:
                logging.error(f"run_gemini_image_api failed with {response}")
        else:
            logging.error(f"run_gemini_image_api Gemini Image API response is None...")
        
        output_result["image_path"] = full_path
        output_result["message"] = output_message
        output_result["success"] = success

        return output_result
    except Exception as e:
        print(f"\n❌ ERROR: run_gemini_image_api {e}")
        # If it's a timeout, you'll now see 'ReadTimeout' or similar.
        output_result["success"] = False        
        return output_result

@server.prompt("system_prompt")
def system_prompt() -> str:
    """
    """
    prompt="""
    The tool 
        'gemini_image_api' takes query as input and return dict of url: data_url
    """
    return prompt

@server.tool()
def generate_image_gemini(
    model: Annotated[str, "The image generation model to use. Defaults to 'gemini-2.5-flash-image'. Supported models include 'gemini-3-pro-image-preview', 'gemini-2.5-flash-image' "] = "gemini-2.5-flash-image",
    prompt: Annotated[str, "A detailed text description for the image to be generated."] = "A detailed, cinematic image of a futuristic city.",
    image_name: Annotated[str, "The filename for the output image. Defaults to 'gemini_output_images.png'."] = "gemini_output_images.png",
    output_folder: Annotated[Optional[str], "The optional folder path where the image will be saved. If None, uses a default location."] = None,
    aspect_ratio: Annotated[str, "The aspect ratio of the generated image (e.g., '16:9', '1:1', '4:3')."] = "16:9",
    image_size: Annotated[str, "The size/resolution of the generated image (e.g., '1K', '2K')."] = "1K"
    ) -> Dict:
    """ Generates an image using the Gemini Image API.
            Supported Models (aliases are internal):
            The model parameter allows selection between available image generation models.
            - "gemini-2.5-flash-image" (recommended default for stable, fast response).
            - "gemini-3-pro-image-preview".

            Aliases for these models are 'nano-banana 2.5' and 'nano-banana 3 Pro' respectively.
            Please use 'gemini-2.5-flash-image' unless the user specifically requests the Gemini 3 model.

        Args:
            model: The image generation model to use (see supported models above). Defaults to "gemini-2.5-flash-image".
            prompt: A detailed text description for the image to be generated.
            image_name: The filename for the output image, can be a relative path. Defaults to "gemini_output_images.png".
            output_folder: The optional folder path where the image will be saved (use the user's personal directory). If None, uses a server default.
            aspect_ratio: The aspect ratio of the generated image (e.g., '16:9', '1:1', '4:3'). Defaults to '16:9'.
            image_size: The size/resolution of the generated image (e.g., '1K', '2K', '4K'). Defaults to '1K'.

        Return:
            Dict: Result dictionary containing image path, message, and success status.
            output_result["image_path"]: str
            output_result["message"]: str
            output_result["success"]: bool
    """
    try:
        # results list of json
        return run_gemini_image_api(model, prompt, image_name, output_folder, aspect_ratio, image_size)

    except httpx.HTTPError as e:
        return f"Error communicating with Bing Image Search API: {str(e)}"
        return []
    except Exception as e:
        return f"Unexpected error: {str(e)}"
        return []

@server.tool()
def generate_image_nano_banana(
        model: Annotated[str, "The image generation model to use. Defaults to 'gemini-2.5-flash-image'. Supported models include 'gemini-3-pro-image-preview', 'gemini-2.5-flash-image' "] = "gemini-2.5-flash-image",
        prompt: Annotated[str, "A detailed text description for the image to be generated."] = "A detailed, cinematic image of a futuristic city.",
        image_name: Annotated[str, "The filename for the output image. Defaults to 'gemini_output_images.png'."] = "gemini_output_images.png",
        output_folder: Annotated[Optional[str], "The optional folder path where the image will be saved. If None, uses a default location."] = None,
        aspect_ratio: Annotated[str, "The aspect ratio of the generated image (e.g., '16:9', '1:1', '4:3')."] = "16:9",
        image_size: Annotated[str, "The size/resolution of the generated image (e.g., '1K', '2K')."] = "1K"
) -> Dict:
    """ Get Public Available Stock Symbols from Global Marketplace

        Args:
            model: The image generation model to use. Defaults to "gemini-2.5-flash-image". Supported Models such as follows Google Gemini Doc, such as "gemini-3-pro-image-preview", "gemini-2.5-flash-image", note that nano-banana is the alias name of the Gemini Image Model. Nano banana 3 Pro refers to Gemini 3 pro preview, and Nono Banana 2.5 refers to Gemini 2.5. Unless specified by user to use Gemini 3 model preview, general 'Neno Banana' image models, please use 'gemini-2.5-flash-image' for more stable and fast response.
            prompt: A detailed text description for the image to be generated.
            image_name: The filename for the output image, can be a relative path, such as "./new_gemini_image.png", etc. Defaults to "gemini_output_images.png".
            output_folder: The optional folder path where the image will be saved. Please use the users' personal directory for this path. If None, uses a default location to the root folder of the server/image
            aspect_ratio: The aspect ratio of the generated image (e.g., '16:9', '1:1', '4:3'), defaults to '16:9'.
            image_size: The size/resolution of the generated image (e.g., '1K', '2K', '4K'), defaults to '1K'.

        Return:
            Dict:  output_result is the result dict of MCP returned
            output_result["image_path"] = full_path: str
            output_result["message"] = output_message: str
            output_result["success"] = success: bool
    """
    try:
        # results list of json
        return run_gemini_image_api(model, prompt, image_name, output_folder, aspect_ratio, image_size)

    except httpx.HTTPError as e:
        return f"Error communicating with Bing Image Search API: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def test_run_gemini_image_api():
    """
    """
    prompt="Generate an Image of a female Human Resource Specialist working in a Chinese Internet company. Glassed, Hair Dyed as Purple Color, Holding a toy of Labubu"
    run_gemini_image_api(model = MODEL_GEMINI_2_5_FLASH_IMAGE, prompt=prompt, image_name="./image_gemini_2.5_model.png")
    run_gemini_image_api(model = MODEL_GEMINI_3_PRO_IMAGE_PREVIEW, prompt=prompt, image_name="./image_gemini_3_model.png")

if __name__ == "__main__":
    # Initialize and run the server
    server.run(transport='stdio')
