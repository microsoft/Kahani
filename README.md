## Kahani - Cultural Visual Story Telling Pipeline
### Work done in collaboration with Karya

### T2I Models used:

1. [FLUX 1.1 PRO ULTRA](https://replicate.com/black-forest-labs/flux-1.1-pro-ultra)


### Setting up:

#### Setting up PIM tool for ease of access to managed identities

```
git clone https://github.com/msr-new-england/pimtool
# While doing az login select your SC-ALT
az login
az login --scope https://graph.microsoft.com/.default
cd pimtool
pip install .
pimtool
# If pimtool is not installed in path
export PATH=/home/<alias>/.local/bin:$PATH
```

#### First time running git?
git config --global user.email "you@example.com"
git config --global user.name "Your Name"

### Steps to run:

1. Install pip and python in your system. To install (Linux), run `sudo apt install python3-pip`
2. Clone this repository and install all the python packages from requirements using `python3 -m pip install -r requirements.txt` in your CLI.
3. Create a `.env` file inside the project directory and paste the contents of the `env_template.txt` file and modify the values with your personal credentials. You would require `REPLICATE API TOKEN` and Azure OpenAI endpoint and Managed Identity Client ID.
4. Now, to run the code, set the story-title to any story from the `data` folder and simply run `python3 kahani-visuals.py`. An `outputs` folder will be created with a sub-folder specific to your story with all the generated outputs.

### Directory Tree

```bash
.
├── README.md
├── env_template.txt
├── kahani-visuals.py
└── requirements.txt
```

