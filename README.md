# Yeh Hai Meri Kahani

For TAB we want to create a system that's engaging for the user during the complete generation of our multi-step visual story

Basic 
- [ ] remap the volume
 
Here are some possible approaches:

- [ ] Gradio Streaming Chat with multi-step process
- [ ] SDXL Turbo
- [ ] Manual control

Additional UX improvements:
- [ ] Beautify the formatting of the story

## Developer Notes:

```
$ docker build . -t kahani-streaming
$ touch .env
$ vi .env
# SDAPI_HOST=http://172.17.0.1:7860
# OPENAI_API_KEY=<OPENAI_API_KEY>
$ docker run -it -d -p 8080:8080 --env-file .env kahani-streaming

```