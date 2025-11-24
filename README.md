# Gemini API MCP Server & DeepNLP OneKey MCP Router Support

[![MCP Marketplace User Review Rating Badge](https://www.deepnlp.org/api/marketplace/svg?name=gemini-google/gemini-3-pro-nano-banana-image-preview)](https://deepnlp.org/store/model/image-generator/pub-gemini-google/gemini-3-pro-nano-banana-image-preview)

This MCP server is a API wrapper of Official Gemini API, supports various Gemini Models (Gemini 2.5, Gemini 3 for text, images, speech, etc)

| Model | OneKey MCP Router Website|
| ---- | ---- |
| Gemini 2.5 Flash (Nano Banana) |  [Gemini 2.5 Flash Image MCP Website](https://www.deepnlp.org/store/model/image-generator/pub-gemini-google/nano-banana) |
| Gemini 3 Pro Image Preview (Nano Banana Pro) |  [Gemini 3 Pro Image MCP Website](https://deepnlp.org/store/model/image-generator/pub-gemini-google/gemini-3-pro-nano-banana-image-preview)  |


# Usage

## 1.1 HttpStreaming MCP OneKey Router (No Installation Needed)
Google Gemini Image Preview(Nano Banana) on OneKey MCP Router

See OneKey MCP Router Demo Usage [Document](https://www.deepnlp.org/doc/onekey_mcp_router) and Register [Keys](https://deepnlp.org/workspace/keys)

[Gemini Nano Banana Playground](https://agent.deepnlp.org)


### MCP Client (Cursor, Claude Desktop, VS Code, etc)

Use One Access Key to MCP Proxy to use Nano Banana


Gemini MCP Server on DeepNLP OneKey Router
```
{
	"mcpServers":{
		"gemini": {
			"url": "https://agent.deepnlp.org/mcp?server_name=gemini&onekey={DEEPNLP_ONEKEY_ROUTER_ACCESS}"
		}
	}
}
```

or Alias (server_name=nano_banana)

```
{
	"mcpServers":{
		"nano-banana": {
			"url": "https://agent.deepnlp.org/mcp?server_name=nano_banana&onekey={DEEPNLP_ONEKEY_ROUTER_ACCESS}"
		}
	}
}
```

Beta Test Key 

```
DEEPNLP_ONEKEY_ROUTER_ACCESS=BETA_TEST_KEY_OCT_2025


{
	"mcpServers":{
		"nano-banana": {
			"url": "https://agent.deepnlp.org/mcp?server_name=nano_banana&onekey=BETA_TEST_KEY_OCT_2025"
		},
		"gemini": {
			"url": "https://agent.deepnlp.org/mcp?server_name=gemini&onekey=BETA_TEST_KEY_OCT_2025"
		},

	}
}
```


## 1.2 Locally Install (Python/uv)

```
pip install gemini_mcp_onekey

pip install nano_banana_mcp_onekey

```


mcp_config.json

```

{
	"mcpServers":{
	    "gemini": {
	      "command": "uvx",
	      "args": [
	          "gemini_mcp_onekey"
	      ],
	      "env": {
	          "GOOGLE_API_KEY": "YOUR_GOOGLE_API_KEYS"
	      }
	    },
	}
}
```



## Tools
### gemini_image_api

**Parameters**
model: str = "gemini-2.5-flash-image",
prompt: str = "A detailed, cinematic image of a futuristic city.",
image_name: str = "gemini_output_images.png",
output_folder: Optional[str] = None,
aspect_ratio: str = "16:9",
image_size: str = "1K"


